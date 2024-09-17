import logging
from typing import Callable

from hydra_zen import ZenStore

from .callback import Callback

log = logging.getLogger(__name__)


class HydraZenCallback(Callback):
    """
    relies on the user setting up the store(s) beforehand!
    """

    def __init__(self, task_fn: Callable, store: ZenStore, job_type: str, hydra_version_base: str = "1.3"):
        self.task_fn = task_fn
        self.store = store
        self.job_type = job_type
        self.hydra_version_base = hydra_version_base

    def before_run_start(self):
        log.info("HydraZenCallback: before_run_start")

        from hydra_zen import zen

        # TODO add some default settings
        # https://github.com/facebookresearch/hydra/issues/324
        # https://github.com/facebookresearch/hydra/issues/910
        # https://stackoverflow.com/questions/65104134/disable-file-output-of-hydra
        # hydra/job_logging = "disabled"  # disable logging
        # hydra.output_subdir = "null"  # disable output subdir

        self.store.add_to_hydra_store(overwrite_ok=True)
        # exposes the cli
        zen(self.task_fn).hydra_main(config_name=self.job_type, version_base=self.hydra_version_base)
