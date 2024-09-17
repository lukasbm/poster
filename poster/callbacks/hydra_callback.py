from .callback import Callback


class HydraCallback(Callback):
    def __init__(self, config_name='config', config_path=None, overrides=None):
        self.config_name = config_name
        self.config_path = config_path
        self.overrides = overrides or []

    def before_run_start(self):
        # lazy imports to speed up the import process
        from hydra import initialize, compose
        from omegaconf import OmegaConf

        # Initialize Hydra and compose the configuration
        with initialize(config_path=self.config_path, version_base=None):
            cfg = compose(config_name=self.config_name, overrides=self.overrides)
            # Convert OmegaConf object to a dictionary
            cfg_dict = OmegaConf.to_container(cfg, resolve=True)
            # Update the context's config
            context['config'].update(cfg_dict)
            # Optionally store the Hydra config object in the context
            context['hydra_cfg'] = cfg
