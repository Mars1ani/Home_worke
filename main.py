from decouple import config

from aiogram import Bot, Dispatcher, Router, F
import asyncio
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import logging
import random

token = config('BOT_TOKEN')

router = Router()

drinks_db = []

class AddProduct(StatesGroup):
    product_1 = State()
    product_2 = State()
    product_3 = State()


@router.message(Command("start"))
async def start_command(message: Message, bot: Bot):
    await message.answer("Напиши мне  свое имя")
    about_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="О нас", callback_data="about")]
    ])
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот, который поможет тебе с твоими задачами.", reply_markup=about_keyboard)


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("/start - начать работу с ботом\n/help - помощь")


@router.message(Command('menu'))
async def menu_command(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/time"), KeyboardButton(text="/random")],
            [KeyboardButton(text="/joke"), KeyboardButton(text="/mem")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer("Выберите команду:", reply_markup=keyboard)


@router.message(Command("time"))
async def time_command(message: Message):
    now =datetime.now()
    await message.answer(f"Текущее время: {now.strftime('%H:%M:%S')}")


@router.message(Command("random"))
async def random_command(message: Message):
    number = random.randint(1, 100)
    await message.answer(f"Случайное число: {number}")


jokes = [
    "Почему программисты любят кофе? Потому что без него они не могут компилировать свои мысли.",
    "Почему программисты не любят природу? Потому что там нет Wi-Fi.",
    "Почему программисты не любят кошек? Потому что они не могут отлаживать их поведение.",
    "Почему программисты не любят спорт? Потому что они не могут найти кнопку 'Run' на беговой дорожке.",
    "Почему программисты не любят отпуск? Потому что они не могут найти кнопку 'Debug' на пляже.",
]


@router.message(Command("joke"))
async def joke_command(message: Message):
    joke = random.choice(jokes)
    await message.answer(joke)


@router.message(F.text == 'привет')
async def hello_command(message: Message):
    await message.answer("Привет! Как дела?")


@router.message(F.text == 'пока')
async def bye_command(message: Message):
    await message.answer("До встречи!")

@router.callback_query(lambda c: c.data == 'about')
async def about_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Наше кафе — уютное место с свежими напитками и приятной атмосферой.")


@router.message(Command('add_product'))
async def add_product_start(message: Message, state: FSMContext):
    await state.set_state(AddProduct.product_1)
    await message.answer("Введите напиток 1:")


@router.message(AddProduct.product_1)
async def add_product_1(message: Message, state: FSMContext):
    await state.update_data(product_1=message.text)
    await state.set_state(AddProduct.product_2)
    await message.answer("Введите напиток 2:")


@router.message(AddProduct.product_2)
async def add_product_2(message: Message, state: FSMContext):
    await state.update_data(product_2=message.text)
    await state.set_state(AddProduct.product_3)
    await message.answer("Введите напиток 3:")


@router.message(AddProduct.product_3)
async def add_product_3(message: Message, state: FSMContext):
    data = await state.get_data()
    drinks = [data['product_1'], data['product_2'], message.text]
    drinks_db.extend(drinks)
    await message.answer("Напитки добавлены в меню.")
    await state.clear()


@router.message(Command('drinks'))
async def drinks_command(message: Message):
    if not drinks_db:
        await message.answer("Меню пока пустое")
        return

    drinks_list = "\n".join(f"- {drink}" for drink in drinks_db)
    await message.answer(f"Наши напитки:\n{drinks_list}")


@router.message(Command('mem'))
async def mem_command(message: Message, bot: Bot):
    photo = FSInputFile('media/mem.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

@router.message(F.text)
async def echo(message: Message):
    await message.answer(f"такой команды нет: {message.text}")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())