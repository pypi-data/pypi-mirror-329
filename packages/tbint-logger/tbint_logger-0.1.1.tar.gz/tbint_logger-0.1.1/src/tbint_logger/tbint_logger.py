"""
TBIntLogger

This service is used to log messages and data to Datadog.
"""

import os
import time
from typing import List, Optional

import aiohttp
import pkg_resources
import requests
from dotenv import load_dotenv

load_dotenv()

__version__ = pkg_resources.get_distribution("tbint-logger").version


# pylint: disable=too-few-public-methods too-many-instance-attributes
class LoggerData:
    """
    Data class for TBIntLogger
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        system=None,
        event=None,
        correlation_id=None,
        component=None,
        class_name=None,
        method=None,
        description=None,
        duration_ms=None,
        context=None,
    ):
        self.system = system
        self.event = event
        self.correlation_id = correlation_id
        self.component = component
        self.class_name = class_name
        self.method = method
        self.description = description
        self.duration_ms = duration_ms
        self.context = context

    def to_dict(self):
        """
        Convert the data to a dictionary
        """

        return {
            "system": self.system,
            "event": self.event,
            "correlation_id": self.correlation_id,
            "component": self.component,
            "class_name": self.class_name,
            "method": self.method,
            "description": self.description,
            "duration_ms": self.duration_ms,
            "context": self.context,
        }


class Logger:
    """
    Logging service

    This service is used to log messages and data to Datadog.
    """

    LOG_LEVELS = {"debug": 10, "info": 20, "warn": 30, "error": 40}

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(
        self,
        service: Optional[str] = None,
        system: Optional[str] = None,
        component: Optional[str] = None,
        obfuscate_context_fields: Optional[List[str]] = None,
        obfuscate_context_character="*",
        class_name: Optional[str] = None,
    ):
        self.dd_service_name: str = service or os.getenv("DD_SERVICE_NAME", "unknown")
        self.dd_source: str = f"tbint-logger-py/{__version__}"
        self.dd_tags: str = os.getenv("DD_TAGS", "")
        self.dd_api_endpoint: str = os.getenv(
            "DD_API_ENDPOINT", "https://http-intake.logs.datadoghq.eu/v2/logs"
        )
        self.dd_api_key: str = os.getenv("DD_API_KEY", "")
        self.log_level = os.getenv("LOG_LEVEL", "error").lower()
        self.log_environment = os.getenv("LOG_ENVIRONMENT", "development")
        self.system = system
        self.component = component
        self.class_name = class_name
        self.obfuscate_context_fields = {
            field.lower() for field in (obfuscate_context_fields or [])
        }
        self.obfuscate_context_character = obfuscate_context_character

        if self.log_level not in self.LOG_LEVELS:
            raise ValueError(
                f"""Invalid LOG_LEVEL: {self.log_level}.
                Must be one of {list(self.LOG_LEVELS.keys())}."""
            )

    def obfuscate_context(self, context):
        """
        Recursively obfuscate matching fields in the context.
        """
        if isinstance(context, dict):
            return {
                key: (
                    self.obfuscate_context(value)
                    if key.lower() not in self.obfuscate_context_fields
                    else self.obfuscate_context_character * len(str(value))
                )
                for key, value in context.items()
            }
        if isinstance(context, list):
            return [self.obfuscate_context(item) for item in context]
        return context

    def __request_sync(self, headers, log_message):
        if self.dd_api_endpoint != "" and self.dd_api_key != "":
            response = requests.post(
                url=self.dd_api_endpoint, json=log_message, headers=headers, timeout=5
            )
            if not str(response.status_code).startswith("2"):
                log_res = response.json()
                print(
                    f"Error logging: {response.status_code} {response.reason} {log_res}"
                )

    async def __request_async(self, headers, log_message):
        if self.dd_api_endpoint != "" and self.dd_api_key != "":
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self.dd_api_endpoint,
                    json=log_message,
                    headers=headers,
                    timeout=5,
                ) as response:
                    if not str(response.status).startswith("2"):
                        log_res = await response.json()
                        print(
                            f"Error logging: {response.status} {response.reason} {log_res}"
                        )

    def get_headers(self):
        """
        Get headers for the request

        Simple helper function to get the headers for the request
        """

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "DD-API-KEY": self.dd_api_key,
        }

    def get_log_message(self, level, d: LoggerData):
        """
        Get log message

        Simple helper function to get the log message formatted for Datadog
        """

        data = d.to_dict()

        # Fallback to the class attributes if not provided in the data
        system = (
            self.system if not data.get("system", None) else data.get("system", None)
        )
        component = (
            self.component
            if not data.get("component", None)
            else data.get("component", None)
        )
        class_name = (
            self.class_name
            if not data.get("class_name", None)
            else data.get("class_name", None)
        )

        obfuscated_context = self.obfuscate_context(data.get("context", {}))

        return {
            "service": self.dd_service_name,
            "ddsource": self.dd_source,
            "ddtags": self.dd_tags,
            "level": level,
            "message": {
                "message": {
                    # ISO 8601 timestamp
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "env": self.log_environment,
                    "system": system,
                    "event": data.get("event", None),
                    "correlation_id": data.get("correlation_id", None),
                    "component": component,
                    "class": class_name,
                    "method": data.get("method", None),
                    "description": data.get("description", None),
                    "duration_ms": data.get("duration_ms", None),
                    "context": obfuscated_context,
                }
            },
        }

    async def __log_async(self, level, data):
        if self.should_log(level):
            headers = self.get_headers()
            log_message = self.get_log_message(level, data)
            print(log_message)
            await self.__request_async(headers, log_message)

    def __log_sync(self, level, data):
        if self.should_log(level):
            headers = self.get_headers()
            log_message = self.get_log_message(level, data)
            print(log_message)
            self.__request_sync(headers, log_message)

    def should_log(self, level):
        """
        Check if the message should be logged based on the log level.
        """
        return self.LOG_LEVELS[level] >= self.LOG_LEVELS[self.log_level]

    async def debug(self, data: LoggerData):
        """
        Logs a message and data (debug level) asynchronously
        """
        await self.__log_async("debug", data)

    async def info(self, data: LoggerData):
        """
        Logs a message and data (info level) asynchronously
        """
        await self.__log_async("info", data)

    async def warn(self, data: LoggerData):
        """
        Logs a message and data (warn level) asynchronously
        """
        await self.__log_async("warn", data)

    async def error(self, data: LoggerData):
        """
        Logs a message and data (error level) asynchronously
        """
        await self.__log_async("error", data)

    def debug_sync(self, data: LoggerData):
        """
        Logs a message and data (debug level) synchronously
        """
        self.__log_sync("debug", data)

    def info_sync(self, data: LoggerData):
        """
        Logs a message and data (info level) synchronously
        """
        self.__log_sync("info", data)

    def warn_sync(self, data: LoggerData):
        """
        Logs a message and data (warn level) synchronously
        """
        self.__log_sync("warn", data)

    def error_sync(self, data: LoggerData):
        """
        Logs a message and data (error level) synchronously
        """
        self.__log_sync("error", data)
