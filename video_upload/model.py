from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Video(BaseModel):
    title: str

    tags: List[str] = []

    cover_path: str

    video_path: str

    publish_time: Optional[datetime] = None
