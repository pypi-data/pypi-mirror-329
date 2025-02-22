import asyncio
import configparser
import logging
import pickle
from typing import Any, Dict, Optional

import aiogram
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey
from aiogram.types import Message

from aiogram_mediagroup_handle import MediaGroup, MediaGroupFilter, MediaGroupObserver

logging.basicConfig(level=logging.DEBUG)


class PickleStorage(BaseStorage):
    def __init__(self):
        self.storage: dict[StorageKey, bytes] = {}

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        """
        Set state for specified key

        :param key: storage key
        :param state: new state
        """
        self.storage[key] = pickle.dumps(state)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Get key state

        :param key: storage key
        :return: current state
        """
        if data := self.storage.get(key):
            return pickle.loads(data).get('state')

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        """
        Write data (replace)

        :param key: storage key
        :param data: new data
        """
        self.storage[key] = pickle.dumps(data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        """
        Get current data for key

        :param key: storage key
        :return: current data
        """
        if data := self.storage.get(key):
            return pickle.loads(data)
        return {}

    async def close(self) -> None:  # pragma: no cover
        """
        Close storage (database connection, file or etc.)
        """
        self.storage.clear()


async def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    dp = aiogram.Dispatcher(
        storage=PickleStorage(),
    )

    @dp.message(MediaGroupFilter())
    async def _handle(message: Message, state: FSMContext):
        data = await state.get_data()
        media: MediaGroup = data[message.media_group_id]

        await message.answer_media_group(media.as_input_media())

    MediaGroupObserver().register(dp)
    bot = Bot(token=config['bot']['token'])

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
