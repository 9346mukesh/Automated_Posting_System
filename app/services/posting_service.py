
import asyncio
import logging

from app.platforms.github import GitHubPlatform
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.discord import DiscordPlatform

from app.schemas import PostingResponse, PlatformResult

logger = logging.getLogger(__name__)


async def publish_on_platform(platform, message: str) -> PlatformResult:
    try:
        result = await platform.post(message)
        return PlatformResult(**result)

    except Exception as exc:
        logger.exception(
            "Publishing failed on %s",
            platform.__class__.__name__
        )

        # Avoid returning sensitive credential information
        error_message = (
            str(exc)
            if not isinstance(exc, Exception)
            else type(exc).__name__
        )

        return PlatformResult(
            platform=platform.platform_name,
            status="failed",
            posted_url=None,
            public_access=False,
            date=None,
            time=None,
            error=error_message
        )


async def publish_message(message: str) -> PostingResponse:

    platforms = [
        GitHubPlatform(),
        BlueskyPlatform(),
        MastodonPlatform(),
        TelegramPlatform(),
        DiscordPlatform()
    ]

    results = await asyncio.gather(
        *[
            publish_on_platform(platform, message)
            for platform in platforms
        ]
    )

    return PostingResponse(
        success=any(
            result.status == "success"
            for result in results
        ),
        results=results
    )
