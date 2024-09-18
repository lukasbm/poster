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
    print("simple example!")

    # build hydra stores
    name_store = store(group="names")
    name_store(just(["Alice", "Bob", "Charlie"]), name="basic")
    name_store(just(["Dave", "Eve", "Frank"]), name="advanced")

    launcher = Launcher(callbacks=[
        HydraZenCallback(task_fn=main_fn, store=store, job_type="simple"),
    ])
    launcher.start()
    # TODO: where is this called launcher.end()
