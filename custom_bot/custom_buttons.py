from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

u_kb=ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('расписание'),
                                                   KeyboardButton('больше меньше'))