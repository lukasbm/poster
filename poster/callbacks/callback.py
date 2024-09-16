import abc


class Callback(abc.ABC):
    def before_job_start(self):
        pass

    def before_run_start(self):
        pass

    def on_run_start(self):
        pass

    def on_run_end(self):
        pass

    def after_run_end(self):
        pass

    def after_job_end(self):
        pass
