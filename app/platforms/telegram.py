
from datetime import datetime, timezone

import httpx

from app.config import settings


class TelegramPlatform:
    platform_name = "Telegram"

    async def post(self, message: str) -> dict:

        if not settings.telegram_bot_token:
            raise ValueError("Telegram bot token is not configured")

        if not settings.telegram_channel_id:
            raise ValueError("Telegram channel ID is not configured")

        api_url = (
            f"https://api.telegram.org/bot"
            f"{settings.telegram_bot_token}/sendMessage"
        )

        payload = {
            "chat_id": settings.telegram_channel_id,
            "text": message
        }

        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.post(
                api_url,
                json=payload
            )

            response.raise_for_status()

            data = response.json()

            if not data.get("ok"):
                raise ValueError(data.get("description", "Telegram API error"))

        result = data["result"]
        chat = result["chat"]

        message_id = result["message_id"]
        username = chat.get("username")

        posted_url = (
            f"https://t.me/{username}/{message_id}"
            if username else None
        )

        created_at = datetime.fromtimestamp(
            result["date"],
            tz=timezone.utc
        )

        return {
            "platform": "Telegram",
            "status": "success",
            "posted_url": posted_url,
            "public_access": bool(username and posted_url),
            "date": created_at.date(),
            "time": created_at.time().replace(microsecond=0),
            "error": None
        }
