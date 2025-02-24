import os
import aiohttp
from dotenv import load_dotenv
from pathlib import Path
from herd_sdk.main import HerdClient

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


async def setup_test_client() -> HerdClient:
    """Set up a test client with environment variables."""
    token = os.getenv("TEST_TOKEN")
    api_url = os.getenv("HERD_API_URL", "http://localhost:3000")

    # Verify we have a token
    if not token:
        raise ValueError("TEST_TOKEN environment variable is required")

    print("Token:", token)
    print("API URL:", api_url)

    # Validate token against /me endpoint
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{api_url}/api/auth/me", headers={"Authorization": f"Bearer {token}"}
        ) as response:
            # Log the status and body
            print("Status:", response.status)
            body = await response.text()
            print("Body:", body)

            if not response.ok:
                raise ValueError(
                    "Invalid TEST_TOKEN - failed to authenticate with /me endpoint"
                )

    # Create client with validated token
    client = HerdClient(api_url, token)

    # Initialize NATS connection
    await client.initialize()

    return client
