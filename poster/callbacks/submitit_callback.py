from typing import List, Callable, Dict

from .callback import Callback
import logging

log = logging.getLogger(__name__)


class SubmititCallback(Callback):
    _EXECUTOR = "abstract"

    def __init__(self, task_fn: Callable, task_params: Dict, submitit_conf: Dict):
        self.conf = conf
        self.task_fn = task_fn
        self.task_params = task_params

    def before_job_start(self):
        import submitit  # lazy import to speed up imports
        executor = submitit.AutoExecutor(folder=self.conf["submitit_folder"])
        # or executor = submitit.SlurmExecutor
        executor.update_parameters(**self.conf)  # e.g timeout_min
        job = executor.submit(self.task_fn, **self.task_params)
        # return job


class SLURMSubmititCallback(SubmititCallback):
    _EXECUTOR = "SLURM"


class LocalSubmititCallback(SubmititCallback):
    _EXECUTOR = "LOCAL"
