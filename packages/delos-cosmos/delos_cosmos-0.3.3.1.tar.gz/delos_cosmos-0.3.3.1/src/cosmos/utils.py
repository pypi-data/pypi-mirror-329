"""Utility functions for the Cosmos API client."""

import json
from collections.abc import Generator
from contextlib import suppress
from typing import Any

import requests


def read_streaming_response(response: requests.Response) -> Generator[dict[str, Any], None, None]:
    """Process the streaming response and yield parsed data."""
    for line in response.iter_lines():
        if not line:
            continue

        line_read = line.decode("utf-8")
        if line_read == "data: [DONE]":
            break

        if line_read.startswith("data: "):
            data = line_read[6:]
            with suppress(json.JSONDecodeError):
                yield json.loads(data)

        elif line_read.startswith("0:"):
            yield line_read[2:].strip('"')


def process_streaming_response(response: requests.Response) -> Generator[str, None, None]:
    """Process the streaming response and yield raw data lines."""
    for line in response.iter_lines():
        if line:
            yield line.decode("utf-8")
