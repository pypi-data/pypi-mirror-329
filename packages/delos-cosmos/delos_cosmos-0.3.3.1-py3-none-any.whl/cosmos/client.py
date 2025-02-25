"""Client for interacting with the Cosmos API."""

import json
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import IO, Any, Callable, Literal, cast

import requests
from pydantic import BaseModel, PrivateAttr

from .endpoints import Endpoints, RequestMethod
from .exceptions import APIKeyMissingError, InvalidInputError
from .models import ResponseFormat
from .releases import AllReleases
from .settings import VerboseLevel, cosmos_logger

COSMOS_PLATFORM_BACKEND_URL = "https://platform.cosmos-suite.ai"


class APIClient(BaseModel):
    """Base class for API clients."""

    api_key: str
    _server_url: str = PrivateAttr()
    _verbose: VerboseLevel = PrivateAttr()
    _session: requests.Session = PrivateAttr()
    _client_version: Any = PrivateAttr()

    class Config:
        """Configuration for the API Clients."""

        arbitrary_types_allowed = True

    def __init__(
        self: "APIClient",
        api_key: str,
        server_url: str = COSMOS_PLATFORM_BACKEND_URL,
        verbose: VerboseLevel = VerboseLevel.INFO,
    ) -> None:
        """Initialize the client with the server URL and API key.

        Args:
            api_key: The API key to be used for requests.
            server_url: The URL of the server.
            verbose: The verbosity level of the client.
                0 - No logging
                1 - Only print the requests (default)
                2 - Print the requests and the response

        """
        super().__init__(api_key=api_key)
        if not api_key:
            raise APIKeyMissingError

        self._server_url = server_url
        self._verbose = verbose
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        self._client_version = AllReleases[0]

        # Inner client logger
        self._logger_id = f"{__name__}.{id(self)}"
        self._logger = cosmos_logger.bind(client_id=self._logger_id)

        # Disable logger if verbose is NONE
        if self._verbose == VerboseLevel.NONE:
            cosmos_logger.disable(self._logger_id)

    @property
    def server_url(self) -> str:
        """Get the server URL."""
        return self._server_url

    @property
    def verbose(self) -> VerboseLevel:
        """Get the verbosity level."""
        return self._verbose

    def _log(self, message: str, level: int = VerboseLevel.INFO) -> None:
        """Log internal client messages based on verbosity setting.

        Args:
            message: The message to log.
            level: The verbosity level of the message.

        """
        if self._verbose >= level:
            if level == VerboseLevel.DEBUG:
                self._logger.debug(message)
            elif level == VerboseLevel.INFO:
                self._logger.info(message)

    def _build_request(
        self: "APIClient",
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, Callable[..., requests.Response], dict[str, Any]]:
        """Prepare the request by setting up the URL, request function, and request arguments.

        Args:
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            kwargs: Specific keyword arguments to be passed to the request function.

        Returns:
            A tuple containing the URL, request function, and prepared request arguments.

        """
        url = f"{self.server_url}{self._client_version.suffix}{endpoint[0]}"
        request_method = endpoint[1]

        request_func = cast(
            "Callable[..., requests.Response] | None",
            {
                RequestMethod.GET: self._session.get,
                RequestMethod.POST: self._session.post,
                RequestMethod.PUT: self._session.put,
                RequestMethod.DELETE: self._session.delete,
            }.get(request_method),
        )

        if not request_func:
            unsupported_method_error = f"Unsupported HTTP method: {request_method}"
            self._log(unsupported_method_error, level=VerboseLevel.DEBUG)
            raise ValueError(unsupported_method_error)

        files_details = [name for (param, (name, content)) in files] if files else ""
        files_message = f"{len(files)} Files: {files_details}" if files else "No files"

        self._log(f"Request URL: {url}", VerboseLevel.DEBUG)
        self._log(f"Request Method: {request_method}", VerboseLevel.DEBUG)
        self._log(f"Request Data: {data}", VerboseLevel.DEBUG)
        self._log(f"Request Files: {files_message}", VerboseLevel.DEBUG)
        self._log(f"Request Params: {params}", VerboseLevel.DEBUG)

        form_data = {}
        if data:
            form_data.update({k: str(v) if v is not None else "" for k, v in data.items()})

        request_args = {
            "data": form_data,
            "files": files,
            "params": params,
            **kwargs,
        }

        return url, request_func, request_args

    def _make_request(
        self: "APIClient",
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        """Make a request to the specified endpoint with the given data and files.

        Args:
            api_key: The Cosmos key to be used for the request.
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            kwargs: Specific keyword arguments to be passed to the request function.

        Returns:
            The response from the request as a dictionary, or None if an error occurred.

        """
        url, request_func, request_args = self._build_request(endpoint, data, files, params, **kwargs)

        try:
            response = request_func(url, **request_args)
            response.raise_for_status()

            if self.verbose >= VerboseLevel.INFO:
                self._log(f"Response: {response.json()}", VerboseLevel.INFO)
            return response.json()

        except requests.exceptions.RequestException:
            self._logger.exception("Request to %s failed", url)
            raise

    async def _make_streaming_request(
        self: "APIClient",
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str | dict[str, Any], None]:
        """Make a request to the specified streaming endpoint with the given data and files.

        Args:
            api_key: The Cosmos key linked to this client.
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            kwargs: Specific keyword arguments to be passed to the request function.

        Returns:
            The streaming response from the request.

        """
        if endpoint[1] != RequestMethod.POST:
            streaming_error_message = "Streaming is only supported for POST requests."
            self._logger.warning(streaming_error_message)
            raise ValueError(streaming_error_message)

        url, _request_func, request_args = self._build_request(endpoint, data, files, params, **kwargs)

        request_args["stream"] = True

        try:
            response = self._session.post(url, **request_args)
            response.raise_for_status()

            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    yield chunk

            if self._verbose >= VerboseLevel.INFO:
                self._log("Streaming completed", VerboseLevel.INFO)

        except requests.exceptions.RequestException:
            self._logger.exception("Request to %s (streaming) failed", url)
            raise


class CosmosClient(APIClient):
    """Client for interacting with the Cosmos API.

    Attributes:
        server_url: The URL of the server.
        api_key: The API key to be used for requests.

    """

    def __init__(
        self,
        api_key: str,
        server_url: str = COSMOS_PLATFORM_BACKEND_URL,
        verbose: VerboseLevel = VerboseLevel.INFO,
    ) -> None:
        """Initialize the CosmosClient.

        Args:
            api_key: The Cosmos key linked to this client.
            server_url: The URL of the server.
            verbose: The verbosity level of the client.

        """
        super().__init__(api_key=api_key, server_url=server_url, verbose=verbose)

    def status_health(
        self: "CosmosClient",
    ) -> dict[str, Any] | None:
        """Make a request to check the health of the server."""
        return self._make_request(Endpoints.STATUS.HEALTH.value)

    def translate_text(
        self: "CosmosClient",
        text: str,
        output_language: str,
        input_language: str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to translate text.

        Args:
            text: The text to be translated.
            output_language: The output language for the translation.
            input_language: The input language for the translation (Optional).

        Returns:
            The server response.

        """
        data = {
            "text": text,
            "output_language": output_language,
        }
        if input_language:
            data["input_language"] = input_language
        return self._make_request(endpoint=Endpoints.TRANSLATE.TRANSLATE_TEXT.value, data=data)

    def translate_file(
        self: "CosmosClient",
        filepath: Path | str,
        output_language: str,
        input_language: str | None = None,
        return_type: Literal["raw_text", "url", "file"] = "raw_text",
    ) -> dict[str, Any] | None:
        """Make a request to translate a file.

        Args:
            filepath: The file path to be translated.
            output_language: The output language for the translation.
            input_language: The input language for the translation (Optional).
            return_type: The type of return for the translation (Optional). Default is "raw_text".

        Returns:
            The server response.

        """
        data = {
            "output_language": output_language,
            "return_type": return_type,
        }
        if input_language:
            data["input_language"] = input_language

        file_path = Path(filepath) if isinstance(filepath, str) else filepath
        files = [("file", (file_path.name, file_path.open("rb")))]

        return self._make_request(Endpoints.TRANSLATE.TRANSLATE_FILE.value, data=data, files=files)

    def web_search(
        self: "CosmosClient",
        text: str,
        output_language: str | None = None,
        desired_urls: list[str] | str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to perform a search.

        Args:
            text: The text to be searched.
            output_language: The output language for the search (Optional).
            desired_urls: The desired URLs to be priviledged in the search (Optional).

        Returns:
            The server response.

        """
        data = {"text": text}
        if output_language:
            data["output_language"] = output_language
        if desired_urls:
            data["desired_urls"] = str(desired_urls)

        return self._make_request(Endpoints.WEB.SEARCH.value, data)

    def llm_chat(
        self: "CosmosClient",
        text: str,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        """Make a request to chat with the LLM.

        Args:
            text: The text to be chatted.
            messages: The history of the conversation (Optional. Default is None).
            model: The model to be used for chatting.
            temperature: The temperature for the chat (Optional. Default is 0.7).
            response_format: The response format for the chat (Optional).
                For example: `response_format = {"type":"json_object"}`
            kwargs: Other specific keyword arguments to be passed to the request function.

        Returns:
            The server response.

        """
        data = {"text": text, "model": model}
        if messages is not None:
            data["messages"] = str(messages)
        if response_format is not None:
            if isinstance(response_format, str):
                self._logger.warning(
                    "The parameter `response_format:str`, soon will be deprecated. "
                    "Use instead `response_format:dict[str,Any]` which must contain a `type` key.",
                )
                data["response_format"] = response_format

            else:
                parsed_format = json.dumps(response_format)
                data["response_format"] = parsed_format

        if temperature is not None:
            data["temperature"] = str(temperature)

        data.update(kwargs)
        return self._make_request(endpoint=Endpoints.LLM.CHAT.value, data=data)

    async def llm_chat_stream(
        self: "CosmosClient",
        text: str,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str | dict[str, Any], None]:
        """Make a streaming request to chat with the LLM.

        Args:
            text: The text to be chatted.
            model: The model to be used for chatting.
            messages: The history of the conversation (Optional. Default is None).
            temperature: The temperature for the chat (Optional. Default is 0.7).
            response_format: The response format for the chat (Optional).
                For example: `response_format = {"type":"json_object"}`
            kwargs: Other specific keyword arguments to be passed to the request function.

        Returns:
            The server response.

        """
        data = {"text": text, "model": model}
        if messages is not None:
            data["messages"] = str(messages)

        if response_format is not None:
            if isinstance(response_format, str):
                self._logger.warning(
                    "The parameter `response_format:str`, soon will be deprecated. "
                    "Use instead `response_format:dict[str,Any]` which must contain a `type` key.",
                )
                data["response_format"] = response_format
            else:
                data["response_format"] = str(response_format)

        if temperature is not None:
            data["temperature"] = str(temperature)

        data.update(kwargs)
        async for chunk in self._make_streaming_request(endpoint=Endpoints.LLM.CHAT_STREAM.value, data=data):
            yield chunk

    def llm_embed(
        self: "CosmosClient",
        text: str,
        model: str,
    ) -> dict[str, Any] | None:
        """Make a request to embed data using the LLM.

        Args:
            text: The text to be embedded.
            model: The model to use for embedding.

        Returns:
            The server response.

        """
        return self._make_request(Endpoints.LLM.EMBED.value, data={"text": text, "model": model})

    def files_parse(
        self: "CosmosClient",
        filepath: Path,
        extract_type: Literal["subchunks", "chunks", "pages", "file"] = "chunks",
        read_images: bool = False,
        k_min: int | None = None,
        k_max: int | None = None,
        overlap: int | None = None,
        filter_pages: str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to chunk a file.

        Args:
            filepath: The file path to be chunked.
            extract_type: The type of extraction to be performed (Optional). Default is "chunks".
            read_images: Whether to read images from the files (Optional). Default is False.
            k_min: The minimum number of chunks to be extracted (Optional). Default is 500 tokens.
            k_max: The maximum number of chunks to be extracted (Optional). Default is 1000 tokens.
            overlap: The overlap between chunks (Optional). Default is 10 tokens.
            filter_pages: The filter for pages (Optional). Default is all pages.

        Returns:
            The server response.

        """
        files = [("file", (filepath.name, filepath.open("rb")))]
        data = {
            "extract_type": extract_type,
            "read_images": read_images,
            "k_min": k_min,
            "k_max": k_max,
            "overlap": overlap,
            "filter_pages": filter_pages,
        }
        return self._make_request(Endpoints.FILES.PARSER.value, data=data, files=files)

    def files_index_create(
        self: "CosmosClient",
        name: str,
        read_images: bool = False,
        filepaths: list[Path] | list[str] | None = None,
        filesobjects: list[tuple[str, tuple[str, IO[bytes]]]] | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to create an index.

        Args:
            name: The name of the index.
            read_images: Whether to read images from the files (Optional). Default is False.
            filepaths: A list of file paths to be indexed. Provide either filepaths or filesobjects, not both.
            filesobjects: A list of file objects to be indexed.

        Returns:
            The server response.

        """
        if not filepaths and not filesobjects:
            error_message = "Either filepaths or filesobjects must be provided."
            raise InvalidInputError(error_message)

        if filepaths and filesobjects:
            error_message = "Provide either filepaths or filesobjects, not both."
            raise InvalidInputError(error_message)

        files = []
        if filepaths:
            for fp in filepaths:
                path = Path(fp) if isinstance(fp, str) else fp
                with path.open("rb") as file:
                    files.append(("files", (path.name, file.read())))
        elif filesobjects:
            for _, (filename, file_object) in filesobjects:
                files.append(("files", (filename, file_object.read())))

        return self._make_request(
            Endpoints.FILES.INDEX_CREATE.value,
            data={"name": name, "read_images": read_images},
            files=files,
        )

    def files_index_files_add(
        self: "CosmosClient",
        index_uuid: str,
        read_images: bool = False,
        filepaths: list[Path] | list[str] | None = None,
        filesobjects: list[tuple[str, tuple[str, IO[bytes]]]] | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to add files to an index.

        Args:
            index_uuid: The index UUID.
            read_images: Whether to read images from the files (Optional). Default is False.
            filepaths: A list of file paths to be added to the index.
                        Provide either filepaths or filesobjects, not both.
            filesobjects: A list of file objects to be indexed.

        Returns:
            The server response.

        """
        if not filepaths and not filesobjects:
            error_message = "Either filepaths or filesobjects must be provided."
            raise InvalidInputError(error_message)

        if filepaths and filesobjects:
            error_message = "Provide either filepaths or filesobjects, not both."
            raise InvalidInputError(error_message)

        files = []
        if filepaths:
            for fp in filepaths:
                path = Path(fp) if isinstance(fp, str) else fp
                with path.open("rb") as file:
                    files.append(("files", (path.name, file.read())))
        elif filesobjects:
            for _, (filename, file_object) in filesobjects:
                files.append(("files", (filename, file_object.read())))

        return self._make_request(
            Endpoints.FILES.INDEX_ADD_FILES.value,
            data={"index_uuid": index_uuid, "read_images": read_images},
            files=files,
        )

    def files_index_files_delete(
        self: "CosmosClient",
        index_uuid: str,
        files_hashes: list[str],
    ) -> dict[str, Any] | None:
        """Make a request to delete files from an index.

        Args:
            index_uuid: The index UUID.
            files_hashes: A list of file hashes to be deleted from the index.

        Returns:
            The server response.

        """
        debug_message = (
            f"{len(files_hashes)} Files to be deleted: {files_hashes} (type {type(files_hashes)} "
            f"- first item:{files_hashes[0]} ({type(files_hashes[0])}))"
        )
        self._logger.warning(debug_message)
        files_hashes_str = [str(file_hash) for file_hash in files_hashes]
        data = {"index_uuid": index_uuid, "files_hashes": files_hashes_str}
        return self._make_request(Endpoints.FILES.INDEX_DELETE_FILES.value, data=data)

    def files_index_delete(self: "CosmosClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to delete an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_DELETE.value, data=data)

    def files_index_restore(self: "CosmosClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to restore an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_RESTORE.value, data=data)

    def files_index_rename(
        self: "CosmosClient",
        index_uuid: str,
        name: str,
    ) -> dict[str, Any] | None:
        """Make a request to rename an index.

        Args:
            index_uuid: The index UUID.
            name: The new name for the index.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid, "name": name}
        return self._make_request(Endpoints.FILES.INDEX_RENAME.value, data=data)

    def files_index_ask(
        self: "CosmosClient",
        index_uuid: str,
        question: str,
        output_language: str | None = None,
        active_files: list[str] | str = "all",
    ) -> dict[str, Any] | None:
        """Make a request to ask a question about the index contents.

        Args:
            index_uuid: The index UUID.
            question: The question to be asked.
            output_language: The output language for the question.
            active_files: The hashes of the files to be used for the question. Or "all" (default) or "none".

        Returns:
            The server response.

        """
        data = {
            "index_uuid": str(index_uuid),
            "question": question,
            "active_files": json.dumps(active_files) if isinstance(active_files, list) else active_files,
        }
        if output_language:
            data["output_language"] = output_language

        return self._make_request(Endpoints.FILES.INDEX_ASK.value, data=data)

    def files_index_embed(self: "CosmosClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to embed an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_EMBED.value, data=data)

    def files_index_details(self: "CosmosClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to get details of an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        params = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_DETAILS.value, params=params)

    def files_index_list(self: "CosmosClient") -> dict[str, Any] | None:
        """Make a request to list all indexes."""
        return self._make_request(Endpoints.FILES.INDEX_LIST.value)
