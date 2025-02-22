import typing as t

from aiogram.types import Audio as AAudio
from aiogram.types import Document as ADocument
from aiogram.types import Message
from aiogram.types import PhotoSize as APhotoSize
from aiogram.types import TelegramObject
from aiogram.types import Video as AVideo

Handler = t.Callable[[TelegramObject, dict[str, t.Any]], t.Awaitable[t.Any]]


class MediaGroupObserverProtocol(t.Protocol):
    """Observer protocol"""

    async def add_media(self, message: Message):
        """Add media group"""

    async def schedule_media(self, handler: Handler, message: Message, data: dict[str, t.Any]):
        """Schedule media group dumping to the storage."""


class _PrivateLess:
    def __getstate__(self):
        state = super().__getstate__()
        state.pop('__pydantic_private__')  # noqa
        return state


class PhotoSize(_PrivateLess, APhotoSize):
    pass


class Document(_PrivateLess, ADocument):
    pass


class Video(_PrivateLess, AVideo):
    pass


class Audio(_PrivateLess, AAudio):
    pass
