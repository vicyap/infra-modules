# Infrastructure Modules - Tests

This directory contains code to automatically apply, test and destroy the example modules at [examples](../examples).

## Setup

Install `poetry`. https://python-poetry.org/docs/#installation

For Linux, MacOS, Windows (WSL):

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

After installing `poetry`, install this project's dependencies with the following:

```
poetry install
```

## Running Tests

`aws-vault exec aws-test-role-profile --duration=4h -- poetry run pytest`

Notes:
* It's important to set the duration to more than 1 hour because some tests can take a long time.
* Ideally, we would run these tests in a separate testing account. 

## Developing Tests

The basic workflow for developing Terraform tests is the following:

1. Create a small, standalone module. This module should go in [modules](../modules).
2. Create an easy-to-deploy example for that module. This example should go in [examples](../examples). It's possible to have more than 1 example per module.
3. Run `terraform apply` to deploy the example into a real environment.
4. Validate that what you just deployed works as expected. This step is specific to the type of infrastructure you’re testing. For example, for an ALB, you might validate it by sending an HTTP request and checking that you receive back the expected response.
5. Run terraform destroy at the end of the test to clean up.
6. Code steps 3, 4, 5 as a test in [tests](./tests). There are test fixtures in `conftest.py` to help with running `terraform apply` and `terraform destroy`.

## Diagram

![](./_assets/infrastructure-modules-Testing.drawio.svg)
