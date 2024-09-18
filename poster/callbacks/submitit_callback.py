import logging
from typing import Dict, Callable

from poster.launcher import Job
from .callback import Callback

log = logging.getLogger(__name__)


class SubmititCallback(Callback):
    """
    See:
    - https://github.com/facebookincubator/submitit/blob/main/docs/structure.md

    To see how to write valid code for checkpointing: https://github.com/facebookincubator/submitit/blob/main/docs/mnist.py
    It essentially depends on the class variables!

    Submitit flow:
    1. A callable is submitted, and we receive a job instance.
        - The function and arguments are pickled
        - The sbatch bash script is generated
        - the job is submitted
        - in slurm the original environment is used and the task is loaded from the pickle
    2. results are pickled and saved in the job folder
    3. the main process was waiting all the time, and if the file is available, it will be availalbe in the job instance

    Executor can do:
    - submit(callable, *args, **kwargs) -> Job
    - map_array(function, *iterables) -> List[Job]
    - update_parameters(**kwargs) -> None
    Parameters:
    - slurm_array_parallelism: controls the number of concurrently executed tasks
    - gpus_per_node
    """

    # TODO: maybe use command function?
    # But then i cant use checkpointing?
    # Note: checkpointing is only for resubmission
    # i should not rely on it for the main submission

    def __init__(self, task: Callable, task_params: Dict, submitit_conf: Dict):
        self.submitit_conf = submitit_conf
        self.task = task
        self.task_params = task_params

    def before_job_start(self, job: Job) -> Job:
        import submitit  # lazy import to speed up imports

        executor = submitit.AutoExecutor(folder=self.submitit_conf["submitit_folder"])
        executor.update_parameters(**self.submitit_conf)  # e.g timeout_min

        submission = executor.submit(self.task, **self.task_params)
        return job

