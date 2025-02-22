from aiogram.filters import BaseFilter

from aiogram_mediagroup_handle import util


class MediaGroupFilter(BaseFilter):
    async def __call__(self, message) -> bool:
        return util.is_a_mediagroup_message(message)
