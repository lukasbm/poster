from .callback import Callback
import logging

log = logging.getLogger(__name__)


class FireCallback(Callback):
    def __init__(self):
        pass

    def before_run_start(self):
        log.info("FireCallback: before_run_start")
