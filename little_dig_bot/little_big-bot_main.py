from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os
import aiofiles
import random
from telegramm.little_dig_bot.config import num, count_of_attempts


logging.basicConfig(level=logging.DEBUG,filename='mylog.log',
                    format='%(asctime)s | %(levelname)s | %(funcName)s: %(lineno)d | %(message)s',
                    datefmt='%H:%M:%S')


bot = Bot('5435708975:AAFV4x6YcTk4H-GfnHsHOlDNR4uc5AOTIpg')
dp = Dispatcher(bot)




@dp.message_handler(commands='start')
async def st_mes(message: types.Message):
    if count_of_attempts == 1:
        await bot.send_message(message.from_user.id,
                               text=f'привет,{message.from_user.full_name},я загадал число теперь'
                                    f' пробуй его угадать')
    else:
        await bot.send_message(message.from_user.id, text='введите число')


@dp.message_handler()
async def info(message: types.Message):


    try:
        global count_of_attempts, num
        if int(message.text) == num:
            await message.answer(f'Поздравляю ты угадал.\nКоличество попыток: {count_of_attempts}')
            count_of_attempts=1

        elif int(message.text) > num:
            await message.answer(f'Твоё число больше загаданного.\nПопробуй ввести число ещё раз')
            count_of_attempts+=1

        else:
            await message.answer(f'Твоё число меньше загаданного.\nПопробуй ещё раз')
            count_of_attempts += 1

    except :
        await bot.send_message(message.from_user.id,
                               text=f'пиши целое число')



if __name__ == '__main__':
    print('бот запущен')
    executor.start_polling(dp)
