import time
import uuid
import httpx
import os
from typing import (Optional, Dict, Union, List)
from pydantic import (BaseModel, validator, Field)
from .errors import InfuzuAPIError


class ModelWeights(BaseModel):
    price: Optional[float] = None
    error: Optional[float] = None
    start_latency: Optional[float] = None
    end_latency: Optional[float] = None

    class Config:
        extra: str = "allow"


class InfuzuModelParams(BaseModel):
    llms: Optional[List[str]] = None
    exclude_llms: Optional[List[str]] = None
    weights: Optional[ModelWeights] = None
    imsn: Optional[int] = None
    max_input_cost: Optional[float] = None
    max_output_cost: Optional[float] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsRequestContentPart(BaseModel):
    type: str
    text: Optional[str] = None
    image_url: Optional[str] = None
    input_audio: Optional[str] = None

    class Config:
        extra: str = "allow"

    @validator("text", always=True)
    def check_content_fields(cls, value, values):
        if "type" in values:
            content_type = values["type"]
            if content_type == "text" and value is None:
                raise ValueError("Text must be provided when type is 'text'")
            if content_type != "text" and value is not None:
                raise ValueError("Text cannot be provided when type is not 'text'")
        return value


class ChatCompletionsHandlerRequestMessage(BaseModel):
    content: Union[str, List[ChatCompletionsRequestContentPart]]
    role: str
    name: Optional[str] = None

    class Config:
        extra: str = "allow"

    @validator('role')
    def role_must_be_valid(cls, v):
        if v not in ('system', 'user', 'assistant'):
            raise ValueError('Role must be one of: system, user, assistant')
        return v


class ChatCompletionsChoiceMessageAudioObject(BaseModel):
    id: Optional[str] = None
    expired_at: Optional[int] = None
    data: Optional[str] = None
    transcript: Optional[str] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceMessageFunctionCallObject(BaseModel):
    name: Optional[str] = None
    arguments: Optional[str] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceMessageToolCallFunctionObject(BaseModel):
    name: Optional[str] = None
    arguments: Optional[str] = None

    class Config:
        extra: str = "allow"


class chatCompletionsChoiceMessageToolCallObject(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    function: Optional[ChatCompletionsChoiceMessageToolCallFunctionObject] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceMessageObject(BaseModel):
    content: Optional[str] = None
    refusal: Optional[str] = None
    tool_calls: Optional[List[chatCompletionsChoiceMessageToolCallObject]] = None
    role: Optional[str] = None
    function_call: Optional[ChatCompletionsChoiceMessageFunctionCallObject] = None
    audio: Optional[ChatCompletionsChoiceMessageAudioObject] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceLogprobsItemTopLogprobObject(BaseModel):
    token: Optional[str] = None
    logprob: Optional[int] = None
    bytes: Optional[List[int]] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsLogprobsItemObject(BaseModel):
    token: Optional[str] = None
    logprob: Optional[int] = None
    bytes: Optional[List[int]] = None
    content: Optional[List[ChatCompletionsChoiceLogprobsItemTopLogprobObject]] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceLogprobsObject(BaseModel):
    content: Optional[List[ChatCompletionsLogprobsItemObject]] = None
    refusal: Optional[List[ChatCompletionsLogprobsItemObject]] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceModelObject(BaseModel):
    ref: Optional[str] = None
    rank: Optional[int] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceErrorObject(BaseModel):
    message: Optional[str] = None
    code: Optional[str] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceLatencyObject(BaseModel):
    start: Optional[int] = Field(None, alias='start_latency')
    end: Optional[int] = Field(None, alias='end_latency')

    class Config:
        extra: str = "allow"


class ChatCompletionsChoiceObject(BaseModel):
    finish_reason: Optional[str] = None
    index: Optional[int] = None
    message: Optional[ChatCompletionsChoiceMessageObject] = None
    logprobs: Optional[ChatCompletionsChoiceLogprobsObject] = None
    model: Optional[ChatCompletionsChoiceModelObject] = None
    error: Optional[ChatCompletionsChoiceErrorObject] = None
    latency: Optional[ChatCompletionsChoiceLatencyObject] = None

    class Config:
        extra: str = "allow"


class ChatCompletionsObject(BaseModel):
    id: Optional[str] = None
    choices: Optional[List[ChatCompletionsChoiceObject]] = None
    created: Optional[int] = None
    model: Optional[str] = None
    service_tier: Optional[str] = None
    system_fingerprint: Optional[str] = None
    object: Optional[str] = None
    usage: Optional[Dict[str, int]] = None

    class Config:
        extra: str = "allow"


API_BASE_URL = "https://chat.infuzu.com/api"


def create_chat_completion(
        messages: List[ChatCompletionsHandlerRequestMessage],
        api_key: Optional[str] = None,
        model: Optional[Union[str, InfuzuModelParams]] = None,
) -> ChatCompletionsObject:
    """
    Creates a chat completion using the Infuzu API.

    Args:
        messages: A list of message objects.
        api_key: Your Infuzu API key. If not provided, it will be read from the
                 INFUZU_API_KEY environment variable.
        model:  The model to use for the chat completion. Can be a string (model name)
                or a InfuzuModelParams object for more advanced configuration.

    Returns:
        A dictionary containing the JSON response from the API.

    Raises:
        ValueError: If the API key is not provided and the INFUZU_API_KEY
                    environment variable is not set.
        httpx.HTTPStatusError: If the API request returns an error status code.
    """

    if api_key is None:
        api_key = os.environ.get("INFUZU_API_KEY")
        if api_key is None:
            raise ValueError(
                "API key not provided and INFUZU_API_KEY environment variable not set."
            )

    headers = {
        "Content-Type": "application/json",
        "Infuzu-API-Key": api_key,
    }

    payload = {
        "messages": [message.dict(by_alias=True) for message in messages],
    }

    if model:
        if isinstance(model, str):
            payload["model"] = model
        else:
            payload["model"] = model.dict(by_alias=True)

    try:
        with httpx.Client() as client:
            response = client.post(
                f"{API_BASE_URL}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=600
            )

        response.raise_for_status()
        json_response: dict[str, any] = response.json()

        json_response.setdefault('id', f"chatcmpl-{uuid.uuid4()}")
        json_response.setdefault('created', int(time.time()))
        json_response.setdefault('model', 'infuzu-ims')
        json_response.setdefault('object', 'chat.completion')

        return ChatCompletionsObject(**json_response)
    except httpx.HTTPStatusError as e:
        raise InfuzuAPIError(e)
