from collections.abc import Generator
from typing import Any

import requests

def read_streaming_response(response: requests.Response) -> Generator[dict[str, Any], None, None]: ...
def process_streaming_response(response: requests.Response) -> Generator[dict[str, Any], None, None]: ...
