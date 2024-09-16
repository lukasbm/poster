from typing import List

from .callbacks import Callback


# TODO: how to pass the context to the callbacks?

class Launcher:
    def __init__(self, callbacks: List[Callback], execute_final_callbacks_in_reverse: bool):
        """
        :param callbacks: The order of callbacks matters
        :param execute_final_callbacks_in_reverse:
            If True, the final callbacks will be executed in reverse order
        """
        self.callbacks = callbacks
        self.context = {}
        self.exec_in_reverse = execute_final_callbacks_in_reverse

    def start(self):
        for callback in self.callbacks:
            callback.before_job_start(self.context)
        for callback in self.callbacks:
            callback.before_run_start(self.context)
        for callback in self.callbacks:
            callback.on_run_start(self.context)

    def end(self):
        for callback in self.callbacks:
            callback.on_run_end(self.context)
        for callback in self.callbacks:
            callback.after_run_end(self.context)
        for callback in reversed(self.callbacks) if self.exec_in_reverse else self.callbacks:
            callback.after_job_end(self.context)
