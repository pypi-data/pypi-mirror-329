import torch
from gymnasium import spaces
from stable_baselines3 import PPO, SAC


class OnnxablePolicy(torch.nn.Module):
    def __init__(
        self,
        obs_keys=None,
        features_extractor=None,
        mlp_extractor=None,
        action_net=None,
        value_net=None,
        use_obs_array=None,
        actor=None,
    ):
        super().__init__()
        self.obs_keys = obs_keys
        self.features_extractor = features_extractor
        self.mlp_extractor = mlp_extractor
        self.action_net = action_net
        self.value_net = value_net
        self.use_obs_array = use_obs_array
        self.actor = actor

    def forward_sac(self, observation: torch.Tensor, state_ins):
        return self.actor(observation, deterministic=True), state_ins

    def forward_ppo(self, obs, state_ins):
        features = None

        if self.use_obs_array:
            features = self.features_extractor(obs)
        else:
            obs_dict = {k: v for k, v in zip(self.obs_keys, obs)}
            features = self.features_extractor(obs_dict)

        action_hidden, value_hidden = self.mlp_extractor(features)
        return self.action_net(action_hidden), state_ins

    def forward(self, obs, state_ins):
        if self.actor:
            return self.forward_sac(obs, state_ins)
        else:
            return self.forward_ppo(obs, state_ins)


def export_model_as_onnx(model, onnx_model_path: str, use_obs_array: bool = False, obs_keys=None):
    if obs_keys is None:
        obs_keys = ["obs"]
    policy = model.policy.to("cpu")
    dummy_input = None
    onnxable_model = None

    if isinstance(model, SAC):
        assert use_obs_array, "SAC ONNX export works with use_obs_array=True, MLPPolicy and SBGSingleObsEnv only."

    if isinstance(model, PPO):
        onnxable_model = OnnxablePolicy(
            obs_keys,
            policy.features_extractor,
            policy.mlp_extractor,
            policy.action_net,
            policy.value_net,
            use_obs_array,
        )
        if use_obs_array:
            dummy_input = torch.unsqueeze(torch.tensor(model.observation_space.sample()), 0)
        else:
            dummy_input = dict(model.observation_space.sample())
            for k, v in dummy_input.items():
                dummy_input[k] = torch.from_numpy(v).unsqueeze(0)
            dummy_input = [v for v in dummy_input.values()]

    elif isinstance(model, SAC):
        onnxable_model = OnnxablePolicy(actor=model.policy.actor)
        dummy_input = torch.randn(1, *model.observation_space.shape)

    torch.onnx.export(
        onnxable_model,
        args=(dummy_input, torch.zeros(1).float()),
        f=onnx_model_path,
        opset_version=17,
        input_names=["obs", "state_ins"],
        output_names=["output", "state_outs"],
        dynamic_axes={
            "obs": {0: "batch_size"},
            "state_ins": {0: "batch_size"},  # variable length axes
            "output": {0: "batch_size"},
            "state_outs": {0: "batch_size"},
        },
    )

    # We only verify with PPO currently due to different output shape with SAC
    # (this can be updated in the future)
    if isinstance(model, PPO):
        # If the space is MultiDiscrete, we skip verifying as action output will have an expected mismatch
        # (the output from onnx will be the action logits for each discrete action,
        # while the output from sb3 will be a single int)
        if not isinstance(model.action_space, spaces.MultiDiscrete):
            verify_onnx_export(model, onnx_model_path, use_obs_array=use_obs_array)


def verify_onnx_export(ppo: PPO, onnx_model_path: str, num_tests=10, use_obs_array: bool = False):
    import numpy as np
    import onnx
    import onnxruntime as ort

    onnx_model = onnx.load(onnx_model_path)
    onnx.checker.check_model(onnx_model)

    sb3_model = ppo.policy.to("cpu")
    ort_sess = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])

    for i in range(num_tests):
        obs = None
        obs2 = None

        if use_obs_array:
            obs = np.expand_dims(ppo.observation_space.sample(), axis=0)
            obs2 = torch.tensor(obs)
        else:
            obs = dict(ppo.observation_space.sample())
            obs2 = {}
            for k, v in obs.items():
                obs2[k] = torch.from_numpy(v).unsqueeze(0)
            obs = [v for v in obs.values()]

        with torch.no_grad():
            action_sb3, _, _ = sb3_model(obs2, deterministic=True)

        action_onnx, state_outs = ort_sess.run(None, {"obs": obs, "state_ins": np.array([0.0], dtype=np.float32)})
        assert np.allclose(action_sb3, action_onnx, atol=1e-5), "Mismatch in action output"
        assert np.allclose(state_outs, np.array([0.0]), atol=1e-5), "Mismatch in state_outs output"
