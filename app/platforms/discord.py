
from datetime import datetime

import httpx

from app.config import settings


class DiscordPlatform:

    platform_name = "Discord"

    async def post(self, message: str) -> dict:

        if not settings.discord_webhook_url:
            raise ValueError("Discord webhook URL is not configured")

        async with httpx.AsyncClient(timeout=30.0) as client:

            # Publish message
            response = await client.post(
                settings.discord_webhook_url,
                params={"wait": "true"},
                json={"content": message}
            )

            response.raise_for_status()
            data = response.json()

            # Extract message information
            message_id = data.get("id")
            channel_id = data.get("channel_id")
            guild_id = data.get("guild_id")

            if not message_id or not channel_id:
                raise ValueError(
                    "Discord did not return message ID or channel ID"
                )

            # Retrieve webhook metadata if guild ID is missing
            if not guild_id:
                webhook_response = await client.get(
                    settings.discord_webhook_url
                )

                webhook_response.raise_for_status()

                webhook_data = webhook_response.json()
                guild_id = webhook_data.get("guild_id")

            # Construct actual Discord message URL
            posted_url = None

            if guild_id:
                posted_url = (
                    f"https://discord.com/channels/"
                    f"{guild_id}/{channel_id}/{message_id}"
                )

            # Extract actual message creation timestamp
            timestamp = data.get("timestamp")

            if not timestamp:
                raise ValueError(
                    "Discord did not return message timestamp"
                )

            created_at = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )

        return {
            "platform": self.platform_name,
            "status": "success",
            "posted_url": posted_url,
            "public_access": False,
            "date": created_at.date(),
            "time": created_at.time().replace(microsecond=0),
            "error": None
        }
