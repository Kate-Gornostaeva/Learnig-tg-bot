import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from conf import TOKEN, CATS_API_KEY
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_cats_breeds():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {"x-api-key": CATS_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def get_cat_image_by_breed (breed_id):
    url = f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}'
    headers = {"x-api-key": CATS_API_KEY}
    response = requests.get(url, headers=headers)
    data =response.json()
    return data[0]['url']

def get_breed_info(breed_name):
    breeds = get_cats_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот для поиска котов по породам. Пожалуйста, введите название породы кота.")


@dp.message()
async def send_cat_info (message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info:
        breed_id = breed_info['id']
        cat_image_url = get_cat_image_by_breed(breed_id)
        info  = (f"Название породы: {breed_info['name']}\n"
                 f"Описание: {breed_info['description']}\n"
                 f"Продолжительность жизни: {breed_info['life_span'] }\n")
        await message.answer_photo(cat_image_url, caption=info)
    else:
        await message.answer("Порода кота не найдена.")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
