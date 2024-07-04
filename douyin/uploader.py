from pathlib import Path

from playwright.async_api import async_playwright


async def auth_cookies():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=Path(Path(__file__).parent.resolve() / "cookies.json"))
        # 创建一个新的页面
        page = await context.new_page()
        # 访问指定的 URL
        await page.goto("https://creator.douyin.com/creator-micro/home")

        if "https://creator.douyin.com/creator-micro/home" in page.url:
            print(True)
            return True
        else:
            print(False)
            return False
