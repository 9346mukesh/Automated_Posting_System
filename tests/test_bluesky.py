
import asyncio

from app.platforms.bluesky import BlueskyPlatform


async def main():

    bluesky = BlueskyPlatform()

    result = await bluesky.post(
        "Check out our latest business platform https://example.com"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
