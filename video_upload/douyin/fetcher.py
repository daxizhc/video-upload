import asyncio
import sys
from pathlib import Path
import logging
from playwright.async_api import async_playwright

from video_upload.constants import DOUYIN_HOME_PAGE

logger = logging.getLogger("douyin-uploader")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


async def fetch_cookies():
    async with async_playwright() as playwright:
        options = {
            'headless': False
        }

        browser = await playwright.chromium.launch(**options)

        context = await browser.new_context()  # Pass any options

        page = await context.new_page()

        logger.info("开始打开登录页面")
        await page.goto(url="https://creator.douyin.com/", timeout=20000)
        logger.info("打开登录页面成功")

        while DOUYIN_HOME_PAGE not in page.url:
            logger.info("等待登录...")
            await asyncio.sleep(5)

        logger.info("登录成功")
        cookies_path = Path(Path(__file__).parent.resolve() / "cookies.json")
        # 保存cookie
        await context.storage_state(path=cookies_path)
        logger.info("保存cookie成功")

        await context.close()
        await browser.close()
        await playwright.stop()
        logger.info("退出浏览器")
