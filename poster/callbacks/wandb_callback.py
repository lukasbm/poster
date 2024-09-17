from .callback import Callback


class WandBCallback(Callback):

    def __init__(self):
        pass

    def on_run_start(self):
        import wandb
        wandb.init()

    def on_run_end(self):
        import wandb
        wandb.finish()
