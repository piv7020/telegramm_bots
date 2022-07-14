from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,InlineKeyboardMarkup,\
    InlineKeyboardButton
from aiogram.utils import executor
import logging
import os
import datetime


logging.basicConfig(level=logging.DEBUG,filename='mylog.log',
                    format='%(asctime)s | %(levelname)s | %(funcName)s: %(lineno)d | %(message)s',
                    datefmt='%H:%M:%S')


bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def star_mes(message:types.Message):
    await bot.send_message(message.from_user.id,f'привет {message.from_user.first_name},я бот который отправит тебеа '
                                                f' твоё же сообщение',reply_markup=u_kb)

    await bot.send_message(message.from_user.id,f'можешь узнать дату',reply_markup=user_i_kb)


@dp.message_handler(text='пожелание доброго утра')
async def  gm(message:types.Message):
    await bot.send_message(message.from_user.id,f'доброе утро')


@dp.message_handler(text='пожелание доброй ночи')
async def gn(message:types.Message):
    await bot.send_message(message.from_user.id,f'доброй ночи')


@dp.callback_query_handler(text='button_date')
async def reply_mes(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, 'кнопка сработала')


    now_date=datetime.datetime.now()
    await bot.send_message(callback_query.from_user.id,f'{now_date.strftime("%d,%m,%Y,%H:%M:%S")}')


@dp.message_handler(text='время🕰️')
async def r_t(message:types.Message):
    now_date = datetime.datetime.now()
    await bot.send_message(message.from_user.id,f'{now_date.strftime("%d,%m,%Y,%H:%M:%S")}')

@dp.message_handler()
async def reply_m(message:types.Message):
    await message.reply(message.text)





'''***************************  bUtToNs  ******************************************************'''

button_gm = KeyboardButton('пожелание доброго утра')
button_gn = KeyboardButton('пожелание доброй ночи')
time = KeyboardButton('время🕰️')

# u_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_gm).add(button_gn)
u_kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).row(button_gm,button_gn,time)


button_date = InlineKeyboardButton(text='время и дата',callback_data='button_date')
user_i_kb=InlineKeyboardMarkup(resize_keyboard=True).row(button_date)


if __name__ == '__main__':
    print('бот запущен')
    executor.start_polling(dp)
