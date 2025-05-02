import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging
from conf import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()


#
# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         user_id INTEGER PRIMARY KEY,
#         username TEXT,
#         chat_id INTEGER
#     )
# ''')
#
# conn.commit()
# conn.close()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())