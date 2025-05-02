import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile
from deep_translator import GoogleTranslator
from gtts import gTTS
from conf import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
states = {'voice': set(), 'translate': set()}


@dp.message(CommandStart())
async def start(message):
    await message.answer(f"Привет, {message.from_user.first_name}. "
                         f"Я бот, которого создали исключительно в учебных целях.")

@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Это бот выполняет команды:\n"
                         "Чтобы начать работу введите /start\n"
                         "Чтобы получить справку введите /help\n"
                         "Чтобы сохранить фото введите /photo\n"
                         "Чтобы послушать бота введите /voice\n"
                         "Чтобы получить перевод на английский введите /english")

@dp.message(Command("photo"))
async def handle_photo_command(message: types.Message):
    await message.answer("Отправьте мне фото, и я сохраню его в папку img.")


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]

    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    save_path = f"img/{file_id}.jpg"
    await bot.download_file(file_path, save_path)
    await message.answer(f"Фото сохранено как {save_path}")


@dp.message(Command("voice"))
async def voice_cmd(message: types.Message):
    states['voice'].add(message.from_user.id)
    await message.answer("Отправьте текст для озвучки")


@dp.message(Command("english"))
async def english_cmd(message: types.Message):
    states['translate'].add(message.from_user.id)
    await message.answer("Введите текст для перевода")


@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id

    if user_id in states['voice']:
        tts = gTTS(text=message.text, lang='ru')
        tts.save(f"voice_{user_id}.mp3")
        await message.answer_voice(FSInputFile(f"voice_{user_id}.mp3"))
        states['voice'].remove(user_id)

    elif user_id in states['translate']:
        translation = GoogleTranslator(source='ru', target='en').translate(message.text)
        await message.answer(f"Перевод: {translation}")
        states['translate'].remove(user_id)

    elif not message.text.startswith('/'):
        await message.answer(message.text)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

