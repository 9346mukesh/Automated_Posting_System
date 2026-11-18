
import asyncio

from app.platforms.mastodon import MastodonPlatform


async def main():

    mastodon = MastodonPlatform()

    result = await mastodon.post(
        "Check out our latest business platform https://example.com"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
