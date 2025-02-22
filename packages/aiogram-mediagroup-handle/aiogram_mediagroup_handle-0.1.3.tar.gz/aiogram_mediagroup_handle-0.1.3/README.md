# aiogram-mediagroup-handle

**aiogram plugin for handling media groups**

This library supports **aiogram v3 and above**.

## Overview

`aiogram-mediagroup-handle` leverages the `aiogram.Dispatcher.storage` to collect and store 
media files in FSM data by `media_group_id`.

FSMStorage ensures data consistency and, combined with data serialization, allows any of 
the known storage strategies to be used (not just in-memory).

`aiogram-mediagroup-handle` comes with some utilities:
- **MediaGroupFilter** – A filter to detect media groups.
- **MediaGroup** – A lightweight dataclass object (the actual media group intake) accessible in 
FSMStorage data dictionary by `media_group_id`.

### MediaGroup Dataclass reference
```python
from dataclasses import dataclass, field
import typing as t
from aiogram.types import PhotoSize, Audio, Document, Video
from aiogram.enums import ContentType

MediaGroupType = list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo]
MediaType = list[PhotoSize] | Audio | Document | Video

@dataclass(slots=True, kw_only=True, frozen=True)
class MediaGroup:
    """Lightweight media group representation."""
    caption: t.Optional[str] = None
    photos: list[list[PhotoSize]] = field(default_factory=list)
    audio: list[Audio] = field(default_factory=list)
    documents: list[Document] = field(default_factory=list)
    video: list[Video] = field(default_factory=list)
    
    def get_media(self) -> t.Iterator[MediaType]:
        """Return media group iterator"""
        ...
    
    def as_input_media(self) -> MediaGroupType:
        """Return media group for sending via aiogram.Bot"""
        ...
        
    @property
    def content_type(self) -> ContentType:
        """Return media group content type"""
        ...

```

## Usage

### Registering the Observer
```python
import aiogram
from aiogram_mediagroup_handle import MediaGroupObserver

dp = aiogram.Dispatcher(...)
observer = MediaGroupObserver()
observer.register(dp)
```

### Handling Media Groups
```python
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram_mediagroup_handle import MediaGroupFilter, MediaGroup

router = Router()

@router.message(MediaGroupFilter())
async def media_group_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    media_data: MediaGroup = data[message.media_group_id]
    # Process the media group data here...
    
    # f.e. answer with media
    await message.answer_media_group(media=media_data.as_input_media())
```

## Installation
```sh
pip install aiogram-mediagroup-handle
```

## License
[MIT License](LICENSE)

