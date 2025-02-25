import logging
from json import JSONDecodeError
from typing import Optional
import httpx
from pydantic import BaseModel


logger: logging.Logger = logging.getLogger(__name__)


class APIError(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None

    class Config:
        extra: str = "allow"


class APIWarning(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None

    class Config:
        extra: str = "allow"


class InfuzuAPIError(httpx.HTTPStatusError):
    def __init__(self, base_error: httpx.HTTPStatusError) -> None:
        super().__init__(
            f"Infuzu API Error: {base_error}", request=base_error.request, response=base_error.response
        )

        try:
            self.response_json: dict[str, any] = self.response.json()
        except JSONDecodeError as e:
            logger.warning(f"Failed to decode JSON response: {e}")
            self.response_json: dict[str, any] = {}

        self.results: dict[str, any] = self.response_json.get("results", {})

        self.errors: list[APIError] = [APIError(**error) for error in self.response_json.get("errors", [])]

        self.warnings: list[APIWarning] = [APIWarning(**warning) for warning in self.response_json.get("warnings", [])]

    def __str__(self) -> str:
        return f"{super().__str__()} | Errors: {self.errors} | Warnings: {self.warnings} | Results: {self.results}"
