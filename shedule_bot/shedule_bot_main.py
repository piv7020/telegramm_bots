from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
import aiofiles
import random
from aiogram.dispatcher.filters import Text
from telegramm.shedule_bot.config_shedule import shedule
import datetime
from telegramm.shedule_bot.buttons import u_kb

bot = Bot('5435708975:AAFV4x6YcTk4H-GfnHsHOlDNR4uc5AOTIpg')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def st_mes(message: types.Message):
    await bot.send_message(message.from_user.id,f'привет {message.from_user.first_name},я бот который'
                                                f' подскажет тебе расписание',reply_markup=u_kb
                                                )


@dp.message_handler(Text(equals=shedule.keys(),ignore_case=True))
async def  get_all(message: types.Message):
    msg =shedule[message.text]
    await bot.send_message(message.from_user.id,f'<b>{msg}<b>',parse_mode=types.ParseMode.HTML)



@dp.message_handler(Text(equals=('сегодня'),ignore_case=True))
async def  g_sh(message: types.Message):
    msg=shedule[
        list(shedule.keys())[datetime.datetime.now().weekday()]
    ]
    await bot.send_message(message.from_user.id,f'<b>{msg}<b>',parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals=('завтра'),ignore_case=True))
async def  g_sh_tom(message: types.Message):
    msg=shedule[
        list(shedule.keys())[datetime.datetime.now().weekday()+1]
    ]
    await bot.send_message(message.from_user.id,f'<b>{msg}<b>',parse_mode=types.ParseMode.HTML)

if __name__ == '__main__':
    print('бот запущен')
    executor.start_polling(dp)

