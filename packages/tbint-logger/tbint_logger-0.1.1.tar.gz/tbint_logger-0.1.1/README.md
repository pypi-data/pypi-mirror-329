# TBint Logger Python

`TBIntLogger` is a Python-based logging library designed to simplify
logging messages and data to [Datadog](https://www.datadoghq.com/).

It supports both synchronous and asynchronous logging,
providing flexibility for various application needs.

## Features

- Log messages at different levels: `debug`, `info`, `warn`, `error`.
- Support for both synchronous and asynchronous logging.
- Customizable through environment variables.
- Easy integration with Datadog for centralized logging and monitoring.

## Installation

You can install `tbint-logger` from PyPI:

```sh
pip install tbint-logger
```

## Getting Started

### Environment Variables

Before using `TBIntLogger`, set the following environment variables:

- `DD_SERVICE_NAME`: The name of the service (default: `unknown`).
- `DD_TAGS`: Tags to associate with the logs (or empty).
- `DD_API_ENDPOINT`: The Datadog API endpoint for log ingestion. (default: `https://http-intake.logs.datadoghq.eu/api/v2/logs`)
- `DD_API_KEY`: Your Datadog API key.
- `LOG_LEVEL`: The log level threshold (default: `error`). Possible values: `debug`, `info`, `warn`, `error`.
- `LOG_ENVIRONMENT`: The logging environment (default: `development`, usually this is `production`, `staging` or `development`).

Example `.env` file:

```env
DD_SERVICE_NAME=my-service
DD_SOURCE=production
DD_TAGS=env:production,team:backend
DD_API_ENDPOINT=https://http-intake.logs.datadoghq.eu/api/v2/logs
DD_API_KEY=your-datadog-api-key
LOG_LEVEL=info
```

Load the environment variables using [python-dotenv](https://pypi.org/project/python-dotenv):

### Basic Usage

#### Synchronous Logging

```python
from tbint_logger import Logger, LoggerData

# Init with default values
logger = Logger(
    system="my-system",
    component="auth",
    class_name="AuthService",
    # NOTE:
    # This will obfuscate the context (list or dict) fields
    # recursively, with the character '*'.
    # Matches are case-insensitive.
    # INFO: This is completely optional.
    obfuscate_context_fields=["password", "email", "cc_number", "cvv"],
    obfuscate_context_character="*"
)

# Default values can be overridden
# on each call to the logger
data = LoggerData(
    system="my-system2",
    event="user-login",
    correlation_id="abc123",
    component="auth2",
    class_name="AuthService2",
    method="login",
    description="User successfully logged in",
    duration_ms=120,
    context={
        "user_id": 42,
        "email": "foo@bar.de",
        "password": "secret",
        "cc_number": "1234567890",
        "cvv": "123"
    }
)

logger.info_sync(data)
```

#### Asynchronous Logging

```python
import asyncio
from tbint_logger import Logger, LoggerData

# Init with default values
logger = Logger(
    system="my-system",
    component="auth",
    class_name="AuthService",
)

# Default values can be overridden
# on each call to the logger
data = LoggerData(
    system="my-system2",
    event="user-login",
    correlation_id="abc123",
    component="auth2",
    class_name="AuthService2",
    method="login",
    description="User successfully logged in",
    duration_ms=120,
    context={"user_id": 42}
)

async def log_event():
    await logger.info(data)

asyncio.run(log_event())
```

### Logging Levels

- **Debug**: Use for detailed diagnostic information.
  ```python
  logger.debug_sync(data)
  await logger.debug(data)
  ```

- **Info**: Use for general informational messages.
  ```python
  logger.info_sync(data)
  await logger.info(data)
  ```

- **Warn**: Use for warnings that don't require immediate attention.
  ```python
  logger.warn_sync(data)
  await logger.warn(data)
  ```

- **Error**: Use for errors that require attention.
  ```python
  logger.error_sync(data)
  await logger.error(data)
  ```

## LoggerData Class

The `LoggerData` class is used to structure log messages.
It accepts the following attributes:

| Attribute      | Type   | Description                                       |
|----------------|--------|---------------------------------------------------|
| `system`         | `str`  | The system generating the log.                  |
| `event`          | `str`  | The event type (e.g., "user-login").            |
| `correlation_id` | `str`  | A unique identifier for correlating logs.       |
| `component`      | `str`  | The system component generating the log.        |
| `class_name`     | `str`  | The class name where the log originates.        |
| `method`         | `str`  | The method where the log originates.            |
| `description`    | `str`  | A description of the log event.                 |
| `duration_ms`    | `int`  | Duration of the event in milliseconds.          |
| `context`        | `dict` | Additional context data to include in the log.  |

## How It Works

1. **Environment Configuration**: Reads environment variables for Datadog configuration.
2. **Log Message Construction**: Formats log messages with metadata and timestamp.
3. **Datadog Integration**: Sends logs to Datadog via API.
4. **Sync/Async Options**: Offers both synchronous and asynchronous logging for flexible use cases.

## License

`TBIntLogger` is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Development

```sh
python3 -m venv venv
source venv/bin/activate
rm -rf dist/*
python3 -m pip install -r requirements.txt
python3 -m build
python3 -m twine upload --repository pypi dist/*
```

## Update Requirements

```sh
python3 -m pip freeze > requirements.txt
```
