import pytest
import asyncio
import pytest_asyncio
from herd_sdk.main import HerdClient
from .setup import setup_test_client


@pytest_asyncio.fixture
async def client():
    """Fixture to provide a test client."""
    client = await setup_test_client()
    try:
        yield client
    finally:
        await client.close()


async def get_connected_device(client: HerdClient):
    """Get the first connected device."""
    devices = await client.list_devices()
    assert devices, "No devices available"
    print("Available devices:", [(d.device_id, d.status) for d in devices])

    # Find an online device
    online_devices = [d for d in devices if d.status == "online"]
    assert online_devices, "No online devices available"

    device = online_devices[0]
    assert device is not None, "Failed to get device"
    return device


async def twitter_login(page):
    """Helper function to login to Twitter."""
    await page.goto(
        "https://twitter.com/login", options={"waitForNavigation": "networkidle2"}
    )
    await page.type('input[autocomplete="username"]', TWITTER_USERNAME)
    await page.click("#layers button:nth-child(6)")
    await asyncio.sleep(1)
    await page.type('input[autocomplete="current-password"]', TWITTER_PASSWORD)
    await page.click('#layers button[type="submit"]')
    await asyncio.sleep(DEFAULT_WAIT_TIME)

    # Verify login successful
    profile_button = await page.find('[data-testid="AppTabBar_Profile_Link"]')
    assert profile_button, "Login failed - profile button not found"


async def twitter_logout(page):
    """Helper function to logout from Twitter."""
    await page.click('[data-testid="AppTabBar_More_Menu"]')
    await asyncio.sleep(1)
    await page.click('[data-testid="logout"]')
    await asyncio.sleep(1)
    await page.click('[data-testid="confirmationSheetConfirm"]')
    await asyncio.sleep(DEFAULT_WAIT_TIME)

    # Verify logout successful
    login_button = await page.find('[data-testid="loginButton"]')
    assert login_button, "Logout failed - login button not found"


@pytest.mark.asyncio
async def test_twitter_login_logout(client: HerdClient):
    """Test Twitter login and logout."""
    device = await get_connected_device(client)
    page = await device.new_page()
    assert page is not None, "Failed to create new page"

    # await twitter_login(page)
    # await twitter_logout(page)
    await page.close()


@pytest.mark.asyncio
async def test_twitter_search_results(client: HerdClient):
    """Test extracting Twitter search results across different tabs."""
    device = await get_connected_device(client)
    page = await device.new_page()
    assert page is not None, "Failed to create new page"

    # await twitter_login(page)

    # Navigate to Twitter search
    await page.goto(
        f"https://twitter.com/search?q={TEST_SEARCH_TERM}",
        options={"waitForNavigation": "networkidle2"},
    )

    # Dictionary to store results from each tab
    search_results = {}

    for tab in SEARCH_TABS:
        # Click the tab
        await page.click(f'[role="tab"][aria-label="{tab}"]')
        await asyncio.sleep(DEFAULT_WAIT_TIME)  # Wait for content to load

        # Extract tweets/content from the tab
        results = await page.extract(
            {
                "_$r": '[data-testid="tweet"]',
                "text": '[data-testid="tweetText"]',
                "username": '[data-testid="User-Name"]',
                "timestamp": "time",
            }
        )

        search_results[tab.lower()] = results

    assert search_results, "Failed to extract search results"
    assert all(
        len(results) > 0 for results in search_results.values()
    ), "Some tabs had no results"

    # await twitter_logout(page)
    await page.close()


@pytest.mark.asyncio
async def test_twitter_profile_extraction(client: HerdClient):
    """Test extracting profile information and relationships."""
    device = await get_connected_device(client)
    page = await device.new_page()

    # await twitter_login(page)

    # Navigate to a Twitter profile
    await page.goto(
        f"https://twitter.com/{TEST_PROFILE}",
        options={"waitForNavigation": "networkidle2"},
    )

    # Extract profile information
    profile_info = await page.extract(
        {
            "name": '[data-testid="UserName"]',
            "bio": '[data-testid="UserDescription"]',
            "location": '[data-testid="UserLocation"]',
            "website": '[data-testid="UserUrl"]',
            "following_count": '[data-testid="following_count"]',
            "followers_count": '[data-testid="followers_count"]',
        }
    )

    assert profile_info, "Failed to extract profile information"

    # Extract recent tweets
    tweets = await page.extract(
        {
            "_$r": '[data-testid="tweet"]',
            "text": '[data-testid="tweetText"]',
            "replies": '[data-testid="reply"]',
            "retweets": '[data-testid="retweet"]',
            "likes": '[data-testid="like"]',
        }
    )

    assert tweets, "Failed to extract tweets"

    # Click followers button and extract some followers
    await page.click('[data-testid="followers"]')
    await asyncio.sleep(DEFAULT_WAIT_TIME)

    followers = await page.extract(
        {
            "_$r": '[data-testid="UserCell"]',
            "username": '[data-testid="User-Name"]',
            "bio": '[data-testid="UserDescription"]',
        }
    )

    assert followers, "Failed to extract followers"

    # await twitter_logout(page)
    await page.close()


@pytest.mark.asyncio
async def test_twitter_tweet_interaction(client: HerdClient):
    """Test interacting with a tweet."""
    device = await get_connected_device(client)
    page = await device.new_page()

    # await twitter_login(page)

    # Navigate to a specific tweet
    await page.goto(
        f"https://twitter.com/{TEST_PROFILE}/status/{TEST_TWEET_ID}",
        options={"waitForNavigation": "networkidle2"},
    )

    # Like the tweet
    like_button = await page.find('[data-testid="like"]')
    assert like_button, "Like button not found"
    await page.click('[data-testid="like"]')
    await asyncio.sleep(1)

    # Verify like was registered
    liked_state = await page.extract('[data-testid="like"][data-liked="true"]')
    assert liked_state, "Tweet was not liked successfully"

    # Retweet the tweet
    retweet_button = await page.find('[data-testid="retweet"]')
    assert retweet_button, "Retweet button not found"
    await page.click('[data-testid="retweet"]')
    await asyncio.sleep(1)

    # Click the confirmation button in the retweet dialog
    await page.click('[data-testid="retweetConfirm"]')
    await asyncio.sleep(1)

    # Verify retweet was registered
    retweeted_state = await page.extract(
        '[data-testid="retweet"][data-retweeted="true"]'
    )
    assert retweeted_state, "Tweet was not retweeted successfully"

    # await twitter_logout(page)
    await page.close()
