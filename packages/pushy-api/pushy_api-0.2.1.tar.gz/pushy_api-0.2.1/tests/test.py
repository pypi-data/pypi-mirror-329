import asyncio

import pytest

from pushy import PushyAPI, Feed


@pytest.mark.asyncio
async def test_simple_notification():
    api = await PushyAPI.create()
    feed = Feed(api)
    post = await feed.send_text("Hello, world!")
    assert post.post_key.startswith('pk')


@pytest.mark.asyncio
async def test_edit_notification():
    api = await PushyAPI.create()
    feed = Feed(api)
    post_upd = await feed.send_text("Old text to be updated")
    await asyncio.sleep(1)
    await post_upd.edit_text("Updated text")


@pytest.mark.asyncio
async def test_delete_notification():
    api = await PushyAPI.create()
    feed = Feed(api)
    post_del = await feed.send_text("Text to be deleted")
    await asyncio.sleep(1)
    await post_del.delete()
