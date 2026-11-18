
import re
from datetime import date as DateType, time as TimeType
from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator


class PostingRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Message containing exactly one CTA URL"
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        urls = re.findall(r"https?://[^\s]+", value)

        if len(urls) != 1:
            raise ValueError(
                "Message must contain exactly one CTA URL"
            )

        url = urls[0].rstrip(".,!?;:)")

        parsed = urlparse(url)

        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or "." not in parsed.hostname
        ):
            raise ValueError("Please provide a valid HTTP/HTTPS URL")

        return value


class PlatformResult(BaseModel):
    platform: str
    status: Literal["success", "failed"]
    posted_url: str | None = None
    public_access: bool = False
    date: DateType | None = None
    time: TimeType | None = None
    error: str | None = None


class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]
