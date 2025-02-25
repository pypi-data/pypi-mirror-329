"""Models for the Cosmos client."""

from typing import Literal, Required, TypedDict

from typing_extensions import TypeAlias


class JSONSchema(TypedDict):
    """JSON Schema for the response format.

    Attributes:
        name: The name of the response format.
            Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64 characters.

        description: A description of what the response format is for,
            used by the model to determine how to respond in the format.

        schema: The schema for the response format, described as a JSON Schema object.

        strict: Whether to enable strict schema adherence when generating the output.
            If set to true, the model will always follow the exact schema defined in the `schema` field.
            Only a subset of JSON Schema is supported when `strict` is `true`.

        type: The type of response format being defined: `json_schema`

    """

    name: str
    description: str | None
    schema_: dict[str, object] | None
    strict: bool | None


class ResponseFormatJSONSchema(TypedDict):
    """Response format through a JSON Schema.

    Attributes:
        type: The type of response format being defined: `json_schema`

    """

    json_schema: JSONSchema
    type: Literal["json_schema"]


class ResponseFormatJSONObject(TypedDict):
    """Response format through a JSON Object.

    Attributes:
        type: The type of response format being defined: `json_object`

    """

    type: Required[Literal["json_object"]]


class ResponseFormatText(TypedDict):
    """Response format as text.

    Attributes:
        type: The type of response format being defined: `text`

    """

    type: Required[Literal["text"]]


ResponseFormat: TypeAlias = ResponseFormatText | ResponseFormatJSONObject | ResponseFormatJSONSchema
