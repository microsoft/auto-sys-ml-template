import pytest  # nopycln: import
from helpers import run_command


def test_fast_dev_run():
    """Test running for 1 train, val and test batch."""
    command = [
        "src/train.py",
        "base=configs/train.yaml",
        "trainer.fast_dev_run=true",
    ]
    run_command(command)


# cpu only test for CI
def test_fast_dev_run_cpu():
    """Test running for 1 train, val and test batch."""
    command = [
        "src/train.py",
        "base=configs/train.yaml",
        "trainer.fast_dev_run=true",
        "trainer.accelerator=cpu",
        "trainer.sync_batchnorm=false",
    ]
    run_command(command)
