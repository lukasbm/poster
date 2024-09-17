from typing import List
from hydra_zen import store, just

from poster import Launcher, HydraZenCallback


@store(
    name="simple",
    hydra_defaults=[
        {"names": "basic"}
    ]
)
def main_fn(a: int, names: List[str]) -> int:
    print("Hello world!", *names)
    return 42 + a


if __name__ == "__main__":
    print("simple")

    name_store = store(group="names")
    name_store(just(["Alice", "Bob", "Charlie"]), name="basic")

    launcher = Launcher(callbacks=[
        HydraZenCallback(task_fn=main_fn, store=store, job_type="simple"),
    ])
    launcher.start()
