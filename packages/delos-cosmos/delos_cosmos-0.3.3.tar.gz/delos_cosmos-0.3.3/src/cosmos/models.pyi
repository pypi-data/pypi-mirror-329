from typing import TypedDict

from typing_extensions import TypeAlias

class JSONSchema(TypedDict):
    name: str
    description: str | None
    schema_: dict[str, object] | None
    strict: bool | None

class ResponseFormatJSONSchema(TypedDict):
    json_schema: JSONSchema
    type: str

class ResponseFormatJSONObject(TypedDict):
    type: str

class ResponseFormatText(TypedDict):
    type: str

ResponseFormat: TypeAlias = ResponseFormatText | ResponseFormatJSONObject | ResponseFormatJSONSchema
