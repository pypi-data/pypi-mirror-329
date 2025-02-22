import httpx
import os
from typing import (Optional, Dict, Union, List)
from pydantic import (BaseModel, validator)
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


API_BASE_URL = "https://chat.infuzu.com/api"


def create_chat_completion(
        messages: List[ChatCompletionsHandlerRequestMessage],
        api_key: Optional[str] = None,
        model: Optional[Union[str, InfuzuModelParams]] = None,
) -> Dict:
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
        return response.json()

    except httpx.HTTPStatusError as e:
        raise InfuzuAPIError(e)
