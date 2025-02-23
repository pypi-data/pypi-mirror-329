import os
from typing import Optional

from .const import TextMode
from .notification import Notification
from .session import PushyAPI
from .utils import _format_tags


class Feed:
    _api: PushyAPI
    api_key: str

    def __init__(self, api: PushyAPI, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.environ['PUSHY_API_KEY']
        self._api = api
        self.api_key = api_key

    def get_notification(self, post_key: str) -> Notification:
        return Notification(self, post_key)

    async def edit_notification_text(
            self, notification_post_key: str, text: str,
            mode: TextMode, tags: list[str] = None
    ) -> None:
        await self._api.put(
            f'/v1/feeds/{self.api_key}/text/{notification_post_key}',
            params={'mode': mode, 'tags': _format_tags(tags)},
            body=text
        )

    async def delete_notification(self, notification_post_key: str) -> None:
        await self._api.delete(
            f'/v1/feeds/{self.api_key}/notifications/{notification_post_key}'
        )

    async def send_text(
            self,
            text: str,
            mode: TextMode = TextMode.DEFAULT,
            tags: list[str] | None = None,
            media_url: str | None = None,
            media_spoiler: bool = False
    ):
        result = await self._api.post(
            f'/v1/feeds/{self.api_key}/text',
            params={
                'mode': mode,
                'tags': _format_tags(tags),
                'media_url': media_url,
                'media_spoiler': media_spoiler
            },
            body=text
        )
        return self.get_notification(result['post_key'])
