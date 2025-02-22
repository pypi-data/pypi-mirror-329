import typing as t
from dataclasses import dataclass, field

from aiogram.enums import ContentType
from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
)

from aiogram_mediagroup_handle._types import Audio, Document, PhotoSize, Video

MediaGroupType = list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo]
MediaType = list[PhotoSize] | Audio | Document | Video

_media_mapping = {
    PhotoSize: InputMediaPhoto,
    Audio: InputMediaAudio,
    Document: InputMediaDocument,
    Video: InputMediaVideo,
}


def _unpack_type(obj):
    if isinstance(obj, list):
        return _unpack_type(obj[0])
    return type(obj)


@dataclass(slots=True, kw_only=True, frozen=True)
class MediaGroup:
    """Light weighted media group"""
    caption: t.Optional[str]
    photos: list[list[PhotoSize]] = field(default_factory=list)
    audio: list[Audio] = field(default_factory=list)
    documents: list[Document] = field(default_factory=list)
    video: list[Video] = field(default_factory=list)

    def get_media(self) -> t.Iterator[MediaType]:
        """Return media group iterator"""
        return iter(self.photos + self.audio + self.documents + self.video)

    def as_input_media(self) -> MediaGroupType:
        """Return media group for sending via aiogram.Bot"""
        return [
            _media_mapping[_unpack_type(media)](
                media=media[-1].file_id if isinstance(media, list) else media.file_id,
                caption=self.caption if idx == 0 else None,
            )
            for idx, media in enumerate(self.get_media())
        ]

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

    def __len__(self) -> int:
        return len(self.photos) + len(self.audio) + len(self.documents) + len(self.video)
