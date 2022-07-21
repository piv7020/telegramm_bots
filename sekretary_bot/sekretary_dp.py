import sqlite3 as sq
from sekretary_bot.sekretary_bot_main import dp, bot


def sql_start():
    global base, cur
    base = sq.connect('info.db')
    cur = base.cursor()
    if base:
        print('\nData base connect')
    base.execute(f'CREATE TABLE IF NOT EXISTS accounts(login PRIMARY KEY, password TEXT)')
    base.commit()


async def sql_add_account(login, question):
    global base, cur
    print(login, question)
    cur.execute(f'INSERT INTO accounts VALUES(?, ?)', (login, question))
    base.commit()


async def delete_all_acc(message):
    global cur, base
    try:
        sql_update_query = 'DELETE from accounts'
        cur.execute(sql_update_query)
        base.commit()
        await bot.send_message(message.from_user.id, 'все аккаунты удалены')
    except sq.Error as error:
        await bot.send_message(message.from_user.id, f'произошла ошибка в работе с базой данных:\n{error} ')


async def sql_read_info(message):
    try:
        acc_count = 0
        accounts = ''

        for info in cur.execute('SELECT * FROM accounts').fetchall():
            acc_count += 1
            accounts += f'\n Аккаунт: {acc_count}\nЛогин: {info[0]}Пароль:{info[1]}'
        await bot.send_message(message.from_user.id, accounts)

    except:
        await bot.send_message(message.from_user.id, 'Добавленных аккаунтов нет')


async def del_acc_db(message, login):
    global cur, base
    try:
        count = 0
        for log in cur.execute("SELECT * FROM accounts").fetchall():
            if log[0] == login:
                sql_udate_query = 'DELETE from accounts where login=?'
                cur.execute(sql_udate_query, (login,))
                base.commit()
                await bot.send_message(message.from_user.id, f'аккаунт {login} успешно удалён')
                count += 1
                break
        if count == 0:
            await bot.send_message(message.from_user.id, f'аккаунт {login} не найден')
    except sq.Error as error:
        await bot.send_message(message.from_user.id, 'ошибка при  работе с базой данных')



async def show_quest_db(message):

    try:
        acc_count = 0
        accounts = ''

        for info in cur.execute('SELECT * FROM accounts').fetchall():
            acc_count += 1
            accounts += f'\n Аккаунт: {acc_count}\nЛогин: {info[0]} задача:{info[1]}'
        await bot.send_message(message.from_user.id, accounts)

    except:
        await bot.send_message(message.from_user.id, 'Добавленных аккаунтов нет')