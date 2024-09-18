from typing import Any, List, Dict, Callable

from submitit.helpers import Checkpointable

from .callbacks import Callback


def handle_signal(sig, frame):
    print(f"Signal {sig} received!")
    # TODO: make sure to run the callbacks?


def task_fn_to_class(task_fn: Callable) -> Checkpointable:
    t = type("Task", (Checkpointable,), {"__call__": task_fn})
    o = t()


class Job(Checkpointable):
    context: Dict[str, Any] = {}

    def __init__(self, commands: List[str]):
        self.commands = commands
        self.is_multirun = len(commands) > 1


class Run:
    command: str
    context: Dict[str, Any] = {}
    callbacks: List[Callback]

    # each run can have different callbacks! should be part of this, not launcher
    def __init__(self, callbacks: List[Callback], command: str):
        self.command = command

    def set_args(self):
        import sys

        sys.argv = self.command.split()


class Launcher:
    def __init__(
            self,
            callbacks: List[Callback],
            execute_final_callbacks_in_reverse: bool = False,
            _called_from_cli: bool = False,
            _commands: List[str] = None
    ):
        """
        :param callbacks: The order of callbacks matters
        :param execute_final_callbacks_in_reverse:
            If True, the final callbacks will be executed in reverse order
        """
        self.callbacks = callbacks
        self.exec_in_reverse = execute_final_callbacks_in_reverse
        self._called_from_cli = _called_from_cli

        self.runs = [
            Run(cmd) for cmd in _commands
        ]
        self.job = Job(_commands)

    def start(self):
        if not self._called_from_cli:
            return

        for callback in self.callbacks:
            self.job = callback.before_job_start(job=self.job)

        for callback in self.callbacks:
            for i in range(len(self.runs)):
                self.runs[i].set_args()
                self.runs[i] = callback.before_run_start(run=self.runs[i])

        for callback in self.callbacks:
            for i in range(len(self.runs)):
                self.runs[i].set_args()
                self.runs[i] = callback.on_run_start(run=self.runs[i])

    def end(self):
        if not self._called_from_cli:
            return

        for callback in reversed(self.callbacks) if self.exec_in_reverse else self.callbacks:
            for i in range(len(self.runs)):
                self.runs[i].set_args()
                self.runs[i] = callback.on_run_end(run=self.runs[i])

        for callback in reversed(self.callbacks) if self.exec_in_reverse else self.callbacks:
            for i in range(len(self.runs)):
                self.runs[i].set_args()
                self.runs[i] = callback.after_run_end(run=self.runs[i])

        for callback in reversed(self.callbacks) if self.exec_in_reverse else self.callbacks:
            self.job = callback.after_job_end(job=self.job)


def instrument_run(
        task: Callable,
        make_checkpointable: bool = False,
        execute_final_callbacks_in_reverse: bool = False,
        *args: Any,
        **kwargs: Any
) -> Launcher:
    # this is the function the user calls!
    if make_checkpointable:
        task = task_fn_to_class(task)

    launcher = Launcher()
