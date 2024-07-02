import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def test():
    async with async_playwright() as playwright:
        options = {
            'headless': False
        }
        # Make sure to run headed.
        browser = await playwright.chromium.launch(**options)
        # Setup context however you like.
        context = await browser.new_context(
            storage_state=Path("E:\\PycharmProjects\\video-upload\\cookies\\douyin.json"))  # Pass any options
        # Pause the page, and start recording manually.
        page = await context.new_page()
        await page.goto(url="https://creator.douyin.com/creator-micro/content/upload", timeout=20000)
        print(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(test())
