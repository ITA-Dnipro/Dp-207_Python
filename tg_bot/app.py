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


@dp.message_handler()
async def post_city(message: types.message):
    commands = message.text.split()
    if commands[-1] == 'погода':
        res = await get_cities(commands[0])
        data = {'temp': res['temperature']}
        await message.reply(f'температура: {data["temp"]}')
    else:
        await message.reply(f'Неправильный формат', reply=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
