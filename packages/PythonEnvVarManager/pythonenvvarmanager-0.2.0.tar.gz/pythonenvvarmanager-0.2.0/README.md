# Env Manager

Env Manager is a lightweight Python library designed to simplify the management of environment variables in your application. It provides a convenient way to access, set, and track environment variables while ensuring that any undocumented variables are logged and optionally written to a `.env` file. Additionally, it can overwrite the built-in `os.getenv` function with its own wrapper to offer extended functionality.

---

## Why Use Env Manager?

Managing environment variables can become challenging, especially as applications grow in complexity. Env Manager addresses these challenges by:

- **Tracking Accessed Variables:** It maintains a registry of all environment variables accessed during runtime.
- **Documenting Missing Variables:** When a variable is requested but not set, Env Manager can append a commented-out entry (with a default value and the source location where it was requested) to your `.env` file. This helps in identifying which variables your application relies on.
- **Overriding `os.getenv`:** Optionally, it can override the default `os.getenv` function to ensure that every retrieval of an environment variable goes through the library’s enhanced logic.
- **Ease of Use:** With simple API functions, you can quickly integrate environment variable management into your application without extensive configuration.

---

## Features

- **Singleton Management:** Ensures a single instance of the environment manager throughout the application.
- **Automatic Documentation:** Writes missing or undocumented variables to a specified `.env` file, making it easier to keep track of necessary configurations.
- **Dynamic Overriding:** Optionally replace `os.getenv` with the library’s custom method for consistent behavior across your codebase.
- **Registry of Variables:** Retrieve a copy of all accessed or set environment variables for debugging or logging purposes.
- **Simple API:** Functions like `getenv`, `setenv`, and `display_env_vars` make it easy to integrate into any Python project.

---

## Installation

1. **Clone or Download the Repository:**

   ```bash
   git clone https://github.com/yourusername/env_manager.git
   cd env_manager
   ```

2. **Install Dependencies:**

   Env Manager relies on a few external libraries. You can install them via pip:

   ```bash
   pip install python-dotenv loguru pytest
   ```

3. **Install Env Manager:**

   If you plan to use it as a package, you can install it locally:

   ```bash
   pip install .
   ```

---

## Usage

### Importing the Library

Import Env Manager in your application:

```python
import env_manager as ENV
```

### Retrieving Environment Variables

Use `getenv` to access environment variables. If the variable is not set, you can supply a default value, which will also be logged and optionally written to your `.env` file:

```python
database_url = ENV.getenv("DATABASE_URL", "sqlite:///:memory:")
secret_key = ENV.getenv("SECRET_KEY", "default-secret")
```

### Setting Environment Variables

Set variables programmatically with `setenv`:

```python
ENV.setenv("NEW_VAR", "some_value")
```

### Displaying Tracked Variables

For debugging purposes, you can display all the environment variables that have been accessed or set:

```python
ENV.display_env_vars()
```

### Configuring the `.env` File Path

Change the path to your `.env` file if needed:

```python
ENV.set_dotenv_path(".env.custom")
```

### Controlling File Write Behavior

By default, undocumented environment variables can be written to the `.env` file. To toggle this behavior:

- **Enable Writing to `.env`:**

  ```python
  ENV.set_write_to_dotenv(True)
  ```

- **Disable Writing to `.env`:**

  ```python
  ENV.set_write_to_dotenv(False)
  ```

### Overriding `os.getenv`

To have Env Manager replace `os.getenv` with its enhanced version, set the `OVERWRITE_OS_GETENV` environment variable to `"True"`. This can be done prior to running your application:

```bash
export OVERWRITE_OS_GETENV=True
```

When enabled, every call to `os.getenv` will be intercepted by Env Manager, allowing it to log and manage the environment variable usage accordingly.

---

## Running Tests

Env Manager includes tests using `pytest` to ensure the functionality works as expected. To run the tests, execute:

```bash
pytest
```

These tests cover:
- Retrieving environment variables and using default values.
- Writing missing environment variables to a test `.env` file.
- Behavior when overriding the `os.getenv` function.

---

## License

[MIT License](LICENSE)

---

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/env_manager/issues) if you want to contribute.

---

Env Manager aims to simplify the hassle of environment variable management in Python applications. By providing automatic tracking and documentation, it can significantly improve the clarity and maintainability of your project’s configuration. Enjoy using Env Manager, and happy coding!

