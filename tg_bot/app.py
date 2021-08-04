import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import aiohttp


load_dotenv()


API_TOKEN = os.getenv('BOT_TOKEN')


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def get_cities(message):
    async with aiohttp.ClientSession() as session:
        async with session.post(os.environ.get('API_CITIES'), json={'city': message}) as res:
            return await res.json()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.message):
    await message.reply('Hello')


@dp.message_handler(commands=['weather'])
async def send_welcome(message: types.message):
    res = await get_cities()
    await message.reply(res)


@dp.message_handler()
async def post_city(message: types.message):
    res = await get_cities(message.text)
    data = {'temp': res['temperature']}
    await message.reply(f'температура: {data["temp"]}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)