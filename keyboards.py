from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
main = ReplyKeyboardMarkup(keyboard=[
      [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url="https://ria.ru/")],
    [InlineKeyboardButton(text="Музыка", url="https://zaycev.net/")],
    [InlineKeyboardButton(text="Видео", url="https://rutube.ru/")]
])

inline_keyboard_more = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]

])

test = ["Опция 1", "Опция 2", "Опция 3", "Опция 4"]
urls = ['https://i.pinimg.com/originals/42/4e/6f/424e6fe3ad41fc58378ba0855782f0e4.jpg',
       'https://avatars.dzeninfra.ru/get-zen_doc/1592767/pub_60264756331cb763521e794e_602648aab498705a818b1883/scale_1200',
       'https://i.pinimg.com/originals/72/65/fc/7265fccf2b3cad93e010d7d123a592d2.jpg',
       'https://i.pinimg.com/736x/a1/0b/13/a10b1313c4f086e331ff0dac98822050.jpg']

async def option_keyboard():
    keyboard = InlineKeyboardBuilder()
    for text, url in zip(test, urls):
        keyboard.add(InlineKeyboardButton(text=text, url=url))  # Устанавливаем свой URL для каждой кнопки
    return keyboard.adjust(2).as_markup()