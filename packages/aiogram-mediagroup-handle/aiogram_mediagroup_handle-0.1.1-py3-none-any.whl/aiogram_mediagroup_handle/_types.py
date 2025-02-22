import typing as t

from aiogram.types import Message, TelegramObject

Handler = t.Callable[[TelegramObject, dict[str, t.Any]], t.Awaitable[t.Any]]


class MediaGroupObserverProtocol(t.Protocol):
    """Observer protocol"""

    async def add_media(self, message: Message):
        """Add media group"""

    async def schedule_media(self, handler: Handler, message: Message, data: dict[str, t.Any]):
        """Schedule media group dumping to the storage."""
