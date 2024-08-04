import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

from video_upload.constants import DOUYIN_UPLOAD_PAGE, DOUYIN_HOME_PAGE, DOUYIN_PUBLISH_PAGE, \
    DOUYIN_PUBLISH_FINISH_PAGE
from video_upload.errors import VideoUploadError
from video_upload.model import Video


async def upload_video(video: Video):
    await auth_cookies()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=Path(Path(__file__).parent.resolve() / "cookies.json"))

        # 创建一个新的页面
        page = await context.new_page()
        # 上传视频，并进入发布页面
        await upload_video_and_enter_publish_page(page, video)
        # 设置标题和话题
        await set_title_and_tags(page, video)
        # 设置定时发布
        await set_publish_time(page, video)
        # 点击发布
        await publish_video(page)

        await context.storage_state(path=Path(Path(__file__).parent.resolve() / "cookies.json"))  # 保存cookie
        print('  [-]cookie更新完毕！')
        await asyncio.sleep(2)  # 这里延迟是为了方便眼睛直观的观看
        # 关闭浏览器上下文和浏览器实例
        await context.close()
        await browser.close()
        await playwright.stop()


async def upload_video_and_enter_publish_page(page, video: Video):
    # 访问指定的 URL
    await page.goto(DOUYIN_UPLOAD_PAGE)
    await page.wait_for_url(DOUYIN_UPLOAD_PAGE)
    # 点击 "上传视频" 按钮
    await page.locator(".upload-btn--9eZLd").set_input_files(video.video_path)

    # 等待页面跳转到指定的 URL
    while True:
        # 判断是是否进入视频发布页面，没进入，则自动等待到超时
        try:
            await page.wait_for_url(DOUYIN_PUBLISH_PAGE)
            break
        except:
            print("正在等待进入视频发布页面...")
            await asyncio.sleep(1)


async def set_title_and_tags(page, video: Video):
    await asyncio.sleep(1)
    print("  [-] 正在填充标题和话题...")
    title_container = page.get_by_text('作品标题').locator("..").locator("xpath=following-sibling::div[1]").locator(
        "input")
    if await title_container.count():
        await title_container.fill(video.title[:30])
    else:
        title_container = page.locator(".notranslate")
        await title_container.click()
        print("clear existing title")
        await page.keyboard.press("Backspace")
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.press("Delete")
        print("filling new  title")
        await page.keyboard.type(video.title)
        await page.keyboard.press("Enter")
    css_selector = ".zone-container"
    for index, tag in enumerate(video.tags, start=1):
        print("正在添加第%s个话题" % index)
        await page.type(css_selector, "#" + tag)
        await page.press(css_selector, "Space")


async def set_publish_time(page, video: Video):
    if video.publish_time is not None:
        # 选择包含特定文本内容的 label 元素
        label_element = page.locator("label.radio--4Gpx6:has-text('定时发布')")
        # 在选中的 label 元素下点击 checkbox
        await label_element.click()
        await asyncio.sleep(1)
        publish_date_hour = video.publish_time

        await asyncio.sleep(1)
        await page.locator('.semi-input[placeholder="日期和时间"]').click()
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.type(str(publish_date_hour))  # 定时发布最早也要2h以后
        await page.keyboard.press("Enter")

        await asyncio.sleep(1)


async def publish_video(page):
    # 判断视频是否发布成功
    while True:
        # 判断视频是否发布成功
        try:
            publish_button = page.get_by_role('button', name="发布", exact=True)
            if await publish_button.count():
                await publish_button.click()
            await page.wait_for_url(DOUYIN_PUBLISH_FINISH_PAGE,
                                    timeout=1500)  # 如果自动跳转到作品页面，则代表发布成功
            print("  [-]视频发布成功")
            break
        except:
            print("  [-] 视频正在发布中...")
            await page.screenshot(full_page=True)
            await asyncio.sleep(0.5)


async def auth_cookies():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=Path(Path(__file__).parent.resolve() / "cookies.json"))
        # 创建一个新的页面
        page = await context.new_page()
        # 访问指定的 URL
        await page.goto(DOUYIN_HOME_PAGE)

        if DOUYIN_HOME_PAGE not in page.url:
            raise VideoUploadError("cookies invalid")

        await context.close()
        await browser.close()
        await playwright.stop()
