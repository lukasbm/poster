import abc

from poster.launcher import Job, Run


class Callback(abc.ABC):
    def before_job_start(self, job: Job) -> Job:
        """
        Called before the job starts.
        Sets up the job (e.g. output directory).
        Could also refer to many runs.
        """
        pass

    def before_run_start(self, run: Run) -> Run:
        """
        Called before the run starts.
        Sets up the run (e.g. argument parsing).
        """
        pass

    def on_run_start(self, run: Run) -> Run:
        """
        Called when the run starts.
        Useful for in-run activities, e.g. experiment tracking.
        """
        pass

    def on_run_end(self, run: Run) -> Run:
        """
        called when the main execution is complete.
        good for clean up jobs.
        """
        pass

    def after_run_end(self, run: Run) -> Run:
        pass

    def after_job_end(self, job: Job) -> Job:
        pass
