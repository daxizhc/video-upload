import asyncio
from contextlib import asynccontextmanager


from fastapi import FastAPI
from playwright.async_api import async_playwright

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     manager = async_playwright()
#     playwright = await manager.__aenter__()
#     app.state.playwright = playwright
#     yield
#     await manager.__aexit__()


app = FastAPI()


@app.get("/generate/cookies/douyin")
async def generate_cookies_douyin():
    await test()
    return "ok"


async def test():
    async with async_playwright() as playwright:
        options = {
            'headless': False
        }
        # Make sure to run headed.
        browser = await playwright.chromium.launch(**options)
        # Setup context however you like.
        context = await browser.new_context()  # Pass any options
        # Pause the page, and start recording manually.
        page = await context.new_page()
        await page.goto(url="https://creator.douyin.com/creator-micro/content/upload", timeout=20000)
        print(1)
