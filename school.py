import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
from conf import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )
''')
    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("Введите фамилию и имя учащегося")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите возраст учащегося")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите класс")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer(f"Фамилия: {user_data['name']}\nВозраст: {user_data['age']}\nКласс: {user_data['grade']}")

    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())