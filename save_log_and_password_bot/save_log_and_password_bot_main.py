from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from aiogram.dispatcher.filters import Text
from telegramm.save_log_and_password_bot.bot_db import *

import telegramm.save_log_and_password_bot.bot_db

bot = Bot('5435708975:AAFV4x6YcTk4H-GfnHsHOlDNR4uc5AOTIpg')
dp = Dispatcher(bot, storage=MemoryStorage())
admin_id = 965665251

users = {}


class FSMAdmin(StatesGroup):
    show_info = State()
    get_log = State()
    get_pass = State()
    accept = State()
    get_info = State()
    delete_accounts = State()
    delete_log=State()


@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'ввод отменён', reply_markup=u_s_k_b)
    await FSMAdmin.show_info.set()


@dp.message_handler(Text(equals=['добавить аккаунт','получить информацию','удалить все аккаунты','удалить аккаунт'],
                         ignore_case=True))
async def start_choice(message: types.Message, state: FSMContext):
    if message.text=='добавить аккаунт':
        await bot.send_message(message.from_user.id, 'введите логин', reply_markup=u_s_k_b)
        await FSMAdmin.get_log.set()

    elif message.text == 'удалить все аккаунты':
        await delete_all_acc(message)
        await state.finish()

    elif message.text == 'удалить аккаунт':
        await bot.send_message(message.from_user.id, 'введите аакаунт ,который ты хочешь удалить',
                               reply_markup=cancel_but)
        await FSMAdmin.delete_log.set()

    else:
        await sql_read_info(message=message)
        await state.finish()


@dp.message_handler(state=FSMAdmin.delete_log)
async def delete_acc(message:types.Message,state:FSMContext):
    await del_acc_db(message=message, login=message.text)
    await state.finish()


@dp.message_handler(commands='start')
async def start_mes(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await bot.send_message(message.from_user.id, 'выберите действие', reply_markup=u_s_k_b)
        await FSMAdmin.show_info.set()
    else:
        await bot.send_message(message.from_user.id, 'вы не админ')


@dp.message_handler(state=FSMAdmin.show_info)
async def send_inf(message: types.Message, state: FSMContext):
    if message.text == 'получить информацию':
        await sql_read_info(message=message)
        await state.finish()

    elif message.text == 'удалить все аккаунты':
        await delete_all_acc(message)
        await state.finish()

    elif message.text == 'удалить аккаунт':
        await bot.send_message(message.from_user.id, 'введите аакаунт ,который ты хочешь удалить',
                               reply_markup=cancel_but)
        await FSMAdmin.delete_log.set()

    else:
        await bot.send_message(message.from_user.id, 'введите логин', reply_markup=cancel_but)
        await FSMAdmin.get_log.set()


@dp.message_handler(state=FSMAdmin.get_log)
async def get_log(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    await FSMAdmin.get_pass.set()
    await bot.send_message(message.from_user.id, 'введите пароль', reply_markup=cancel_but)


@dp.message_handler(state=FSMAdmin.get_pass)
async def get_pas(message: types.Message, state: FSMContext):
    global login , password
    async with state.proxy() as data:
        data['password'] = message.text
    login = data.get('login')
    password = data.get('password')
    await bot.send_message(message.from_user.id, f'убедитесь что что всё верно логин:{login},'
                                                 f'пароль:{password}', reply_markup=accept_but)
    await FSMAdmin.accept.set()


@dp.message_handler(state=FSMAdmin.accept)
async def accept(message: types.Message, state: FSMContext):
    global login , password , users
    if message.text=='да':
        try:
            await sql_add_account(login=login, password=password)
            await bot.send_message(message.from_user.id, 'ваши данные успешно сохранены',
                                   reply_markup=u_s_k_b)
            await state.finish()
        except Exception as ex:
            print(repr(ex))
            await bot.send_message(message.from_user.id, 'такой логин уже есть',
                                   reply_markup=u_s_k_b)
            await FSMAdmin.show_info.set()
        # if message.text=='да':
        #     users[login] = password
        #     print(users)
        #     await state.finish()
        # else:
        #     await bot.send_message(message.from_user.id, f'ввод отменён выберите действие',reply_markup=u_s_k_b)
        #     await FSMAdmin.show_info.set()


# '''*********************************************BUTTONS********************************************'''

u_s_k_b = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('добавить аккаунт'))\
    .add(KeyboardButton('получить информацию'))\
    .add(KeyboardButton('удалить все аккаунты'))\
    .add(KeyboardButton('удалить аккаунт'))

cancel_but = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('отмена'))

accept_but = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('да')).add(KeyboardButton('нет'))

CHOISE_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('зарегистрироваться'))


if __name__ == '__main__':
    print('бот запущен')
    sql_start()
    executor.start_polling(dp, skip_updates=True)
