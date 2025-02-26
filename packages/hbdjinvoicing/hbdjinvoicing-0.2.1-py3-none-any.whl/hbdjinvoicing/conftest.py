import os
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

# AUTOUSE FIXTURES


@pytest.fixture(autouse=True)
def env_variables(monkeypatch):
    with patch.dict(os.environ, clear=True):
        env_vars = {
            # add the test env variables here
        }
        for k, v in env_vars.items():
            monkeypatch.setenv(k, v)
        yield  # This is the magical bit which restore the environment after


# OTHER FIXTURES


@pytest.fixture
def anonymous_client():
    return Client()


@pytest.fixture
def user():
    return get_user_model().objects.create(email="user_log@example.com")


@pytest.fixture
def logged_client(user):
    client = Client()
    client.force_login(user)
    return client
