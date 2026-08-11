from decouple import config

from aiogram import Bot, Dispatcher, Router, F
import asyncio
from aiogram.filters import Command
from datetime import datetime
from aiogram.types import Message, FSInputFile
import logging
import random

token = config('BOT_TOKEN')

router = Router()

@router.message(Command("start"))
async def start_command(message: Message, bot: Bot):
    await message.answer("Напиши мне  свое имя")
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот, который поможет тебе с твоими задачами.")


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("/start - начать работу с ботом\n/help - помощь")


@router.message(Command('menu'))
async def menu_command(message: Message):
    keyboard = [
        [("Время", "time"), ("Случайное число", "random")],
        [("Анекдот", "joke"), ("Мем", "mem")],
    ]
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
    dp = Dispatcher()
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())