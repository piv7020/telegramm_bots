from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os
import aiofiles
from custom_bot.custom_buttons import u_kb
from custom_bot.custom_config import num,count_of_attempts
from aiogram.dispatcher.filters import Text


logging.basicConfig(level=logging.DEBUG,filename='mylog.log',
                    format='%(asctime)s | %(levelname)s | %(funcName)s: %(lineno)d | %(message)s',
                    datefmt='%H:%M:%S')


bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def st_mes(message: types.Message):

    await bot.send_message(message.from_user.id, f'привет {message.from_user.full_name},я бот который'
                                                 f'с каждым днём получает новые функции')


    await bot.send_message(message.from_user.id,f'выбери функцию которой воспользуешься',reply_markup=u_kb)


@dp.message_handler(text='больше меньше')
async def st_mes(message: types.Message):
    if count_of_attempts == 1:
        await bot.send_message(message.from_user.id,
                               text=f'{message.from_user.full_name},я загадал число от 1 до 100'
                                    f' теперь попробуй его угадать')
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

    except ValueError:
        await bot.send_message(message.from_user.id,
                               text=f'пиши целое число')





















if __name__ == '__main__':
    print('бот запущен')
    executor.start_polling(dp)