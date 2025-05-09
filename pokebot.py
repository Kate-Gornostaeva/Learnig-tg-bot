import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import requests
from conf import TOKEN
from googletrans import Translator


bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


def get_pokemon_info(pokemon_name):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
    if response.status_code != 200:
        return None
    pokemon_data = response.json()
    return pokemon_data


def get_pokemon_species_info(species_url):
    response = requests.get(species_url)
    if response.status_code == 200:
            return response.json()
    return None

def translate_description(text):
    try:
        translated = translator.translate(text, src='en', dest='ru')
        return translated.text
    except Exception:
        return text + "\n\n(Не удалось перевести описание)"


def get_pokemon_description(pokemon_data):
    species_url = pokemon_data['species']['url']
    species_data = get_pokemon_species_info(species_url)

    if species_data:
        for entry in species_data['flavor_text_entries']:
            if entry['language']['name'] == 'en':
                description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                return translate_description(description)
    return "Описание недоступно."

#Извлекает URL изображения покемона
def get_pokemon_image_url(pokemon_data):
    if 'other' in pokemon_data['sprites'] and 'official-artwork' in pokemon_data['sprites']['other']:
        return pokemon_data['sprites']['other']['official-artwork']['front_default']
    return pokemon_data['sprites']['front_default']


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я бот-покемодекс. 🎮\n\n"
        "Напиши мне имя покемона на английском, например 'pikachu', "
        "и я покажу тебе его изображение и описание.\n\n"
        "Попробуй: charizard, bulbasaur, mewtwo, ditto"
    )


@dp.message()
async def send_pokemon_info(message: Message):
    pokemon_name = message.text.strip()
    pokemon_data = get_pokemon_info(pokemon_name)

    if not pokemon_data:
        await message.answer(f"Покемон '{pokemon_name}' не найден. Проверь написание и попробуй снова.")
        return

    # Получаем данные о покемоне
    image_url = get_pokemon_image_url(pokemon_data)
    description = get_pokemon_description(pokemon_data)
    types = [t['type']['name'] for t in pokemon_data['types']]

    # Формируем сообщение
    info = (
        f"Имя: {pokemon_data['name'].capitalize()}\n"
        f"Тип: {', '.join(types).title()}\n"
        f"Рост: {pokemon_data['height'] / 10} м\n"
        f"Вес: {pokemon_data['weight'] / 10} кг\n\n"
        f"Описание: {description}"
    )

    await message.answer_photo(image_url, caption=info)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())