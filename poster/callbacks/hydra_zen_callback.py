from typing import Callable

from .callback import Callback
from hydra_zen import ZenStore
import logging

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

        self.store.add_to_hydra_store(overwrite_ok=True)
        # exposes the cli
        zen(self.task_fn).hydra_main(config_name=self.job_type, version_base=self.hydra_version_base)
