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


@pytest.mark.asyncio
async def test_complete_browser_automation_workflow(client: HerdClient):
    """Test a complete browser automation workflow."""
    # Get a connected device
    device = await get_connected_device(client)

    # Create a new page
    page = await device.new_page()
    assert page is not None, "Failed to create new page"

    # Navigate to a test website
    await page.goto(
        "https://example.com", options={"waitForNavigation": "networkidle2"}
    )

    # Extract content using extract method
    title_elem = await page.extract("h1")

    assert title_elem is not None, "Failed to find title element"
    assert title_elem == "Example Domain", "Failed to extract title"

    desc_elem = await page.extract("p")
    assert desc_elem is not None, "Failed to find description element"
    assert "example" in desc_elem.lower(), "Failed to extract description"

    # Close the page
    await page.close()


@pytest.mark.asyncio
async def test_wiki_navigation_and_extraction(client: HerdClient):
    """Test navigating through Wikipedia and extracting content."""
    # Get a connected device
    device = await get_connected_device(client)

    # Create a new page
    page = await device.new_page()
    assert page is not None, "Failed to create new page"

    # Navigate to Wikipedia
    await page.goto(
        "https://en.wikipedia.org/wiki/Web_browser",
        options={"waitForNavigation": "networkidle2"},
    )

    # Extract the main article title and first paragraph
    title_elem = await page.extract("h1#firstHeading")
    assert title_elem == "Web browser", "Failed to extract title"

    intro_elem = await page.extract("#mw-content-text p:not(.mw-empty-elt)")
    assert intro_elem is not None, "Failed to find introduction element"
    assert "web browser" in intro_elem.lower(), "Failed to extract introduction"

    # Extract the history section content
    history_elems = await page.extract(
        {
            "_$r": "#mw-content-text .mw-parser-output > p:not(.mw-empty-elt)",
            "text": ":root",
        }
    )
    assert history_elems, "Failed to find history elements"
    history_text = history_elems[0]["text"]
    assert "browser" in history_text.lower(), "Failed to extract history"

    # Click the WWW link and wait for navigation
    await page.click('a[href*="World_Wide_Web"]')
    await asyncio.sleep(4)  # Wait for navigation

    # Verify we're on the WWW page and extract its content
    new_title_elem = await page.extract("h1#firstHeading")
    assert new_title_elem == "World Wide Web", "Failed to extract WWW title"

    www_intro_elem = await page.extract(
        "#mw-content-text .mw-parser-output > p:not(.mw-empty-elt)"
    )
    assert www_intro_elem is not None, "Failed to find WWW content element"
    assert "www" in www_intro_elem.lower(), "Failed to extract WWW content"

    # Close the page
    await page.close()
