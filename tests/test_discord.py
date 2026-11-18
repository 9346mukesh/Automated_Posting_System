
import asyncio

from app.platforms.discord import DiscordPlatform


async def main():

    discord = DiscordPlatform()

    result = await discord.post(
        "Check out our latest business platform https://example.com"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
