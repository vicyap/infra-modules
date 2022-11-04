"""Tests terraform hello world examples."""
import json
import logging

import pytest

LOGGER = logging.getLogger(__name__)


def test_hello_world(examples_dir_tmp, tf_apply):
    """Tests that we can run terraform and retrieve outputs.

    This test is derived from:
    https://github.com/gruntwork-io/terratest/blob/master/test/terraform_hello_world_example_test.go
    """
    outputs = tf_apply("terraform-hello-world-example", examples_dir_tmp)
    LOGGER.info("outputs: %s" % json.dumps(dict(outputs)))
    assert outputs["hello_world"] == "Hello, World!"
