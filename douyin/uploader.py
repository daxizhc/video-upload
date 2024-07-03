import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def fetch_cookies():
    async with async_playwright() as playwright:
        options = {
            'headless': False
        }

        browser = await playwright.chromium.launch(**options)

        context = await browser.new_context()  # Pass any options

        page = await context.new_page()

        await page.goto(url="https://creator.douyin.com/", timeout=20000)

        while 'https://creator.douyin.com/creator-micro/home' not in page.url:
            await asyncio.sleep(5)

        cookies_path = Path(Path(__file__).parent.resolve() / "cookies.json")
        # 保存cookie
        await context.storage_state(path=cookies_path)

        await context.close()
        await browser.close()
        await playwright.stop()
