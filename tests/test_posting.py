
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import posting_service

client = TestClient(app)


def test_valid_message():
    response = client.post(
        "/posting",
        json={
            "message": "Check out our platform https://example.com"
        }
    )

    assert response.status_code == 200


def test_empty_message():
    response = client.post(
        "/posting",
        json={"message": ""}
    )

    assert response.status_code == 422


def test_message_without_url():
    response = client.post(
        "/posting",
        json={"message": "Check out our business platform"}
    )

    assert response.status_code == 422


def test_message_with_two_urls():
    response = client.post(
        "/posting",
        json={
            "message": "Visit https://example.com and https://google.com"
        }
    )

    assert response.status_code == 422


def test_message_exceeds_200_characters():
    response = client.post(
        "/posting",
        json={
            "message": "A" * 190 + " https://example.com"
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_platform_failure_does_not_stop_others(monkeypatch):

    class FakePlatform:
        def __init__(self, name, should_fail=False):
            self.platform_name = name
            self.should_fail = should_fail

        async def post(self, message):
            if self.should_fail:
                raise RuntimeError("Simulated API failure")

            from datetime import datetime, timezone

            now = datetime.now(timezone.utc)

            return {
                "platform": self.platform_name,
                "status": "success",
                "posted_url": "https://example.com/post/123",
                "public_access": True,
                "date": now.date(),
                "time": now.time().replace(microsecond=0),
                "error": None
            }

    monkeypatch.setattr(
        posting_service,
        "GitHubPlatform",
        lambda: FakePlatform("GitHub Gist")
    )
    monkeypatch.setattr(
        posting_service,
        "BlueskyPlatform",
        lambda: FakePlatform("Bluesky", True)
    )
    monkeypatch.setattr(
        posting_service,
        "MastodonPlatform",
        lambda: FakePlatform("Mastodon")
    )
    monkeypatch.setattr(
        posting_service,
        "TelegramPlatform",
        lambda: FakePlatform("Telegram")
    )
    monkeypatch.setattr(
        posting_service,
        "DiscordPlatform",
        lambda: FakePlatform("Discord")
    )

    result = await posting_service.publish_message(
        "Check out https://example.com"
    )

    assert len(result.results) == 5

    successful = [
        r for r in result.results
        if r.status == "success"
    ]

    failed = [
        r for r in result.results
        if r.status == "failed"
    ]

    assert len(successful) == 4
    assert len(failed) == 1
    assert failed[0].platform == "Bluesky"
