import os

import pytest

import wandb


def test_wandb_credentials():
    api_key = os.getenv("WANDB_API_KEY")
    entity = os.getenv("WANDB_ENTITY")
    project = os.getenv("WANDB_PROJECT")

    assert api_key is not None, "WANDB_API_KEY is not set."
    assert entity is not None, "WANDB_ENTITY is not set."
    assert project is not None, "WANDB_PROJECT is not set."

    wandb.login(key=api_key)

    try:
        run = wandb.init(entity=entity, project=project, job_type="pytest_connection")
        run.finish()
    except Exception as e:
        pytest.fail(
            f"wandb initialization failed, possibly due to invalid credentials or network issues: {str(e)}",
        )
