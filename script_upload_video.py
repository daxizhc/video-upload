import asyncio
from datetime import datetime

import video_upload.douyin.uploader as uploader
from video_upload.model import Video

if __name__ == '__main__':
    video = Video(title="1",
                  tags=["程序员", "编程", "互联网"],
                  video_path="D:\\PycharmProjects\\matrix\\video\\1.mp4",
                  cover_path="D:\\PycharmProjects\\matrix\\video\\1.png",
                  publish_time=datetime(2024, 7, 6, 8, 0, 0))
    asyncio.run(uploader.upload_video(video))
