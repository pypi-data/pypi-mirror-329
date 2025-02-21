#!/usr/bin/env python3
"""
mltoolkit_logging.py

This module provides a configurable logger for ML pipelines that works both locally
and in the cloud. It supports structured logging with custom fields using a JSON formatter,
and integrates with Google Cloud Logging when deployed. This helps data scientists build
and run Docker images locally (with console logs) and, when deployed, have logs aggregated
in Google Cloud Logging.

Usage:
    from mltoolkit_logging import setup_logger

    logger = setup_logger("ml-pipeline")
    logger.info(
        "ML Pipeline stage started",
        extra={"environment": "prod", "operating_company": "ExampleCorp", "stage": "data-prep"}
    )
"""

import os
import logging
import json
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler


class CustomJsonFormatter(logging.Formatter):
    """
    Custom JSON Formatter for structured logging.

    This formatter outputs log records as JSON strings, including standard logging fields
    and any extra fields (e.g., 'environment', 'operating_company', 'stage'). It also includes
    a stack trace if an exception is logged.
    """

    def format(self, record):
        """
        Format a log record as a JSON string.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: A JSON-formatted string representing the log record.
        """
        log_data = {
            "message": record.getMessage(),
            "severity": record.levelname,
            "logger": record.name,
            "timestamp": record.created,
        }
        # Include extra fields if provided.
        for key in ("environment", "operating_company", "stage"):
            if key in record.__dict__:
                log_data[key] = record.__dict__[key]
        if record.exc_info:
            log_data["stack_trace"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


def setup_logger(service_name, log_level=logging.INFO, use_cloud: bool = None):
    """
    Configures and returns a logger that either uses Google Cloud Logging or a local stream handler.

    The logger is set up with a custom JSON formatter to output structured logs. It automatically
    determines whether to use Cloud Logging based on the presence of the GOOGLE_CLOUD_PROJECT
    environment variable unless overridden by the use_cloud parameter.

    Args:
        service_name (str): Identifier for the service; this name appears in the log entries.
        log_level (int, optional): Logging level (default: logging.INFO).
        use_cloud (bool, optional): Forces the logger to use Cloud Logging (True) or local logging (False).
            If None, Cloud Logging is used if the environment variable GOOGLE_CLOUD_PROJECT is set.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(log_level)
    logger.handlers = []  # Clear existing handlers

    # Decide if we're using Cloud Logging based on the environment or parameter.
    if use_cloud is None:
        use_cloud = os.environ.get("GOOGLE_CLOUD_PROJECT") is not None

    if use_cloud:
        try:
            client = google.cloud.logging.Client()
            handler = CloudLoggingHandler(client, name=service_name)
        except Exception as e:
            print(f"Error setting up cloud logging: {e}, falling back to local logging.")
            handler = logging.StreamHandler()
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(CustomJsonFormatter())
    logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    """
    Demonstrates the usage of the mltoolkit logging module.

    This demo configures the logger for local testing (by setting use_cloud=False) and logs both
    an informational message and an exception with a stack trace.
    """
    logger = setup_logger("ml-pipeline", use_cloud=False)

    # Log a standard structured message.
    logger.info(
        "ML Pipeline stage started",
        extra={"environment": "dev", "operating_company": "ExampleCorp", "stage": "data-prep"}
    )

    # Simulate an exception to capture a stack trace.
    try:
        1 / 0
    except Exception:
        logger.exception(
            "Error during data processing",
            extra={"environment": "dev", "operating_company": "ExampleCorp", "stage": "data-processing"}
        )

    print("Logging demo complete. Check your logs locally or in Cloud Logging if deployed.")
