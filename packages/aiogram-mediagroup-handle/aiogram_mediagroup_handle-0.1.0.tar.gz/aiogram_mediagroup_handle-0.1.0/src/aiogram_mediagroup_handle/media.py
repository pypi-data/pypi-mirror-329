import typing as t
from dataclasses import dataclass, field

from aiogram.enums import ContentType
from aiogram.types import Audio, Document, PhotoSize, Video


@dataclass(slots=True, kw_only=True, frozen=True)
class MediaGroup:
    """Light weighted media group"""
    caption: t.Optional[str]
    photos: list[list[PhotoSize]] = field(default_factory=list)
    audio: list[Audio] = field(default_factory=list)
    documents: list[Document] = field(default_factory=list)
    video: list[Video] = field(default_factory=list)

    @property
    def content_type(self) -> str:
        """Return media group content type"""
        if self.photos:
            return ContentType.PHOTO
        if self.documents:
            return ContentType.DOCUMENT
        if self.audio:
            return ContentType.AUDIO
        if self.video:
            return ContentType.VIDEO

        return ContentType.UNKNOWN
