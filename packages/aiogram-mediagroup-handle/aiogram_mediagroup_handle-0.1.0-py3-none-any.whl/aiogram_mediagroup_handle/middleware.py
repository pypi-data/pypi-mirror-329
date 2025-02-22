import typing as t

from aiogram import BaseMiddleware
from aiogram.types import Message

from aiogram_mediagroup_handle import util
from aiogram_mediagroup_handle._types import (
    Handler,
    MediaGroupObserverProtocol
)


class MediaGroupMiddleware(BaseMiddleware):

    def __init__(self, observer: MediaGroupObserverProtocol):
        self._observer = observer

    async def __call__(
        self, handler: Handler, message: Message, data: dict[str, t.Any],
    ) -> t.Any:
        """Add a media to an aiogram fsm context"""
        if util.is_a_mediagroup_message(message):
            await self._observer.add_media(message)
            return await self._observer.schedule_media(handler, message, data)

        return await handler(message, data)
