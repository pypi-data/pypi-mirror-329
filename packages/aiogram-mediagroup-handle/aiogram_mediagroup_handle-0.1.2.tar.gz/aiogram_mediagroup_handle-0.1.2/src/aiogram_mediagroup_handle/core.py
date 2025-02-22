import asyncio
import contextlib
import contextvars
import typing as t

from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ContentType
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage, StorageKey
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import Audio, Document, Message, PhotoSize, Video

from aiogram_mediagroup_handle._types import Handler
from aiogram_mediagroup_handle.media import MediaGroup
from aiogram_mediagroup_handle.middleware import MediaGroupMiddleware

DEFAULT_TIMEOUT = 0.3
_action_map = {
    ContentType.AUDIO: lambda self, message: self._audio.append(message.audio),
    ContentType.DOCUMENT: lambda self, message: self._documents.append(message.document),
    ContentType.PHOTO: lambda self, message: self._photos.append(message.photo),
    ContentType.VIDEO: lambda self, message: self._video.append(message.video),
}

__all__ = [
    "MediaGroupObserver",
]


class MediaGroupObserver:
    """Catches aiogram media group photos and folds to the store"""

    def __init__(
        self,
        wait_for: float = DEFAULT_TIMEOUT,
        loop: t.Optional[asyncio.AbstractEventLoop] = None,
        events_isolation: t.Optional[BaseEventIsolation] = None,
    ) -> None:
        """
        :param float wait_for: time to wait for new updates with current media_group_id
        :param loop: optional asyncio event loop
        """
        assert wait_for > 0, 'wait_for must be positive'
        self._wait_for = wait_for

        self._loop = loop or asyncio.get_event_loop()
        self._events_isolation = events_isolation or SimpleEventIsolation()
        self._storage: t.Optional[BaseStorage] = None

    def register(self, dispatcher: Dispatcher):
        """Register dispatcher's fsm and storage"""
        self._storage = dispatcher.storage
        dispatcher.message.outer_middleware.register(
            MediaGroupMiddleware(observer=self)
        )

    @classmethod
    def _resolve_key(cls, message: Message):
        """Resolve message to a storage key"""
        return StorageKey(
            bot_id=message.bot.id,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            thread_id=message.message_thread_id,
            business_connection_id=message.business_connection_id,
        )

    @classmethod
    def _raw(cls, media_group_id):
        return f"raw_{media_group_id}"

    @contextlib.asynccontextmanager
    async def _get_context(self, message: Message) -> tuple[StorageKey, dict[str, t.Any]]:
        context_key = self._resolve_key(message)
        async with self._events_isolation.lock(key=context_key):
            data = await self._storage.get_data(context_key)
            yield context_key, data

    async def _dump_to_storage(self, handler: Handler, message: Message, data: dict[str, t.Any]):
        """Dump media group to the storage."""
        async with self._get_context(message) as (context_key, storage_data):
            if (store := storage_data.get(self._raw(message.media_group_id))) is None:
                return await handler(message, data)

            if not store.is_ready(self._loop.time() - self._wait_for):
                return UNHANDLED

            del storage_data[self._raw(message.media_group_id)]
            data[message.media_group_id] = MediaGroup(
                caption=store.caption,
                photos=store.photos,
                audio=store.audio,
                documents=store.documents,
            )
            await self._storage.set_data(context_key, data=data)
            return await handler(message, data)

    async def add_media(self, message: Message):
        """Add media group photo"""
        media_group_id = message.media_group_id

        async with self._get_context(message) as (context_key, data):
            now = self._loop.time()
            store = data.setdefault(
                self._raw(media_group_id),
                MediaGroupStore(created_at=now, caption=message.caption),
            )

            await store.update_from_message(message, now)
            await self._storage.update_data(context_key, data=data)

    async def schedule_media(
        self, handler: Handler, message: Message, data: dict[str, t.Any],
    ) -> None:
        """Schedule media group photo dumping to the storage."""
        context = contextvars.copy_context()
        self._loop.call_later(
            self._wait_for,
            asyncio.create_task,
            self._dump_to_storage(handler, message, data),
            context=context,
        )


class MediaGroupStore:
    """Media message store"""

    caption: t.Optional[str] = property(lambda self: self._caption[:])
    photos: list[list[PhotoSize]] = property(lambda self: self._photos[:])
    audio: list[Audio] = property(lambda self: self._audio[:])
    documents: list[Document] = property(lambda self: self._documents[:])
    video: list[Video] = property(lambda self: self._video[:])

    def __init__(self, created_at: float, caption: t.Optional[str]) -> None:
        self._last_updated: float = created_at
        self._caption: t.Optional[str] = caption

        self._photos: list[list[PhotoSize]] = []
        self._audio: list[Audio] = []
        self._documents: list[Document] = []
        self._video: list[Video] = []

    async def update_from_message(self, message: Message, now: float) -> None:
        """Update photo list from message"""
        _action_map[t.cast(ContentType, message.content_type)](self, message)
        self._last_updated = now

    def is_ready(self, deadline: float) -> bool:
        """Return True if message store is completed."""
        return deadline > self._last_updated

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)
