import typing

from .const import TextMode

if typing.TYPE_CHECKING:
    from .feed import Feed


class Notification:
    _feed: 'Feed'
    post_key: str

    def __init__(self, feed: 'Feed', post_key: str):
        self._feed = feed
        self.post_key = post_key

    async def edit_text(self, text: str, mode: TextMode = TextMode.DEFAULT, tags: list[str] | None = None):
        return await self._feed.edit_notification_text(self.post_key, text, mode, tags)

    async def delete(self):
        return await self._feed.delete_notification(self.post_key)