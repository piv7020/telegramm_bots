from aiogram.utils import executor
from aiogram import Bot,Dispatcher,types
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import random

from telegramm import aioparser

bot = Bot('5435708975:AAFV4x6YcTk4H-GfnHsHOlDNR4uc5AOTIpg')
dp = Dispatcher(bot)


list_of_jokes = []


@dp.message_handler(commands='start')
async def start_mes(message:types.Message):
    await bot.send_message(message.from_user.id,'привет я бот который отправляет тебе анекдоты',reply_markup=u_kb)


@dp.callback_query_handler(text='joke_button')
async def get_joke(callback_query:types.CallbackQuery):
    global list_of_jokes
    if len(list_of_jokes) == 0:
        await bot.send_message(callback_query.from_user.id,'в базе нет анекдотов')
    else:
        await bot.answer_callback_query(callback_query.from_user.id,'база данных успешно обновлена',show_alert=True)
        await bot.send_message(callback_query.from_user.id,"{ хочешь получить анекдот нажми кнопку ниже!",
                               reply_markup=u_kb)


@dp.callback_query_handler(text='joke_button')
async def get_joke(callback_query:types.CallbackQuery):
    global list_of_jokes
    try:
        list_of_jokes = await aioparser.parser.run_tasks()
        await bot.answer_callback_query(callback_query.from_user.id, 'база данных успешно обновлена', show_alert=True)
        await bot.send_message(callback_query.from_user.id, "{ хочешь получить анекдот нажми кнопку ниже!",
                               reply_markup=u_kb)
    except Exception as ex :
        await bot.send_message(callback_query.from_user.id,repr(ex),reply_markup=update_base_kb)




'''********************************buttons****************************'''


u_kb=InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('получить анекдот',
                                                                         callback_data='joke_button'))
update_base_kb=InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('обновить базу',
                                                                         callback_data='Update_button'))

if __name__ == '__main__':
    print('бот запущен')

    executor.start_polling(dp, skip_updates=True)