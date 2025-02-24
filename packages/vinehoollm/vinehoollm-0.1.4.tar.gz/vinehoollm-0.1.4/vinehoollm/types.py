"""
Type definitions for VinehooLLM
"""

from typing import Dict, Optional, Literal, List, Any, Union
from pydantic import BaseModel, Field

class FunctionParameters(BaseModel):
    """
    Represents the parameters object in a function definition
    """
    type: Literal["object"] = Field(
        "object",
        description="The type of the parameters object, must be 'object'"
    )
    properties: Dict[str, Dict[str, Any]] = Field(
        ..., 
        description="Properties of the parameters"
    )
    required: List[str] = Field(
        default_factory=list,
        description="List of required parameter names"
    )
    additionalProperties: bool = Field(
        False,
        description="Whether additional properties are allowed"
    )

class Function(BaseModel):
    """
    Represents the function object in a tool definition
    """
    name: str = Field(..., description="The name of the function")
    description: str = Field(..., description="Description of what the function does")
    parameters: FunctionParameters = Field(..., description="Parameters the function accepts")
    strict: bool = Field(True, description="Whether to enforce strict parameter validation")

class FunctionDefinition(BaseModel):
    """
    Represents a function that can be called by the model
    """
    type: Literal["function"] = Field(
        "function",
        description="The type of the definition, must be 'function'"
    )
    function: Function = Field(..., description="The function definition")

class FunctionCall(BaseModel):
    """
    Represents a function call made by the model
    """
    name: str = Field(..., description="The name of the function to call")
    arguments: str = Field(..., description="The arguments to pass to the function")

class ToolCall(BaseModel):
    """
    Represents a tool call in a message
    """
    id: str = Field(..., description="The ID of the tool call")
    type: Literal["function"] = Field(..., description="The type of the tool call")
    function: FunctionCall = Field(..., description="The function call details")

class ChatMessage(BaseModel):
    """
    Represents a single message in a chat conversation
    """
    role: Literal["system", "user", "assistant", "function", "tool"] = Field(
        ...,
        description="The role of the message sender"
    )
    content: Optional[str] = Field(
        None,
        description="The content of the message"
    )
    function_call: Optional[FunctionCall] = Field(
        None,
        description="Function call information if this message contains a function call"
    )
    name: Optional[str] = Field(
        None,
        description="Name of the function that was called, used when role is 'function'"
    )
    tool_calls: Optional[List[ToolCall]] = Field(
        None,
        description="List of tool calls in the message"
    )
    tool_call_id: Optional[str] = Field(
        None,
        description="ID of the tool call this message is responding to"
    )

class CompletionResponse(BaseModel):
    """
    Response from a completion request
    """
    text: str = Field(
        ...,
        description="The generated text"
    )
    finish_reason: Optional[str] = Field(
        None,
        description="The reason the completion finished"
    )
    usage: Dict[str, int] = Field(
        default_factory=dict,
        description="Token usage statistics"
    )
    function_call: Optional[FunctionCall] = Field(
        None,
        description="The function call made by the model"
    )
    messages: List[ChatMessage] = Field(
        default_factory=list,
        description="List of messages in the completion"
    ) 