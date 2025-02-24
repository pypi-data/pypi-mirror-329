from collections.abc import AsyncGenerator
from pathlib import Path
from typing import IO, Any, Literal

import requests
from _typeshed import Incomplete
from pydantic import BaseModel

from .endpoints import Endpoints as Endpoints
from .endpoints import RequestMethod as RequestMethod
from .exceptions import APIKeyMissingError as APIKeyMissingError
from .models import ResponseFormat
from .releases import AllReleases as AllReleases
from .settings import VerboseLevel as VerboseLevel
from .settings import cosmos_logger as cosmos_logger

COSMOS_PLATFORM_BACKEND_URL: str

class APIClient(BaseModel):
    api_key: str
    _server_url: str
    _verbose: VerboseLevel
    _session: requests.Session
    _client_version: Any

    class Config:
        arbitrary_types_allowed: bool

    def __init__(
        self,
        api_key: str,
        server_url: str = ...,
        verbose: VerboseLevel = ...,
    ) -> None: ...
    @property
    def server_url(self) -> str: ...
    @property
    def verbose(self) -> VerboseLevel: ...

class CosmosClient:
    api_key: Incomplete
    server_url: Incomplete
    verbose: Incomplete
    session: Incomplete

    def __init__(
        self,
        api_key: str,
        server_url: str | None = ...,
        verbose: VerboseLevel = ...,
    ) -> None: ...
    def status_health(self) -> dict[str, Any] | None: ...
    def translate_text(
        self,
        text: str,
        output_language: str,
        input_language: str | None = None,
    ) -> dict[str, Any] | None: ...
    def translate_file(
        self,
        filepath: Path | str,
        output_language: str,
        input_language: str | None = None,
        return_type: Literal["raw_text", "url", "file"] = "raw_text",
    ) -> dict[str, Any] | None: ...
    def web_search(
        self,
        text: str,
        output_language: str | None = None,
        desired_urls: list[str] | str | None = None,
    ) -> dict[str, Any] | None: ...
    def llm_chat(
        self: CosmosClient,
        text: str,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None: ...
    async def llm_chat_stream(
        self: CosmosClient,
        text: str,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str | dict[str, Any], None]: ...
    def llm_embed(self, text: str, model: str) -> dict[str, Any] | None: ...
    def files_parse(
        self,
        filepath: Path,
        extract_type: Literal["subchunks", "chunks", "pages", "file"] = "chunks",
        read_images: bool = False,
        k_min: int | None = None,
        k_max: int | None = None,
        overlap: int | None = None,
        filter_pages: str | None = None,
    ) -> dict[str, Any] | None: ...
    def files_index_create(
        self,
        name: str,
        read_images: bool = False,
        filepaths: list[Path] | list[str] | None = None,
        filesobjects: list[tuple[str, tuple[str, IO[bytes]]]] | None = None,
    ) -> dict[str, Any] | None: ...
    def files_index_files_add(
        self,
        index_uuid: str,
        read_images: bool = False,
        filepaths: list[Path] | list[str] | None = None,
        filesobjects: list[tuple[str, tuple[str, IO[bytes]]]] | None = None,
    ) -> dict[str, Any] | None: ...
    def files_index_files_delete(self, index_uuid: str, files_hashes: list[str]) -> dict[str, Any] | None: ...
    def files_index_delete(self, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_restore(self, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_rename(self, index_uuid: str, name: str) -> dict[str, Any] | None: ...
    def files_index_ask(
        self,
        index_uuid: str,
        question: str,
        output_language: str | None = None,
        active_files: list[str] | str = "all",
    ) -> dict[str, Any] | None: ...
    def files_index_embed(self, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_details(self, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_list(self) -> dict[str, Any] | None: ...
