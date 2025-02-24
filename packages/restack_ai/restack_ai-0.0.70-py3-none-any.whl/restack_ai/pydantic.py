from __future__ import annotations

import json
from typing import Any

from pydantic_core import to_jsonable_python
from temporalio.api.common.v1 import Payload
from temporalio.converter import (
    CompositePayloadConverter,
    DataConverter,
    DefaultPayloadConverter,
    JSONPlainPayloadConverter,
)

from .observability import log_with_context


class PydanticJSONPayloadConverter(JSONPlainPayloadConverter):
    """Pydantic JSON payload converter.

    This extends the :py:class:`JSONPlainPayloadConverter` to override
    :py:meth:`to_payload` using the Pydantic encoder.
    """

    def to_payload(self, value: Any) -> Payload | None:
        """Convert values with Pydantic encoder, fallback to default if fails."""
        try:
            # Attempt to convert using Pydantic
            return Payload(
                metadata={"encoding": self.encoding.encode()},
                data=json.dumps(
                    value,
                    separators=(",", ":"),
                    sort_keys=True,
                    default=to_jsonable_python,
                ).encode(),
            )
        except (TypeError, ValueError):
            # Fallback to default JSON conversion
            return super().to_payload(value)

    def from_payload(self, payload: Payload, type_hint: Any | None = None) -> Any:
        """Convert payload back to Python value."""
        try:
            value = super().from_payload(payload, type_hint)
            # If type_hint expects a string but we got a dict, convert dict to string
            if type_hint is str and isinstance(value, dict):
                return json.dumps(value)
        except Exception as e:
            log_with_context("ERROR", "Error parsing payload", error=str(e))
            raise
        else:
            return value


class PydanticPayloadConverter(CompositePayloadConverter):
    """Payload converter that replaces Temporal JSON conversion with Pydantic.

    JSON conversion is handled using Pydantic's serialization model.
    """

    def __init__(self) -> None:
        super().__init__(
            *(
                c
                if not isinstance(c, JSONPlainPayloadConverter)
                else PydanticJSONPayloadConverter()
                for c in DefaultPayloadConverter.default_encoding_payload_converters
            ),
        )


pydantic_data_converter = DataConverter(
    payload_converter_class=PydanticPayloadConverter,
)
"""Data converter using Pydantic JSON conversion."""
