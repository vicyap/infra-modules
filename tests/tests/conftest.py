"""Common pytest fixtures."""
import logging
import os
import shutil
from typing import Dict, Optional
from uuid import uuid4

import pytest
import tftest

LOGGER = logging.getLogger(__name__)


def pytest_configure(config):
    # Create a log file for each pytest xdist worker.
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    if worker_id is not None:
        logging.basicConfig(
            datefmt=config.getini("log_file_date_format"),
            filename=f"pytest_{worker_id}.log",
            format=config.getini("log_file_format"),
            level=config.getini("log_file_level"),
        )


@pytest.fixture
def modules_dir() -> str:
    """Returns the top-level modules directory."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir)


@pytest.fixture
def modules_dir_tmp(modules_dir, tmp_path) -> str:
    """Copies the top-level modules directory to a temporary directory.

    Copying the top-level modules dir to its own directory is useful for not reusing the existing
    examples directories to run these tests. This enables two things:
    * Tests can run in parallel since each test function has its own directory.
    * Tests do not use existing example stacks that are already deployed.
    """
    path = str(tmp_path)
    LOGGER.debug(f"copying {modules_dir=} to {path=}")
    shutil.copytree(str(modules_dir), str(path), dirs_exist_ok=True)
    return str(path)


@pytest.fixture
def examples_dir_tmp(modules_dir_tmp) -> str:
    """Returns the path to the examples dir in the temporary modules dir."""
    return os.path.join(modules_dir_tmp, "examples")


@pytest.fixture
def tf_apply():
    """Terraform apply and destroy helper.

    Runs terraform apply and destroys it at the end of the test.

    Full Example:

    def test_mytest(examples_dir_tmp, tf_apply):
        outputs = tf_apply("my-module-example", examples_dir_tmp, tf_vars={
            "my-variable": "my-value",
        })
    """
    stacks = []

    def _TerraformTest_apply(tfdir, basedir, tf_vars: Optional[Dict] = None) -> Dict:
        tf = tftest.TerraformTest(tfdir, basedir)
        stacks.append((tf, tf_vars))
        tf.setup()
        tf.init()
        tf.apply(tf_vars=tf_vars)
        return tf.output()

    yield _TerraformTest_apply
    # Destroy the stacks in reverse in case there are dependencies where later stacks depend on
    # earlier stacks. Earlier stacks may fail to destroy if it has resources from later stacks.
    for stack, tf_vars in reversed(stacks):
        stack.destroy(auto_approve=True, tf_vars=tf_vars)
