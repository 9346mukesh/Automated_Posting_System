
from datetime import datetime, timezone

import httpx

from app.config import settings


class BlueskyPlatform:
    platform_name = "Bluesky"
    BASE_URL = "https://bsky.social/xrpc"

    async def post(self, message: str) -> dict:

        if not settings.bluesky_handle or not settings.bluesky_app_password:
            raise ValueError("Bluesky credentials are not configured")

        async with httpx.AsyncClient(timeout=30.0) as client:

            # Authenticate
            auth_response = await client.post(
                f"{self.BASE_URL}/com.atproto.server.createSession",
                json={
                    "identifier": settings.bluesky_handle,
                    "password": settings.bluesky_app_password
                }
            )

            auth_response.raise_for_status()

            session = auth_response.json()
            access_token = session["accessJwt"]
            did = session["did"]

            # Create post
            created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

            post_response = await client.post(
                f"{self.BASE_URL}/com.atproto.repo.createRecord",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                json={
                    "repo": did,
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "$type": "app.bsky.feed.post",
                        "text": message,
                        "createdAt": created_at
                    }
                }
            )

            post_response.raise_for_status()

            data = post_response.json()

        rkey = data["uri"].split("/")[-1]

        posted_url = (
            f"https://bsky.app/profile/{settings.bluesky_handle}/post/{rkey}"
        )

        now = datetime.now(timezone.utc)

        return {
            "platform": "Bluesky",
            "status": "success",
            "posted_url": posted_url,
            "public_access": True,
            "date": now.date(),
            "time": now.time().replace(microsecond=0),
            "error": None
        }
