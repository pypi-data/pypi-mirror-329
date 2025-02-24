"""A package for managing environment variables in Python applications.

This package provides a simple way to manage environment variables in Python applications. It allows
you to set environment variables programmatically, retrieve them, and display all the environment
variables that have been set.
"""

from .env_var_manager import EnvManager

# Version of the realpython-reader package
__version__ = "0.2.0"


def set_dotenv_path(dotenv_path: str) -> None:
    """Set the path to the .env file.

    Args:
        dotenv_path (str): The path to the .env file.
    """
    env = EnvManager()
    env.set_dotnet_path(dotenv_path)


def get_dotenv_path() -> str:
    """Return the path to the .env file.

    Returns:
        str: The path to the .env file.
    """
    env = EnvManager()
    return env.dotenv_path


def set_write_to_dotenv(write_to_dotenv: bool) -> None:
    """Set whether to write undocumented environment variables to the .env file.

    Args:
        write_to_dotenv (bool): Whether to write undocumented environment variables to the .env file.
    """
    env = EnvManager()
    env._write_to_dotenv = write_to_dotenv


def getenv(key: str, default: str | int | None = None) -> str | int:
    """Retrieve an environment variable. If it's not found in os.environ and a default is provided.

    check if the .env file already mentions it (active or commented). If not, append a commented-out
    entry with the default value and caller info. Finally, set os.environ with the default so that
    the application has a value.

    Args:
        key (str): The environment variable key.
        default (str | int): The default value of the environment variable.

    Returns:
        str | int: The value of the environment variable.
    """
    env = EnvManager()
    return env.getenv(key=key, default=default)


def setenv(key: str, value: str) -> None:
    """Set an environment variable in os.environ and update the registry.(This does not update the .env file.).

    Args:
        key (str): The environment variable key.
        value (str): The value of the environment variable
    """
    env = EnvManager()
    return env.setenv(key, value)


def display_env_vars() -> None:
    """Print out all registered environment variables in a readable format."""
    env = EnvManager()
    return env.display_env_vars()


def get_all_vars() -> dict:
    """Return a copy of all tracked environment variables.

    Returns:
        dict: A copy of all tracked environment variables
    """
    env = EnvManager()
    return env.get_all_vars()
