from dataclasses import dataclass


@dataclass
class TiktokUrl:

    username: str
    """
    The user who the video belongs to.
    """
    video_id: str
    """
    The id of the video.
    """
    url: str
    """
    The long Tiktok url of that video.
    """

    def __init__(
        self,
        username: str,
        video_id: str,
        url: str
    ):
        self.username = username
        self.video_id = video_id
        self.url = url