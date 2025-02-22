#!/usr/bin/env -S uv run
# /// script
# dependencies = ["prefect", "pendulum"]
# ///

from prefect import flow


@flow(log_prints=True)
def hello_world(name: str = "world", goodbye: bool = False):
    if goodbye:
        pass


if __name__ == "__main__":
    hello_world.serve(
        name="my-first-deployment",
        tags=["onboarding"],
        parameters={"goodbye": True},
        interval=60,
    )
