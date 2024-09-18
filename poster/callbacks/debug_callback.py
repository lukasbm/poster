from .callback import Callback
from ..launcher import Job, Run


class DebugCallback(Callback):
    def before_job_start(self, job: Job) -> Job:
        print("DebugCallback: before_job_start")
        return job

    def before_run_start(self, run: Run) -> Run:
        print("DebugCallback: before_run_start")
        return run

    def on_run_start(self, run: Run) -> Run:
        print("DebugCallback: on_run_start")
        return run

    def on_run_end(self, run: Run) -> Run:
        print("DebugCallback: on_run_end")
        return run

    def after_run_end(self, run: Run) -> Run:
        print("DebugCallback: after_run_end")
        return run

    def after_job_end(self, job: Job) -> Job:
        print("DebugCallback: after_job_end")
        return job
