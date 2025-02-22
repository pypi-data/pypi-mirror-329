from aiogram.types import Message


def is_a_mediagroup_message(message: Message):
    """Return True if the message contains mediagroup."""
    return message.media_group_id is not None
