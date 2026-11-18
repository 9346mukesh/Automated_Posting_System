
from datetime import datetime, timezone

import httpx

from app.config import settings


class MastodonPlatform:
    platform_name = "Mastodon"

    async def post(self, message: str) -> dict:

        if not settings.mastodon_instance_url or not settings.mastodon_access_token:
            raise ValueError("Mastodon credentials are not configured")

        base_url = settings.mastodon_instance_url.rstrip("/")

        headers = {
            "Authorization": f"Bearer {settings.mastodon_access_token}"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.post(
                f"{base_url}/api/v1/statuses",
                headers=headers,
                json={
                    "status": message,
                    "visibility": "public"
                }
            )

            response.raise_for_status()

            data = response.json()

        now = datetime.now(timezone.utc)

        return {
            "platform": "Mastodon",
            "status": "success",
            "posted_url": data.get("url"),
            "public_access": data.get("visibility") == "public",
            "date": now.date(),
            "time": now.time().replace(microsecond=0),
            "error": None
        }
