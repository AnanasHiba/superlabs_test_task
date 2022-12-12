from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
import requests
import random

API_TOKEN = '*'
url = "https://paper-trader.frwd.one"

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

timeframe_list = ['5m', '15m', '1h', '4h', '1d', '1w', '1M']

@dp.message_handler(commands=["start"])
async def command_start_handler(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}! \nYou can start with sending a trading pair")

@dp.message_handler()
async def send_welcome(message: types.Message):
	payload={'candles': random.randint(50,1000),
	'ma': random.randint(10,100),
	'pair': message.text,
	'sl': random.randint(1,50),
	'timeframe': timeframe_list[random.randrange(7)],
	'tp': random.randint(1,50)}

	response = requests.request("POST", url, data=payload)

	try:
		root = BeautifulSoup(response.content, 'html5lib')
		await message.answer_photo(url + root.body.img['src'][1:])
	except:
		await message.answer('Error occurred')

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)