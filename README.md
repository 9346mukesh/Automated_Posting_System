# Automated Multi-Platform Posting System

A Python-based REST API that publishes a single message to multiple social and content platforms simultaneously using their APIs.

Built with **Python 3.11, FastAPI, HTTPX, and Pydantic**.

## Features

- Single REST API endpoint to publish messages across multiple platforms.
- Supports five platform integrations:
  - GitHub Gist
  - Bluesky
  - Mastodon
  - Telegram
  - Discord
- Validates message length (maximum 200 characters).
- Requires exactly one valid HTTP or HTTPS URL in each message.
- Executes platform publishing independently.
- Handles platform-specific errors without interrupting other publishing operations.
- Returns individual publishing results, including status, URL, public accessibility, date, time, and error details.
- Uses environment variables to protect API credentials.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend programming |
| FastAPI | REST API framework |
| HTTPX | Asynchronous HTTP requests |
| Pydantic | Request validation and response models |
| Pydantic Settings | Environment configuration |
| Pytest | Automated testing |

## Project Structure

```text
automated-posting/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   │
│   ├── platforms/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── github.py
│   │   ├── bluesky.py
│   │   ├── mastodon.py
│   │   ├── telegram.py
│   │   └── discord.py
│   │
│   └── services/
│       ├── __init__.py
│       └── posting_service.py
│
├── tests/
│   ├── __init__.py
│   ├── test_posting.py
│   ├── test_github.py
│   ├── test_bluesky.py
│   ├── test_mastodon.py
│   ├── test_telegram.py
│   └── test_discord.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.11 or later
- Git
- API credentials for the supported platforms

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/9346mukesh/Automated_Posting_System.git
cd automated-posting
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your local environment file:

```bash
cp .env.example .env
```

Add your platform credentials to `.env`:

```env
GITHUB_TOKEN=

BLUESKY_HANDLE=
BLUESKY_APP_PASSWORD=

MASTODON_INSTANCE_URL=
MASTODON_ACCESS_TOKEN=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHANNEL_ID=
TELEGRAM_CHANNEL_USERNAME=

DISCORD_WEBHOOK_URL=
```

Replace the empty values with your own credentials.

**Security:** Never commit or share your `.env` file. Keep all API credentials private.

## Platform Configuration

| Platform | Required configuration |
|---|---|
| GitHub Gist | GitHub personal access token with Gist permissions |
| Bluesky | Account handle and app password |
| Mastodon | Instance URL and access token |
| Telegram | Bot token, channel ID, and channel username |
| Discord | Webhook URL |

Ensure the Telegram bot has permission to post messages in the configured channel.

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --port 4000
```

The API will be available at:

```text
http://localhost:4000
```

### API Documentation

FastAPI automatically generates interactive API documentation.

Open:

```text
http://localhost:4000/docs
```

Alternative documentation:

```text
http://localhost:4000/redoc
```

## API Endpoints

### Health Check

**GET** `/health`

Checks whether the application is running.

Example response:

```json
{
  "status": "healthy"
}
```

### Publish Message

**POST** `/posting`

Publishes a message to all configured platforms.

Request:

```json
{
  "message": "Check out my latest project: https://github.com/"
}
```

### Validation Rules

- Message cannot be empty.
- Message must not exceed 200 characters.
- Message must contain exactly one valid HTTP or HTTPS URL.
- Invalid requests return a validation error before publishing begins.

### Example Response

```json
{
  "success": true,
  "results": [
    {
      "platform": "GitHub Gist",
      "status": "success",
      "posted_url": "https://gist.github.com/example",
      "public_access": true,
      "date": "2026-11-18",
      "time": "10:30:00",
      "error": null
    },
    {
      "platform": "Bluesky",
      "status": "success",
      "posted_url": "https://bsky.app/profile/example/post/example",
      "public_access": true,
      "date": "2026-11-18",
      "time": "10:30:00",
      "error": null
    }
  ]
}
```

The response contains an individual result for each configured platform. The example above is illustrative; actual URLs, timestamps, and statuses depend on the publishing results.

## Testing

Run the automated test suite:

```bash
python -m pytest -v
```

The tests cover:

- Valid message submission
- Empty message validation
- Missing URL validation
- Multiple URL validation
- Maximum message length validation
- Independent platform failure handling

The automated tests should mock publishing operations so that running the test suite does not create real public posts.



## Error Handling

Each platform is processed independently.

If one platform fails, the remaining platforms continue publishing.

The response reports the individual status and error information for each platform, allowing clients to identify successful and failed operations.



## Author

**Mukesh Kumar Reddy**

