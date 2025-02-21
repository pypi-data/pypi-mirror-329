from typing import Any

from anthropic.types import (
    Message as AnthropicMessage,
)
from openai.types.chat import (
    ChatCompletionMessage as OpenAIMessage,
)
from pydantic import (
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    SerializationInfo,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
)
from pydantic_core import CoreSchema, core_schema

from .chat.content import Content, ToolResultContent, ToolUseContent


class Message:
    """A class representing a message in a conversation with an LLM.
    
    This class handles messages for both OpenAI and Anthropic formats, providing
    conversion methods between different message formats and validation logic.
    
    Attributes:
        role: The role of the message sender
        content: The content of the message, which can include text and tool interactions
    """

    __slots__ = ("role", "content")


    def __init__(
        self,
        role: Any,
        content: Any,
    ) -> None:
        """Initialize a Message instance.
        
        Args:
            role: The role of the message sender
            content: The content of the message
        """
        object.__setattr__(self, "role", role)
        object.__setattr__(self, "content", content)


    def __str__(self) -> str:
        return f"Message(role={self.role}, content={self.content})"


    def __repr__(self) -> str:
        return f"Message(role={self.role}, content={self.content})"


    def to_openai_input(self) -> dict[str, Any]:
        """Convert the message to OpenAI's expected input format."""
        # OpenAI expects tool calls to be in a separate field in the message
        role = self.role
        content = []
        tool_calls = []
        for content_item in self.content:
            if isinstance(content_item, ToolUseContent):
                tool_calls.append(content_item.to_openai_input())
            elif isinstance(content_item, ToolResultContent):
                return content_item.to_openai_input()
            else:
                content.append(content_item.to_openai_input())
        openai_input = {"role": role,}
        if len(content):
            openai_input["content"] = content 
        if len(tool_calls): 
            openai_input["tool_calls"] = tool_calls

        return openai_input
    

    def to_anthropic_input(self) -> dict[str, Any]:
        """Convert the message to Anthropic's expected input format."""
        return {
            "role": self.role,
            "content": [item.to_anthropic_input() for item in self.content],
        }


    @classmethod
    def validate(cls, value: ValidatorFunctionWrapHandler, _info: dict | ValidationInfo | None = None) -> "Message":
        """Validate and convert inputs into a Message instance."""
        # Don't recurse if we're already dealing with a Message instance
        if isinstance(value, Message):
            return value

        if isinstance(value, OpenAIMessage):
            role = value.role
            tool_calls = value.tool_calls
            # If there are tool calls in the message, for us it will be ToolUseContent
            if tool_calls:
                content = [Content.model_validate(item) for item in tool_calls]
                return cls(role=role, content=content)
            content = value.content
            if not isinstance(content, list):
                content = [content]
            content = [Content.model_validate(item) for item in content]
            return cls(role=role, content=content)
 
        if isinstance(value, AnthropicMessage):
            role = value.role
            content = value.content
            if not isinstance(content, list):
                raise ValueError(f"Invalid content: {content}")
            content = [Content.model_validate(item) for item in content]
            return cls(role=role, content=content)

        if isinstance(value, dict):
            role = value.get("role", None)
            content = value.get("content", None)
            tool_calls = value.get("tool_calls", None)
            # If there are tool calls in the message, for us it will be ToolUseContent
            if tool_calls:
                content = [Content.model_validate(item) for item in tool_calls]
                return cls(role=role, content=content)
            # If the role is "tool", for us it will be a ToolResultContent
            if role == "tool":
                if isinstance(content, list):
                    content_list = content
                else:
                    content_list = [content]
                content = ToolResultContent(
                    id=value.get("tool_call_id"), 
                    content=[Content.model_validate(item) for item in content_list],
                )
                return cls(role="user", content=[content])
            if not isinstance(content, list):
                content = [content]
            content = [Content.model_validate(item) for item in content]
            return cls(role=role, content=content)


    @classmethod
    def serialize(cls, value: Any, _info: dict | SerializationInfo | None = None) -> str:
        """Serialize a Message instance into a dictionary format."""
        # When creating a model with fields with File type that are nullable,
        # pydantic will pass None as the value to File.serialize.
        if value is None:
            return None

        if not isinstance(value, cls):
            raise ValueError("Cannot serialize a non-message object.")

        return {
            "role": value.role,
            "content": value.content,
        }


    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: CoreSchema, _handler: GetJsonSchemaHandler) -> dict[str, Any]:
        """Defines what this type should be in openapi.json."""
        # https://docs.pydantic.dev/2.8/errors/usage_errors/#custom-json-schema
        json_schema = {
            "type": "string",
            "format": "message",
            "description": "An LLM message with role and content",
        }
        return json_schema


    @classmethod
    def __get_pydantic_core_schema__(cls, _source: type[Any], _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Defines how to serialize this type in the core schema."""
        return core_schema.with_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.serialize,
                info_arg=True,
                when_used="always",
            ),
        )
