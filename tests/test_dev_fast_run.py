import pytest

from helpers import run_command


def test_fast_dev_run():
    """Test running for 1 train, val and test batch."""
    command = [
        "src/train.py",
        "-c",
        "configs/train.yaml",
        "--trainer.fast_dev_run=true",
    ]
    run_command(command)
