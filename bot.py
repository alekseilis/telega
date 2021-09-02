from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher.filters import Text

from random import randint



bot = Bot(token="")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer('Добро пожаловать в бота!')
    await message.answer('Доступный список команд: \n\n /Hi \n\n /Random \n\n /Drinks \n\n /WWW ')
    await message.answer('Можете ввести комаду для ввода данных: \n\n /test')

################################# начало FSM

class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()

@dp.message_handler(commands='test')
async def start_test(message: types.Message):
    await message.answer('Вы начали тестирование! Введи ваше имя с клавиатуры!')

    await Form.first()


@dp.message_handler(state=Form.name)
async def answer_name(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer_1 = answer)
    await message.answer('Сколько вам лет ?')

    await Form.next()

@dp.message_handler(state=Form.age)
async def answer_age(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer_2 = answer)
    await message.answer('Укажите ваш пол.')

    await Form.last()

@dp.message_handler(state=Form.gender)
async def answer_gender(message: types.Message,state: FSMContext):
    data = await state.get_data()
    answer_1 = data.get('answer_1')
    answer_2 = data.get('answer_2')
    answer_3 = message.text

    await message.answer('Спасибо за ответы!')
    await message.answer(f'Ваше имя : {answer_1}')
    await message.answer(f'Ваш возраст :  {answer_2}')
    await message.answer(f'Ваш возраст : {answer_3}')

    await state.finish()

################################# конец FSM

@dp.message_handler(commands='hi')
async def command_hi(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button = [types.InlineKeyboardButton(text='Сказать привет!', callback_data='hello')]
    keyboard.add(*button)
    await message.answer('Нажми , что-бы поздороваться!', reply_markup=keyboard)


@dp.callback_query_handler(text='hello')
async def hi(call: types.CallbackQuery):
    await call.message.answer('Привет , Гость!')
    await call.answer('Увидимся!')


@dp.message_handler(commands='random')
async def command_random(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text='Нажми!', callback_data='random_value')]
    keyboard.add(*buttons)
    await message.answer('Нажми на кнопку и получи случайное число от 1 до 100', reply_markup=keyboard)


@dp.callback_query_handler(text='random_value')
async def random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 100)))
    await call.answer('Спасибо за игру!')


@dp.message_handler(commands=['Drinks'])
async def menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [KeyboardButton(text='Pivo'),
               KeyboardButton(text='Vodka')]
    keyboard.add(*buttons)
    await message.answer('Что будем пить?', reply_markup=keyboard)


@dp.message_handler(Text(equals=['Pivo']))
async def pivo(message: types.Message):
    await message.answer('Возьми водки!', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals=['Vodka']))
async def pivo(message: types.Message):
    await message.answer('Спасибо , что взял меня! ', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['www'])
async def menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [InlineKeyboardButton(text='Youtube', url='https://www.youtube.com'),
               InlineKeyboardButton(text='Google', url='https://www.google.by')]
    keyboard.add(*buttons)
    await message.answer('Смотрим или гуглим ?', reply_markup=keyboard)


@dp.message_handler()
async def echo_bot(message: types.Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    print('Бот запущен!')
    executor.start_polling(dp)