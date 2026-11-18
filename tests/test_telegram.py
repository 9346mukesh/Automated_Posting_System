
import asyncio

from app.platforms.telegram import TelegramPlatform


async def main():

    telegram = TelegramPlatform()

    result = await telegram.post(
        "Check out our latest business platform https://example.com"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
