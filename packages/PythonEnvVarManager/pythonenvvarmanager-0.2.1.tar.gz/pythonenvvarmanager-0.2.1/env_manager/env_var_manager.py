"""Singleton class to manage environment variables and write missing ones to a .env file."""

import inspect
import os
import re
from os.path import basename

from dotenv import load_dotenv
from loguru import logger as log

original_getenv = os.getenv  # Keep reference to the original


class EnvManager:
    """Singleton class to manage environment variables and write missing ones to a .env file."""

    _instance = None
    _initialized = False
    _write_to_dotenv = False
    _os_getenv_overwritten = False
    dotenv_path: str = ".env"

    def __new__(cls, *args: str, **kwargs) -> "EnvManager":
        """Singleton constructor to ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dotenv_path: str = ".env") -> None:
        """Initialize the singleton with the path to the .env file.

        Args:
            dotenv_path (str, optional): Path to the .env file. Defaults to ".env".
        """
        if self._initialized:
            return  # Avoid reinitialization in the singleton

        self.dotenv_path = dotenv_path
        # Load any existing environment variables from the .env file into os.environ
        load_dotenv(dotenv_path)
        # Also read the raw lines of the .env file for later checks.
        self._load_dotenv_file()
        self._registered_vars = {}  # Registry to track accessed variables
        self._initialized = True

        if str(self.getenv("OVERWRITE_OS_GETENV", "False")).lower() == "true":
            os.getenv = self.getenv
            self._os_getenv_overwritten = True
            log.debug("OS Getenv is replaced with PythonEnvVarManger wrapper")
        else:
            log.debug(
                "OS Getenv is not replaced with PythonEnvVarManger wrapper"
            )

        self._write_to_dotenv = (
            str(self.getenv("WRITE_ENV_VARS_TO_DOTENV", "False")).lower()
            == "true"
        )
        if self._write_to_dotenv:
            log.debug(
                "Initializing EnvManager and writing undocumented vars to dotenv file, to change this update `WRITE_ENV_VARS_TO_DOTENV` to `False`"
            )
        else:
            log.debug(
                "Initializing EnvManager without updating dotenv, to change this update `WRITE_ENV_VARS_TO_DOTENV` to `True`"
            )

    def set_dotnet_path(self, path: str) -> None:
        """Set the path to the .env file.

        Args:
            path (str): The path to the .env file.
        """
        self.dotenv_path = path
        self._load_dotenv_file()
        log.debug(f"Dotenv path set to {path}")

    def _load_dotenv_file(self) -> None:
        """Load the .env file contents into memory as a list of lines."""
        try:
            with open(self.dotenv_path) as f:
                self._env_lines = f.readlines()
        except FileNotFoundError:
            self._env_lines = []

    def _is_key_in_env_file(self, key: str) -> bool:
        """Check if the key is mentioned in the .env file. This matches lines that either define the variable or are commented-out lines.

        Args:
            key (str): The environment variable key.
        """
        # This regex matches lines that (optionally) start with '#' or whitespace,
        # then the exact key, optional spaces, then '='.
        pattern = r"^[#\s]*" + re.escape(key) + r"\s*="
        return any(re.search(pattern, line) for line in self._env_lines)

    def _append_missing_var_to_dotenv(
        self,
        key: str,
        value: str | int,
        default: str | int,
        filename: str | None,
        line_number: str | int | None,
    ) -> None:
        """Append a commented-out default entry to the .env file with a comment showing where the variable was requested.

        Args:
            key (str): The environment variable key.
            value (str | int): The value of the environment variable.
            default (str | int): The default value of the environment variable.
            filename (str | None): The name of the file where the variable was requested.
            line_number (str | int | None): The line number in the file where the variable was requested.


        """
        comment_line = ""
        if not filename or not line_number:
            comment_line = "# Default value set from unknown source\n"
        else:
            comment_line = (
                f"# Default value set from {filename}:{line_number}\n"
            )
        key_value = value if value else ""
        commented_key_line = f"# {key}={key_value} # Default: {default}\n"
        try:
            with open(self.dotenv_path, "a") as f:
                f.write("\n" + comment_line)
                f.write(commented_key_line)
            # Also update the in-memory list so we don't add it again later.
            self._env_lines.append("\n")
            self._env_lines.append(comment_line)
            self._env_lines.append(commented_key_line)
        except FileNotFoundError as e:
            print(
                f"Error appending missing variable {key} to {self.dotenv_path}: {e}"
            )

    def getenv(self, key: str, default: str | int | None = None) -> str | int:
        """Retrieve an environment variable. If it's not found in os.environ and a default is provided.

        check if the .env file already mentions it (active or commented). If not, append a commented-out
        entry with the default value and caller info. Finally, set os.environ with the default so that
        the application has a value.

        Args:
            key (str): The environment variable key.
            default (str | int): The default value of the environment variable.
        """
        global original_getenv
        value = original_getenv(key, default)
        # Capture the caller's module and line number.
        caller_frame = inspect.stack()[1]
        filename = basename(caller_frame.filename)
        line_number = caller_frame.lineno

        log.debug(f"Getting {key} from os.environ: {value}")

        # Only update the .env file if no active or commented line already mentions the key.
        if (
            self._write_to_dotenv
            and not self._is_key_in_env_file(key)
            and value is not None
        ):
            self._append_missing_var_to_dotenv(
                key, value, default, filename, line_number
            )

        if value is None and default:
            # Set the variable in os.environ so that subsequent calls return a value.
            os.environ[key] = str(default)
            value = str(default)

        # Register the variable (even if it remains None).
        self._registered_vars[key] = value
        return value

    def setenv(self, key: str, value: str) -> None:
        """Set an environment variable in os.environ and update the registry.(This does not update the .env file.).

        Args:
            key (str): The environment variable key.
            value (str): The value of the environment variable
        """
        os.environ[key] = str(value)

        if self._write_to_dotenv and not self._is_key_in_env_file(key):
            self._append_missing_var_to_dotenv(key, value, "", None, None)
        self._registered_vars[key] = str(value)

    def get_all_vars(self) -> dict:
        """Return a copy of all tracked environment variables.

        Returns:
            dict: A copy of all tracked environment variables
        """
        return self._registered_vars.copy()

    def display_env_vars(self) -> None:
        """Print out all registered environment variables in a readable format."""
        print("Registered Environment Variables:")
        for key, value in self._registered_vars.items():
            print(f"  {key}: {value}")
