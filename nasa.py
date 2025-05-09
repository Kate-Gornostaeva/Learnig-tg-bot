import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from conf import TOKEN, NASA_API_KEY
import requests
import random
import datetime
from datetime import datetime, timedelta


bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_random_apod():
   end_date = datetime.now()
   start_date = end_date - timedelta(days=365)
   random_date = start_date + (end_date - start_date) * random.random()
   formatted_date = random_date.strftime('%Y-%m-%d')
   url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={formatted_date}'
   response = requests.get(url)
   return response.json()

@dp.message(Command("apod"))
async def send_apod(message: types.Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']

    await message.answer_photo(photo_url, caption=f"{title}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())