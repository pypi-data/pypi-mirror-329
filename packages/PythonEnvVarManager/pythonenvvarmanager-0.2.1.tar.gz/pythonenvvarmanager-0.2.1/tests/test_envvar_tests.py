import os

import pytest

import env_manager as ENV


@pytest.fixture
def set_own_dotenv_file():
    dotnet_path = ".env.test"

    if not os.path.exists(dotnet_path):
        open(dotnet_path, "w").close()

    ENV.set_dotenv_path(dotnet_path)

    yield dotnet_path

    if os.path.exists(dotnet_path):
        os.remove(dotnet_path)


def test_envvar_test(set_own_dotenv_file):
    # If DATABASE_URL is not set, it will be added (as a commented-out default) to .env.
    db_url = ENV.getenv("DATABASE_URL", "sqlite:///:memory:")
    assert db_url == "sqlite:///:memory:"
    # If SECRET_KEY is not set, the default will be used and an entry will be added if needed.
    secret_key = ENV.getenv("SECRET_KEY", "default-secret")
    assert secret_key == "default-secret"

    # Optionally, set another environment variable programmatically.
    ENV.setenv("NEW_VAR", "some_value")

    new_var = ENV.getenv("NEW_VAR", "default-value")
    assert new_var == "some_value"

    # Display all tracked environment variables.
    ENV.display_env_vars()


def test_envvar_write_to_file(set_own_dotenv_file):
    # If DATABASE_URL is not set, it will be added (as a commented-out default) to .env.
    ENV.set_write_to_dotenv(True)
    # If SECRET_KEY is not set, the default will be used and an entry will be added if needed.
    secret_key = ENV.getenv("SECRET_KEY", "default-secret")
    assert secret_key == "default-secret"

    ## Verify that the .env file has been updated
    with open(set_own_dotenv_file) as f:
        lines = f.read()
        assert "SECRET_KEY=default-secret" in lines


def test_osgetenv(set_own_dotenv_file):
    if str(os.getenv("OVERWRITE_OS_GETENV", "False")).lower() == "false":
        print("OS GETENV is not overwritten, test will be skipped")
        return

    dotnet_path = set_own_dotenv_file

    ENV.set_write_to_dotenv(False)

    with open(dotnet_path) as f:
        lines = f.read()
        assert "OS_UNCAPTURED" not in lines

    print("Getting osenv", os.getenv("OS_UNCAPTURED", "NO VALUE"))

    with open(dotnet_path) as f:
        lines = f.read()
        assert "OS_UNCAPTURED" not in lines

    ENV.set_write_to_dotenv(True)

    print("Getting osenv", os.getenv("OS_CAPTURED", "NO VALUE"))

    with open(dotnet_path) as f:
        lines = f.read()
        assert "OS_CAPTURED" in lines
