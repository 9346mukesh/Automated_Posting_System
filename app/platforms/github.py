
from datetime import datetime, timezone

import httpx

from app.config import settings


class GitHubPlatform:
    platform_name = "GitHub Gist"

    API_URL = "https://api.github.com/gists"

    async def post(self, message: str) -> dict:

        if not settings.github_token:
            raise ValueError("GitHub token is not configured")

        headers = {
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        payload = {
            "description": "Automated Multi-Platform Posting",
            "public": True,
            "files": {
                "business-update.txt": {
                    "content": message
                }
            }
        }

        async with httpx.AsyncClient(timeout=20.0) as client:

            response = await client.post(
                self.API_URL,
                headers=headers,
                json=payload
            )

            response.raise_for_status()

            data = response.json()

        created_at = datetime.now(timezone.utc)

        return {
            "platform": "GitHub Gist",
            "status": "success",
            "posted_url": data.get("html_url"),
            "public_access": data.get("public", False),
            "date": created_at.date(),
            "time": created_at.time().replace(microsecond=0),
            "error": None
        }
