import asyncio
import logging
import random
import requests
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from conf import TOKEN, EXCHANGE_API_KEY


bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


button_register = KeyboardButton(text='Регистрация')
button_exchange_rates = KeyboardButton(text='Курсы валют')
button_tips= KeyboardButton(text='Советы по экономии')
button_finances= KeyboardButton(text='Личные финансы')

keyboards = ReplyKeyboardMarkup(keyboard=[
    [button_register, button_exchange_rates],
    [button_tips, button_finances]
], resize_keyboard=True)

conn = sqlite3.connect('user.db')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,        
        name TEXT NOT NULL,
        category1 TEXT,
        category2 TEXT,
        category3 TEXT,
        expenses1 REAL,
        expenses2 REAL,
        expenses3 REAL
    )
''')
conn.commit()

class FinanceForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Добро пожаловать в бота-финансового помощника! Выберите одну из опций:", reply_markup=keyboards)

@dp.message(F.text == 'Регистрация')
async def register(message: types.Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name

    cur.execute ('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
    user = cur.fetchone()
    if user :
        await message.answer("Вы уже зарегистрированы!")
    else:
        cur.execute ('''INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer("Вы успешно зарегистрировались!")

@dp.message(F.text == 'Курсы валют')
async def exchange_rates(message: types.Message):
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer('Произошла ошибка при получении курсов валют')
            return
        usd_to_rub = data['conversion_rates']['RUB']
        euro_to_usd = data['conversion_rates']['EUR']
        euro_to_rub = (1 /euro_to_usd) * usd_to_rub
        await message.answer(f'Курс USD/RUB: {usd_to_rub:.2f}\n'
                             f'Курс EUR/USD: {euro_to_usd:.2f}\n'
                             f'Курс EUR/RUB: {euro_to_rub:.2f}')

    except Exception as e:
        await message.answer(f'Произошла ошибка при получении курсов валют: {e}')

@dp.message(F.text == 'Советы по экономии')
async def tips(message: types.Message):
    tips = [
        "Холодильник — не музей! Не храни там экспонаты прошлого месяца.Забытый огурец — это не арт-объект, а будущий компост. Планируй меню и ешь остатки, пока они не начали с тобой разговаривать.",
        "Стиралка — не фондюшница. Загружай её полностью, но не до состояния щёлкни — и взорвётся. И да, режим 30°C — твой друг.Кипятить можно чайник, а не футболки.",
        "Вода капает? Это плачет твой кошелёк! Почини кран, даже если он всего лишь поёт тебе печальные баллады.А ещё поставьте бутылку в бачок унитаза — пусть экономит воду, пока ты экономишь деньги.",
        "Зарядка — не украшение. Выдёргивай зарядку из розетки, особенно если у тебя кот с пытливым умом и стальными когтями.Электричество дорожает, а новые провода — тоже не бесплатные.",
        "Магазины — это квест, а не терапия. Ходи за продуктами с списком и сытым.Иначе купишь три пакета чипсов, потому что они смотрят с тоской. Голодный шопинг — враг бюджета!😄"
        ]
    tip = random.choice(tips)
    await message.answer(tip)

@dp.message(F.text == 'Личные финансы')
async def finances(message: types.Message, state: FSMContext):
    await state.set_state(FinanceForm.category1)
    await message.reply("Введите первую категорию расходов")

@dp.message(FinanceForm.category1)
async def finances(message: types.Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinanceForm.expenses1)
    await message.reply("Введите расходы на эту катергорию")

@dp.message(FinanceForm.expenses1)
async def finances(message: types.Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinanceForm.category2)
    await message.reply("Введите вторую категорию расходов")

@dp.message(FinanceForm.category2)
async def finances(message: types.Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinanceForm.expenses2)
    await message.reply("Введите расходы на эту катергорию")

@dp.message(FinanceForm.expenses2)
async def finances(message: types.Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinanceForm.category3)
    await message.reply("Введите третью категорию расходов")

@dp.message(FinanceForm.category3)
async def finances(message: types.Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinanceForm.expenses3)
    await message.reply("Введите расходы на эту катергорию")

@dp.message(FinanceForm.expenses3)
async def finances(message: types.Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = message.from_user.id
    cur.execute('''
                UPDATE users 
                SET category1 = ?, expenses1 = ?, 
                    category2 = ?, expenses2 = ?, 
                    category3 = ?, expenses3 = ? 
                WHERE telegram_id = ?
            ''', (
        data['category1'], data['expenses1'],
        data['category2'], data['expenses2'],
        data['category3'], float(message.text),
        telegram_id
    ))
    conn.commit()

    await state.clear()
    await message.answer("Данные успешно сохранены!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())