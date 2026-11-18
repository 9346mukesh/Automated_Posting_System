
import asyncio

from app.platforms.github import GitHubPlatform


async def main():
    github = GitHubPlatform()

    result = await github.post(
        "Check out our latest business platform https://example.com"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
