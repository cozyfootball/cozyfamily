# -*- coding: utf-8 -*-
import io
import random
import logging
import sqlite3
import datetime as dt
import pandas as pd
import os
from pathlib import Path
from aiogram.dispatcher.filters import BoundFilter
from random import shuffle
from datetime import datetime, timezone
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.types import ParseMode, CallbackQuery, message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import text, bold  # , italic, code, pre
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# База данных
bd = sqlite3.connect('stom.db')
cur = bd.cursor()
bd.commit()
bd.execute(
    'CREATE TABLE IF NOT EXISTS Users'
    '(id int NOT NULL, '
    'phone NULL, '
    'instanse NULL, '
    'real_name NULL, '
    'date_birth int NULL, '
    'serv_book int NULL, '
    'garante NULL, '
    'main_recom int, '
    'plan NULL, '
    'photoproc NULL, '
    'secret_key int, '
    'doctor NULL, '
    'PRIMARY KEY(phone))')

bd.execute(
    'CREATE TABLE IF NOT EXISTS Meets'
    '(id_meets int NOT NULL,'
    'id int NULL,'
    'date NULL, '
    'time NULL, '
    'price NULL, '
    'price_state NULL, '
    'plan NULL, '
    'recomend NULL,'
    'act NULL,'
    'approve NULL,'
    'real_date NULL,'
    'real_name NULL,'
    'UNIQUE(id_meets))')

bd.commit()

# Фильтр на админов
my_admin_id = []


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.from_user.id in my_admin_id:
            return True

# Стейты
class Change(StatesGroup):
    ChangeMeet = State()

class Phone(StatesGroup):
    PhoneSearch = State()

class Client(StatesGroup):
    ClientUp = State()
    ClientUpp = State()

# Все кнопки бота
b1 = types.InlineKeyboardButton(text="Мой кабинет🦷", callback_data="MyButton1")
b2 = types.InlineKeyboardButton(text="Перезвоните мне☎", callback_data="MyButton3")
b3 = types.InlineKeyboardButton(text="Записаться✏️", callback_data="MyButton3")
b4 = types.InlineKeyboardButton(text="О нас👩🏼‍⚕️", callback_data="MyButton4")
b5 = types.InlineKeyboardButton(text="Админка⚙️", callback_data="MyButton5")
b6 = types.InlineKeyboardButton(text="Сервисная книжка📖", callback_data="MyButton6")
b7 = types.InlineKeyboardButton(text="Адрес📪", callback_data="MyButton7")
b8 = types.InlineKeyboardButton(text="Канал📲", callback_data="MyButton8")
b9 = types.InlineKeyboardButton(text="Акции🧮", callback_data="MyButton9")
b10 = types.InlineKeyboardButton(text="История посещений📆", callback_data="MyButton10")
b11 = types.InlineKeyboardButton(text="План лечения📈", callback_data="MyButton11")
b12 = types.InlineKeyboardButton(text="Условия гарантии🗞", callback_data="MyButton12")
b13 = types.InlineKeyboardButton(text="🧼телефон", callback_data="MyButton13")
b14 = types.InlineKeyboardButton(text="🧼фио", callback_data="MyButton14")
b15 = types.InlineKeyboardButton(text="🧼др", callback_data="MyButton15")
b16 = types.InlineKeyboardButton(text="Сайт💻", callback_data="MyButton16")
b17 = types.InlineKeyboardButton(text="🧼серв книга", callback_data="MyButton17")
b18 = types.InlineKeyboardButton(text="🧼гарантия", callback_data="MyButton18")
b19 = types.InlineKeyboardButton(text="🧼общ рекоменд", callback_data="MyButton19")
b20 = types.InlineKeyboardButton(text="🧼ключ пациента", callback_data="MyButton20")
b21 = types.InlineKeyboardButton(text="Обновить📝", callback_data="MyButton21")
b22 = types.InlineKeyboardButton(text='Записи🔏', callback_data="MyButton22")
b24 = types.InlineKeyboardButton(text="Фотопротокол📸", callback_data="MyButton24")
b25 = types.InlineKeyboardButton(text="Акт📜", callback_data="MyButton25")
b26 = types.InlineKeyboardButton(text="план лечения📜", callback_data="MyButton26")
b27 = types.InlineKeyboardButton(text="фотопротокол📜", callback_data="MyButton27")
b30 = types.InlineKeyboardButton(text="Добавить запись✅", callback_data="MyButton30")
b31 = types.InlineKeyboardButton(text="Изменить запись🧩", callback_data="MyButton31")
b32 = types.InlineKeyboardButton(text="Удалить❌", callback_data="MyButton32")
b34 = types.InlineKeyboardButton(text="Корректировать✂️", callback_data="MyButton34")
b28 = types.InlineKeyboardButton(text="🧼id", callback_data="MyButton28")
b40 = types.InlineKeyboardButton(text="🧼дата", callback_data="MyButton40")
b41 = types.InlineKeyboardButton(text="🧼время", callback_data="MyButton41")
b42 = types.InlineKeyboardButton(text="🧼цена", callback_data="MyButton42")
b43 = types.InlineKeyboardButton(text="🧼оплата", callback_data="MyButton43")
b44 = types.InlineKeyboardButton(text="🧼план", callback_data="MyButton44")
b45 = types.InlineKeyboardButton(text="🧼рекомендации", callback_data="MyButton45")
b51 = types.InlineKeyboardButton(text="💾план лечения", callback_data="MyButton51")
b52 = types.InlineKeyboardButton(text="💾фотопротокол", callback_data="MyButton52")
b53 = types.InlineKeyboardButton(text="Админы🗿", callback_data="MyButton53")
b55 = types.InlineKeyboardButton(text="Пациенты🌝", callback_data="MyButton55")
b59 = types.InlineKeyboardButton(text="Запросить🔔", callback_data="MyButton59")
b61 = types.InlineKeyboardButton(text="✅Я приду", callback_data="MyButton61")
b62 = types.InlineKeyboardButton(text="🚷Я не приду", callback_data="MyButton62")
b66 = types.InlineKeyboardButton(text="Статус🎒", callback_data="MyButton66")
b77 = types.InlineKeyboardButton(text="По номеру⚠️", callback_data="MyButton77")
b89 = types.InlineKeyboardButton(text="Внести как пациента📩", callback_data="MyButton89")
b98 = types.InlineKeyboardButton(text="Внести как пациента📩", callback_data="MyButton98")
b95 = types.InlineKeyboardButton(text="Внести как админа👩🏻‍🎓", callback_data="MyButton95")


# Старт бота
@dp.message_handler(CommandStart(), state="*")
async def send_welcome(message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    # получим все ID админов
    admins = cur.execute('SELECT id FROM Users WHERE instanse == "admin"').fetchall()
    admin_list = [x[0] for x in admins]
    for i in admin_list:
        if i not in my_admin_id:
            my_admin_id.append(i)
    # получим все ID админов клиентов
    friends = cur.execute('SELECT id FROM Users WHERE instanse = "friend"').fetchall()
    friends_list = [x[0] for x in friends]
    # создадим клавиатуры для каждой категории
    guest_keyboard = types.InlineKeyboardMarkup(row_width=1)
    friend_keyboard = types.InlineKeyboardMarkup(row_width=1)
    admin_keyboard = types.InlineKeyboardMarkup(row_width=1)
    guest_keyboard.add(b4, b2)
    friend_keyboard.add(b1, b2, b4)
    admin_keyboard.add(b1, b4, b5)
    # Клиентское меню
    if user_id in friends_list:
        text_message_g = f'Здраствуйте, {user_name}'
        start_message = await bot.send_message(user_id, text_message_g, reply_markup=friend_keyboard)
        await bot.pin_chat_message(user_id, start_message.message_id)
    # Админское менюЫФВЫФВЫФВ
    elif user_id in admin_list or user_id in []:
        info_for_ad = (f'*🔱ИНСТРУКЦИЯ ДЛЯ АДМИНИСТРАТОРОВ🔱*\n'
                       f' \n'
                       f'*Как добавить нового пациента?*\n'
                       f'⚠️*Способ 1.* Отправить боту контакт пациента(мобильная версия)\n'
                       f'⚠️*Способ 2.* Админка ==> По номеру ==> ввести номер телефона в формате 89296081589 ==> после того как номер телефона не будет найден в базе, нажать кнопку "Внести как пациента"\n'
                        f'⚠️*Способ 3.* Отправить типовой шаблон боту и в комментарии написать "бд"\n'
                         f' \n'
                        f'*Как обновить информацию по пациенту?*\n'
                       f'⚠️*Способ 1.* Для обновления информации через чат с ботом необходимо сначала найти пациента в базе данных.\n'
                       f'🔎Поиск юзера в базе: отправить контакт или админка(по номеру) или админка(пациенты).\n'
                        f'Для изменения текстовой информации(профиль юзера, записи) необходимо отправлять текстовоые сообщения и нажимать соответствующую кнопку обновления:\n'
                       f'Для изменения файлов по пациенту необходимо отправить боту файл в виде документа и в комментарии написать "обновить"\n'
                       f'⚠️*Способ 2.*Отправить типовой шаблон боту и в комментарии написать "бд"\n'
                       )
        await bot.send_message(user_id, info_for_ad,
                                               parse_mode='MarkDown')

        text_message_g = (
                          f'*Всего пользователей:* {len(admin_list) + len(friends_list)}\n'
                          f'*Администраторы:* {len(admin_list)}\n'  
                          f'*Пациенты:* {len(friends_list)}\n'
                          )
        start_message = await bot.send_message(user_id, text_message_g, reply_markup=admin_keyboard,
                                               parse_mode='MarkDown')

        await bot.pin_chat_message(user_id, start_message.message_id)
    # Сценарий для юзеров не из базы
    else:
        text_message_g = 'Цифровая стомоталогия - реставрация зубов'
        await bot.send_message(user_id, text_message_g, reply_markup=guest_keyboard)

# Кабинет клиента
user_path = []
@dp.callback_query_handler(text=['MyButton10'], state="*")
async def MyCabinet(call, state: FSMContext):
    user_id = call.from_user.id
    # Получим все записи
    my_meets = cur.execute('SELECT date, time, plan, price, price_state FROM Meets WHERE id=? ORDER BY real_date DESC', (user_id,)).fetchall()
    meets_count = len(my_meets)
    dates = []
    time = []
    plan = []
    price = []
    price_state = []
    for i in my_meets:
        dates.append(i[0])
        time.append(i[1])
        plan.append(i[2])
        price.append(i[3])
        price_state.append(i[4])
    aps = f'Всего записей на приём: {meets_count}\n'
    for i in range(len(dates)):
        mes = f'*Дата* {dates[i]} *Время* {time[i]} *{price_state[i]}* {price[i]}\n*План лечения* {plan[i]}'
        aps = aps + mes + '\n'
    # Создадим клавиатуру с кнопкой по каждой записи
    f_keyboard = types.InlineKeyboardMarkup(row_width=1)
    user_path.clear()
    for i in dates:
        f_keyboard.add(types.InlineKeyboardButton(text=i, callback_data=i), b25)
        user_path.append(i)
    await bot.send_message(chat_id=user_id,
                           text=aps, parse_mode='MarkDown', reply_markup=f_keyboard)
update_user = []

# Файлы с данными
@dp.callback_query_handler(text=['MyButton11', 'MyButton24', 'MyButton26', 'MyButton27'], state="*")
async def MyCallBack11(call, state: FSMContext):
    user_id = call.from_user.id
    if call.data == 'MyButton11':
        my_file = cur.execute('SELECT plan FROM Users WHERE id = ?', (user_id,)).fetchone()
        if my_file[0] is not None:
            file = open(my_file[0], 'rb')
            await bot.send_document(call.from_user.id, file)

        else:
            await bot.send_message(chat_id=user_id,
                                   text='План лечения пока не подгружен в базу. За подробной информацией обратитесь к администратору')
    elif call.data == 'MyButton24':
        my_file = cur.execute('SELECT photoproc FROM Users WHERE id = ?', (user_id,)).fetchone()
        if my_file[0] is not None:
            file = open(my_file[0], 'rb')
            await bot.send_document(call.from_user.id, file)
        else:
            await bot.send_message(chat_id=user_id,
                                   text='Фотопротокол пока не подгружен в базу. За подробной информацией обратитесь к администратору')
    elif call.data == 'MyButton26':
        my_file = cur.execute('SELECT plan FROM Users WHERE id = ?', (update_user[-1],)).fetchone()
        if my_file[0] is not None:
            file = open(my_file[0], 'rb')
            await bot.send_document(call.from_user.id, file)

        else:
            await bot.send_message(chat_id=user_id,
                                   text='План лечения пока не подгружен в базу.')
    elif call.data == 'MyButton27':
        my_file = cur.execute('SELECT photoproc FROM Users WHERE id = ?', (update_user[-1],)).fetchone()
        if my_file[0] is not None:
            file = open(my_file[0], 'rb')
            await bot.send_document(call.from_user.id, file)
        else:
            await bot.send_message(chat_id=user_id,
                                   text='Фотопротокол пока не подгружен в базу.')


# Админка
@dp.callback_query_handler(text=['MyButton5'], state="*")
async def MyCallBack5(call, state: FSMContext):
    user_id = call.from_user.id
    all_meets = cur.execute('SELECT COUNT(*) FROM Meets').fetchone()
    all_users = cur.execute('SELECT COUNT(*) FROM Users').fetchone()
    ad_keyboard = types.InlineKeyboardMarkup(row_width=1)
    ad_keyboard.add(b55, b53, b66, b77)
    admins_info = f'Общий статус: пользователей - {all_users[0]} записей - {all_meets[0]}'
    await bot.send_message(user_id, admins_info,
                           reply_markup=ad_keyboard)



@dp.callback_query_handler(text=['MyButton66'], state="*")
async def MyCallBack66(call, state: FSMContext):
    user_id = call.from_user.id
    current_date = cur.execute('SELECT date()').fetchone()
    next_date =  cur.execute("SELECT date('now','+14 days')").fetchone()
    true_rows = cur.execute('SELECT date, time, id, price, price_state, approve, real_name FROM Meets WHERE real_date >=? AND real_date <= ? ORDER BY real_date DESC', (current_date[0], next_date[0], )).fetchall()
    dates = []
    times = []
    id = []
    prices = []
    price_state = []
    approve = []
    real_names = []
    for i in true_rows:
        dates.append(i[0])
        times.append(i[1])
        id.append(i[2])
        prices.append(i[3])
        price_state.append(i[4])
        approve.append(i[5])
        real_names.append(i[6])

    dontget_money = 0
    get_money = 0
    for i in range(len(prices)):
        if price_state[i] == 'оплачено':
            get_money += int(prices[i])
        elif price_state[i] == 'не оплачено':
            dontget_money += int(prices[i])

    aps = (f'*Ближайшие записи*\n'
        f'Всего: *{len(dates)}* записей\n'
        f'Всего начислено: *{get_money+dontget_money}* руб.\n'
        f'Оплачено: *{get_money}* руб.\n'
        f'К оплате: *{dontget_money}* руб.\n'
           f' \n')

    for i in range(len(dates)):
        mes = f' \nДата* {dates[i]}* Время* {times[i]}* Пациент* {real_names[i]} {prices[i]} *руб. *{price_state[i]}* Посещение* {approve[i]}*'
        aps = aps + mes + '\n'
    app_keyb = types.InlineKeyboardMarkup(row_width=1)
    app_keyb.add(b59,b5)
    await bot.send_message(user_id, aps, parse_mode='MarkDown', reply_markup=app_keyb)




@dp.callback_query_handler(text=['MyButton59'], state="*")
async def MyCallBack59(call, state: FSMContext):
    user_id = call.from_user.id
    current_date = cur.execute('SELECT date()').fetchone()
    next_date = cur.execute("SELECT date('now','+3 days')").fetchone()
    true_rows = cur.execute(
        'SELECT date, time, id, price, price_state, approve, real_name, id_meets FROM Meets WHERE real_date >=? AND real_date <= ? ORDER BY real_date DESC',
        (current_date[0], next_date[0],)).fetchall()
    dates = []
    times = []
    id = []
    prices = []
    price_state = []
    approve = []
    real_names = []
    id_meets = []
    for i in true_rows:
        dates.append(i[0])
        times.append(i[1])
        id.append(i[2])
        prices.append(i[3])
        price_state.append(i[4])
        approve.append(i[5])
        real_names.append(i[6])
        id_meets.append(i[7])
    client_keyboard = types.InlineKeyboardMarkup(row_width=1)
    client_keyboard.add(b61, b62)
    for i in range(len(id)):
        checking = cur.execute("SELECT phone FROM Users WHERE id=?", (id[i],)).fetchone()

        if approve[i] == 'не запрошено' and str(checking[0])!= id[i]:
            client_approve_mes = (f'Здраствуйте *{real_names[i]}*. Вы записаны на лечение *{dates[i]} в {times[i]}*\n'
                              f'К оплате *{prices[i]} руб.* статус оплаты *{price_state[i]}*\n'
                              f'Просим Вас *подтвердить* своё посещение.')
            client_keyboard = types.InlineKeyboardMarkup(row_width=1)
            client_keyboard.add(b61,b62)
            try:
                await bot.send_message(id[i], client_approve_mes,
                           reply_markup=client_keyboard, parse_mode='MarkDown')
                cur.execute('UPDATE Meets SET approve=? WHERE id_meets=?', ('запрошено', id_meets[i],))
                bd.commit()
                z_keyboard = types.InlineKeyboardMarkup(row_width=1)
                z_keyboard.add(b5)
                await bot.send_message(user_id, f'Запрос на подтверждение был направлен {real_names[i]}')
            except:
                pass
        elif str(checking[0])==str(id[i]):
            await bot.send_message(user_id, f'Не удалось отправить уведомление юзеру {real_names[i]}. Так как у него не указан корректный ID')



my_call_clients = []
# Список всех клиентов для админа
@dp.callback_query_handler(text=['MyButton55', 'MyButton53'], state="*")
async def MyCallBack55(call, state: FSMContext):
    user_id = call.from_user.id
    if call.data == 'MyButton55':
        user_all = cur.execute('SELECT real_name FROM Users WHERE real_name IS NOT NULL AND instanse == "friend"').fetchall()
        user_name_list = [x[0] for x in user_all]
        f_keyboard = types.InlineKeyboardMarkup(row_width=1)
        my_call_clients.clear()
        for i in user_name_list:
            f_keyboard.add(types.InlineKeyboardButton(text=i, callback_data=i))
            my_call_clients.append(i)
        await bot.send_message(user_id, f'Cписок всех пациентов',
                           reply_markup=f_keyboard)
    elif call.data == 'MyButton53':
        user_all = cur.execute('SELECT real_name FROM Users WHERE instanse == "admin"').fetchall()
        user_name_list = [x[0] for x in user_all]
        f_keyboard = types.InlineKeyboardMarkup(row_width=1)
        my_call_clients.clear()
        for i in user_name_list:
            f_keyboard.add(types.InlineKeyboardButton(text=i, callback_data=i))
            my_call_clients.append(i)
        await bot.send_message(user_id, f'Cписок всех админов',
                           reply_markup=f_keyboard)



# Поиск по номеру телефона текстом
@dp.callback_query_handler(text=['MyButton77'], state="*")
async def MyCallBack77(call, state: FSMContext):
    user_id = call.from_user.id
    await bot.send_message(user_id, f'Отправьте в следующем сообщении последние 10 цифр телефона. Пример: 9296086665')
    await Phone.PhoneSearch.set()


@dp.message_handler(IsAdmin(), state=Phone.PhoneSearch)
async def MyCallBack777(message: types.Message, state: FSMContext):
    mes = message.text
    user_id = message.from_user.id
    if len(message.text) == 10:
        check_user = cur.execute('SELECT id, phone, instanse, real_name, date_birth, serv_book, garante, main_recom, secret_key FROM Users WHERE phone == ?', (mes,)).fetchone()
        if user_id in [1757558411, 29720838] and check_user is None:
            add_keyboard = types.InlineKeyboardMarkup(row_width=1)
            add_keyboard.add(b98,b95)
            await message.answer(
                'В базе отсутствует пользователь с этим номером. Я могу добавить этот номер, но для доступа в личный кабинет, понадобится секретный ключ. Добавить пользователя как пациента или как админа?',
                reply_markup=add_keyboard)
            new_client.clear()
            new_client.append(mes)
            await state.reset_state()
        elif check_user is None:
            add_keyboard = types.InlineKeyboardMarkup(row_width=1)
            add_keyboard.add(b98)
            await message.answer(
                'В базе отсутствует пользователь с этим номером. Я могу добавить этот номер, но для доступа в личный кабинет, понадобится секретный ключ. Добавить пользователя как пациента?',
                reply_markup=add_keyboard)
            new_client.clear()
            new_client.append(mes)
            await state.reset_state()
        else:
            myansw = (f'*Профиль пациента*\n'
                      f'*ID*: {check_user[0]}\n'
                      f'*Телефон*: {check_user[1]}\n'
                      f'*Статус*: {check_user[2]}\n'
                      f'*ФИО*:{check_user[3]}\n'
                      f'*День рождения*:{check_user[4]}\n'
                      f'*Сервисная книга*:\n{check_user[5]}\n'
                      f'*Условия гарантии*:\n{check_user[6]}\n'
                      f'*Общие рекомендации*:\n{check_user[7]}\n'
                      f'*Ключ подключения*: {check_user[8]}\n'
                      )
            cor_keyb = types.InlineKeyboardMarkup(row_width=1)
            cor_keyb.add(b21,b22,b26,b27)
            await message.answer(myansw, parse_mode='MarkDown', reply_markup=cor_keyb)
            await state.reset_state()
            update_user.clear()
            update_user.append(check_user[0])

    else:
        await message.answer(
            'Номер не соотвествует заданному формату.  Пример формата: 9296086665')
        await state.reset_state()

# История записей клиента
@dp.callback_query_handler(text=['MyButton22'], state="*")
async def MyCallBack21(call, state: FSMContext):
    user_id = update_user[-1]
    my_meets = cur.execute('SELECT date, time, price, price_state, plan, approve FROM Meets WHERE id=? ORDER BY real_date DESC', (user_id,)).fetchall()
    meets_count = len(my_meets)
    aps = f'Всего записей на приём: {meets_count}\n'
    if meets_count > 0:
        dates = []
        time = []
        plan = []
        price = []
        price_state = []
        approves = []
        for i in my_meets:
            dates.append(i[0])
            time.append(i[1])
            plan.append(i[4])
            price.append(i[2])
            price_state.append(i[3])
            approves.append([i[5]])
        for i in range(len(dates)):
            mes = f'*Дата* {dates[i]} *Время* {time[i]} *{price_state[i]}* {price[i]} руб. *Подтверждение* {approves[i]}\n*План лечения* {plan[i]}'
            aps = aps + mes + '\n'
        f_keyboard = types.InlineKeyboardMarkup(row_width=1)
        f_keyboard.add(b30, b31, b5)
        await bot.send_message(chat_id=call.from_user.id,
                               text=aps, parse_mode='MarkDown', reply_markup=f_keyboard)
    elif meets_count == 0:
        f_keyboard = types.InlineKeyboardMarkup(row_width=1)
        f_keyboard.add(b30,b5)
        await bot.send_message(chat_id=call.from_user.id,
                               text=aps, parse_mode='MarkDown', reply_markup=f_keyboard)

# Добавить запись по клиенту
@dp.callback_query_handler(text=['MyButton30'], state="*")
async def MyCallBack30(call, state: FSMContext):
    user_id = update_user[-1]
    last_ids = cur.execute("SELECT id_meets FROM Meets ORDER BY id_meets DESC LIMIT 1").fetchone()
    new_id = last_ids[0] + 1
    real_name = cur.execute("SELECT real_name FROM Users WHERE id=?", (user_id, )).fetchone()
    cur.execute('INSERT INTO Meets(id_meets, id, date, price_state, approve, real_name) VALUES(?,?,?,?,?,?)', (new_id, user_id, 'новая запись', 'не оплачено', 'не запрошено', real_name[0]))
    create_add = cur.execute("SELECT * FROM Meets WHERE id_meets=" + str(new_id)).fetchone()
    new_add = (f'Номер *{create_add[0]}*\n'
               f'ФИО *{create_add[11]}*\n'
               f'Дата *{create_add[2]}*\n'
               f'Время *{create_add[3]}*\n'
               f'Цена *{create_add[4]}*\n'
               f'Статус оплаты *{create_add[5]}*\n'
               f'Подтверждение  *{create_add[9]}*\n'
               f'План лечения *{create_add[6]}*\n'
               f'Рекомендации *{create_add[7]}*\n')
    time_keyboard = types.InlineKeyboardMarkup(row_width=1)
    time_keyboard.add(b40,b41,b42,b43,b44,b45,b22,b5)
    await bot.send_message(chat_id=call.from_user.id,
                           text=new_add, parse_mode='MarkDown', reply_markup=time_keyboard)
    last_id.clear()
    last_id.append(new_id)


buf = []
last_id = []
@dp.callback_query_handler(IsAdmin(),
                           text=['MyButton40', 'MyButton41', 'MyButton42', 'MyButton43', 'MyButton44', 'MyButton45'],
                           state="*")
async def MyCallBackUpdaterZap(call, state: FSMContext):
    user_id = call.from_user.id
    if call.data == 'MyButton40':
        cur.execute('UPDATE Meets SET date=? WHERE id_meets =?', (buf[0], last_id[-1],)).fetchone()
        finish = buf[-1].split(".")
        finish_date = f'{finish[2]}-{finish[1]}-{finish[0]}'
        cur.execute('UPDATE Meets SET real_date=? WHERE id_meets =?', (finish_date, last_id[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton41':
        cur.execute('UPDATE Meets SET time=? WHERE id_meets =?', (buf[0], last_id[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton44':
        cur.execute('UPDATE Meets SET plan=? WHERE id_meets =?', (buf[0], last_id[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton42':
        cur.execute('UPDATE Meets SET price=? WHERE id_meets =?', (buf[0], last_id[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton43':
        cur.execute('UPDATE Meets SET price_state=? WHERE id_meets =?', (buf[0], last_id[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton45':
        cur.execute('UPDATE Meets SET recomend=? WHERE id_meets =?', (buf[0], last_id[-1],)).fetchone()
        bd.commit()
    create_add = cur.execute("SELECT * FROM Meets WHERE id_meets=?", (last_id[-1],)).fetchone()
    new_add = (f'Номер *{create_add[0]}*\n'
               f'ФИО *{create_add[11]}*\n'
               f'Дата *{create_add[2]}*\n'
               f'Время *{create_add[3]}*\n'
               f'Цена *{create_add[4]}*\n'
               f'Статус оплаты *{create_add[5]}*\n'
               f'Подтверждение визита *{create_add[9]}*\n'
               f'План лечения *{create_add[6]}*\n'
               f'Рекомендации *{create_add[7]}*\n')
    time_keyboard = types.InlineKeyboardMarkup(row_width=1)
    time_keyboard.add(b40, b41, b42, b43, b44, b45, b22, b5)
    await bot.send_message(chat_id=call.from_user.id,
                           text=new_add, parse_mode='MarkDown', reply_markup=time_keyboard)

# Вывод списка записей по юзеру
my_call_buf = []
@dp.callback_query_handler(text=['MyButton31'], state="*")
async def MyCallBack31(call, state: FSMContext):
    user_id = update_user[-1]
    user_meets = cur.execute('SELECT id_meets, date FROM Meets WHERE id=' + str(user_id)).fetchall()
    meets_count = len(user_meets)
    dates = []
    id_meets = []
    for i in user_meets:
        dates.append(i[1])
        id_meets.append(i[0])
    f_keyboard = types.InlineKeyboardMarkup(row_width=1)
    my_call_buf.clear()
    for i in dates:
        f_keyboard.add(types.InlineKeyboardButton(text=i, callback_data=i))
        my_call_buf.append(i)
    await bot.send_message(chat_id=call.from_user.id,
                           text='Все записи', parse_mode='MarkDown', reply_markup=f_keyboard)



# Пред этап по обновлению инфы в базе
@dp.callback_query_handler(text=['MyButton21'], state="*")
async def MyCallBack21(call, state: FSMContext):
    user_id = call.from_user.id
    update_keyboard = types.InlineKeyboardMarkup(row_width=1)
    update_keyboard.add(b28,b13,b14,b15,b17,b18,b19,b20,b26,b27,b5,b22)
    await bot.send_message(user_id,
                           f'⬇️Обновление информации в БД:\n1. Отправить текстовое сообщение с информацией, которую нужно добавить в базу\n2. Выбрать ячейку, которую нужно обновить в базе',
                           reply_markup=update_keyboard)


@dp.callback_query_handler(IsAdmin(),
                           text=['MyButton13', 'MyButton14', 'MyButton15', 'MyButton17', 'MyButton18', 'MyButton19',
                                 'MyButton20', 'MyButton28'], state="*")
async def MyCallBackUpdater(call, state: FSMContext):
    user_id = call.from_user.id
    if call.data == 'MyButton13':
        cur.execute('UPDATE Users SET phone=? WHERE id =?', (buf[-1], update_user[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton14':
        cur.execute('UPDATE Users SET real_name=? WHERE id =?', (buf[-1], update_user[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton15':
        cur.execute('UPDATE Users SET date_birth=? WHERE id =?', (buf[-1], update_user[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton17':
        cur.execute('UPDATE Users SET serv_book=? WHERE id =?', (buf[-1], update_user[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton18':
        cur.execute('UPDATE Users SET garante=? WHERE id =?', (buf[-1], update_user[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton19':
        cur.execute('UPDATE Users SET main_recom=? WHERE id =?', (buf[-1], update_user[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton20':
        cur.execute('UPDATE Users SET secret_key=? WHERE id =?', (buf[-1], update_user[-1],)).fetchone()
        bd.commit()
    elif call.data == 'MyButton28':
        cur.execute('UPDATE Users SET id=? WHERE id =?', (buf[-1], update_user[-1],)).fetchone()
        bd.commit()

    check_user = cur.execute('SELECT id, phone, instanse, real_name, date_birth, serv_book, garante, main_recom, secret_key FROM Users WHERE id == ?', (update_user[-1],)).fetchone()
    myansw = (f'*Профиль пациента*\n'
              f'*ID*: {check_user[0]}\n'
              f'*Телефон*: {check_user[1]}\n'
              f'*Статус*: {check_user[2]}\n'
              f'*ФИО*: {check_user[3]}\n'
              f'*День рождения*: {check_user[4]}\n'
              f'*Сервисная книга*:\n{check_user[5]}\n'
              f'*Условия гарантии*:\n{check_user[6]}\n'
              f'*Общие рекомендации*:\n{check_user[7]}\n'
              f'*Ключ подключения*: {check_user[8]}\n'
              )
    update_keyboard = types.InlineKeyboardMarkup(row_width=1)
    update_keyboard.add(b28, b13, b14, b15, b17, b18, b19, b20, b5, b22)
    await bot.send_message(user_id, myansw, parse_mode='MarkDown', reply_markup=update_keyboard)

# Загрузка файлов на сервер
path_to = []
@dp.message_handler(IsAdmin(), text=['обновить'], content_types=types.ContentType.DOCUMENT, state="*")
async def MyCallBackDoc(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not update_user:
        await message.answer(
            'Связь с пациентом не установлена. Просьба найти пациента в базе и повторить загрузку ')
    else:
        path_to_download = Path().joinpath(str(update_user[-1]))
        path_to_download.mkdir(parents=True, exist_ok=True)
        path_to_download = path_to_download.joinpath(message.document.file_name)
        await message.document.download(destination=path_to_download)
        down_keyboard = types.InlineKeyboardMarkup(row_width=1)
        down_keyboard.add(b51, b52)
        await bot.send_message(user_id,
                               f'Документ загружен в каталог юзера {update_user[-1]}. Укажите тип загруженного документа',
                               parse_mode='MarkDown', reply_markup=down_keyboard)
        path_to.clear()
        path_to.append(str(path_to_download))

@dp.message_handler(IsAdmin(), text=['бд'], content_types=types.ContentType.DOCUMENT, state="*")
async def MyCallBacktest(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    path_to_download = Path().joinpath('all_clients')
    path_to_download.mkdir(parents=True, exist_ok=True)
    path_to_download = path_to_download.joinpath(message.document.file_name)
    await message.document.download(destination=path_to_download)
    df = pd.read_excel(path_to_download, sheet_name='Пациент')
    dfz = pd.read_excel(path_to_download, sheet_name='Записи')
    phone_number = str(df.loc[0,"Инфо"])
    full_name = str(df.loc[1, "Инфо"])
    date_birt = df.loc[2, "Инфо"]
    date_birth = f'{date_birt.day}.{date_birt.month}.{date_birt.year}'
    serv_book= str(df.loc[3, "Инфо"])
    garentee = str(df.loc[4, "Инфо"])
    recommend = str(df.loc[5, "Инфо"])
    my_key = str(df.loc[6, "Инфо"])

    check_user = cur.execute('SELECT real_name FROM Users WHERE phone =?', (phone_number[-10:],)).fetchone()
    if check_user is not None:
        check_step = cur.execute('SELECT id FROM Users WHERE phone =?', (phone_number[-10:],)).fetchone()
        cur.execute('DELETE FROM Users WHERE phone = ?', (phone_number[-10:],))
        cur.execute('DELETE FROM Meets WHERE id= ?', (check_step[0],))
        cur.execute('INSERT INTO Users(id, phone, instanse, real_name, date_birth, serv_book, garante, main_recom, secret_key) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (check_step[0], phone_number[-10:], 'friend', full_name, date_birth, serv_book, garentee, recommend, my_key,))
        bd.commit()
        await bot.send_message(user_id,
                               f'Пациент {full_name} с телефоном {phone_number} уже был в базе на момент загрузки. Все предыдущие записи удалены. Загружена актуальная информация')

    if check_user is  None:
        await bot.send_message(user_id, f'Номер телефона в базе не найден. Пользователь {full_name} с телефоном {phone_number} занесён в базу как новый пациент')
        cur.execute('INSERT INTO Users(id, phone, instanse, real_name, date_birth, serv_book, garante, main_recom, secret_key) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (phone_number[-10:], phone_number[-10:], 'friend', full_name, date_birth, serv_book, garentee, recommend, my_key,))
        bd.commit()
    check_user = cur.execute('SELECT id, phone, instanse, real_name, date_birth, serv_book, garante, main_recom, secret_key FROM Users WHERE phone =?', (phone_number[-10:],)).fetchone()
    myansw = (f'*Профиль пациента*\n'
                  f'*ID*: {check_user[0]}\n'
                  f'*Телефон*: {check_user[1]}\n'
                  f'*Статус*: {check_user[2]}\n'
                  f'*ФИО*: {check_user[3]}\n'
                  f'*День рождения*: {check_user[4]}\n'
                  f'*Сервисная книга*:\n{check_user[5]}\n'
                  f'*Условия гарантии*:\n{check_user[6]}\n'
                  f'*Общие рекомендации*:\n{check_user[7]}\n'
                  f'*Ключ подключения*: {check_user[8]}\n'
                  )
    await message.answer(myansw,
                             parse_mode='MarkDown')

    for i in range(len(dfz)):
            last_ids = cur.execute("SELECT id_meets FROM Meets ORDER BY id_meets DESC LIMIT 1").fetchone()
            date = f'{dfz.loc[i, "Дата"].day}.{dfz.loc[i, "Дата"].month}.{dfz.loc[i, "Дата"].year}'

            finish_date = dfz.loc[i, "Дата"].strftime("%Y-%m-%d")
            cur.execute('INSERT INTO Meets(id_meets, id, date, time, price, price_state, plan, recomend, real_name, approve, real_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (str(last_ids[0]+1), check_user[0], date, str(dfz.loc[i, "Время"]),
                         str(dfz.loc[i, "Цена"]), str(dfz.loc[i, "Статус оплаты"]),
                         str(dfz.loc[i, "План лечения"]), str(dfz.loc[i, "Рекомендации"]), full_name, 'не запрошено', finish_date))
            bd.commit()
    my_meets = cur.execute(
            'SELECT date, time, price, price_state, plan, approve FROM Meets WHERE id=? ORDER BY real_date DESC',
            (check_user[0],)).fetchall()
    meets_count = len(my_meets)
    aps = f'Всего записей на приём: {meets_count}\n'
    if meets_count > 0:
            dates = []
            time = []
            plan = []
            price = []
            price_state = []
            approves = []
            aps = f'*Все записи*:\n'
            for i in my_meets:
                dates.append(i[0])
                time.append(i[1])
                plan.append(i[4])
                price.append(i[2])
                price_state.append(i[3])
                approves.append([i[5]])
            for i in range(len(dates)):
                mes = f'*Дата* {dates[i]} *Время* {time[i]} *{price_state[i]}* {price[i]} руб. *Подтверждение* {approves[i]}\n*План лечения* {plan[i]}'
                aps = aps + mes + '\n'
            f_keyboard = types.InlineKeyboardMarkup(row_width=1)
            f_keyboard.add(b5)
            await bot.send_message(chat_id=user_id,
                                   text=aps, parse_mode='MarkDown', reply_markup=f_keyboard)
            update_user.clear()
            update_user.append(check_user[0])
    os.remove(path_to_download)

# Обратная связь (клиент => клиника)
@dp.callback_query_handler(text=['MyButton3'], state="*")
async def MyCallBack3(call, state: FSMContext):
    user_id = call.from_user.id
    await bot.send_message(user_id, 'Отправьте сообщение с вашим запросом/пожеланиями по записи. Не забудьте указать контактные данные, чтобы мы могли связаться с вами.')
    await Change.ChangeMeet.set()

# Второй этап по обратной связь (клиент => клиника)
zapros = []
@dp.message_handler(state=Change.ChangeMeet)
async def MyCallBack17(message: types.Message, state: FSMContext):
    mes = message.text
    user_id = message.from_user.id
    zapros.append(message.from_user.first_name)
    zapros.append(mes)
    ad_keyboard = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text="Отправить📩", callback_data="MyButton99")
    b2 = types.InlineKeyboardButton(text="Изменить🔧", callback_data="MyButton3")
    ad_keyboard.add(b1, b2)
    await bot.send_message(user_id, f'Направить администратору текст запроса?\nТекст запроса:\n{mes}',
                           reply_markup=ad_keyboard)
    await state.reset_state()

# Финал по обратной связь (клиент => клиника) запрос отправляется админам
@dp.callback_query_handler(text=['MyButton99'], state="*")
async def MyCallBack3(call, state: FSMContext):
    user_id = call.from_user.id
    check_user = cur.execute('SELECT real_name, phone FROM Users WHERE id =?', (user_id,)).fetchone()
    admins = cur.execute('SELECT id FROM Users WHERE instanse == "admin"').fetchall()
    admin_list = [x[0] for x in admins]
    if check_user is not None:
        fin_zap = (f'Поступил запрос\n'
                   f'Отправитель {check_user[0]}\n'
                   f'Номер телефона {check_user[1]}\n'
                   f'Запрос: {zapros[-1]}')
        for i in admin_list:
            await bot.send_message(i, fin_zap)
    elif check_user is None:
        fin_zap = (f'Поступил запрос от юзера {zapros[0]} не из базы\n'
                   f'Запрос: {zapros[1]}')
        for i in admin_list:
            await bot.send_message(i, fin_zap)
    zapros.clear()
    await bot.send_message(user_id,
                           f'Ваш запрос был направлен администратору. Он уточнит данные и свяжется с вами в ближайшее время')

# поиск клиента в базе с помощью контакта
new_client = []
@dp.message_handler(IsAdmin(), content_types=types.ContentType.CONTACT, state="*")
async def get_contact(message: types.Message):
    contact = message.contact
    user_id = message.from_user.id
    phone = contact.phone_number[-10:]
    await message.answer(
        f'*Поиск контакта в базе*\n'
        f'*Имя* {contact.full_name}\n'
        f'*Телефон* {phone}',
        reply_markup=types.ReplyKeyboardRemove(), parse_mode='MarkDown'
    )
    new_client.clear()
    find_id = message.contact.user_id
    check_user = cur.execute('SELECT id, phone, instanse, real_name, date_birth, serv_book, garante, main_recom, secret_key FROM Users WHERE id == ?', (find_id,)).fetchone()

    if user_id in [1757558411, 29720838] and check_user is None:
        add_keyboard = types.InlineKeyboardMarkup(row_width=1)
        add_keyboard.add(b89,b95)
        if message.contact.user_id is None:
            message_info = 'Данного юзера нет в базе. Добавить?'
            await message.answer(
            message_info,
            reply_markup=add_keyboard)
            new_client.append(phone)
        elif message.contact.user_id is not None:
            message_info = 'Данного юзера нет в базе. Добавить?'
            await message.answer(
                message_info,
                reply_markup=add_keyboard)
            new_client.append(message.contact.user_id)
            new_client.append(phone)

    elif check_user is None:
        add_keyboard = types.InlineKeyboardMarkup(row_width=1)
        add_keyboard.add(b89)

        if message.contact.user_id is None:
            message_info = (f'Не могу получить ID юзера, так как у него установлены настройки приватности.\n'
                           f'ID можно добавить вручную, либо настроить подключение через секрытный код.\n' 
                           f'После этого у пациента откроется доступ к личному кабинету. Добавить юзера в базу?')

            await message.answer(
                message_info,
                reply_markup=add_keyboard)
            new_client.append(phone)
        else:
            new_client.clear()
            await message.answer(
                'В базе отсутствует пользователь с данным номером телефона. Внести пользователя как нового пациента?')
            new_client.append(message.contact.user_id)
            new_client.append(phone)

            await message.answer(
                f'ID: {message.contact.user_id} Телефон: {phone}', reply_markup=add_keyboard)
    else:
        myansw = (f'*Профиль Пациента*\n'
                  f'*ID*: {check_user[0]}\n'
                  f'*Телефон*: {check_user[1]}\n'
                  f'*Статус*: {check_user[2]}\n'
                  f'*ФИО*: {check_user[3]}\n'
                  f'*День рождения*: {check_user[4]}\n'
                  f'*Сервисная книга*:\n{check_user[5]}\n'
                  f'*Условия гарантии*:\n{check_user[6]}\n'
                  f'*Общие рекомендации*:\n{check_user[7]}\n'
                  f'*Ключ подключения*: {check_user[8]}\n'
                  )
        await message.answer(myansw,
                              parse_mode='MarkDown')

# Добавление юзера как клиента
@dp.callback_query_handler(text=['MyButton89', 'MyButton98', 'MyButton95'], state="*")
async def MyCallBack89(call, state: FSMContext):
    user_id = call.from_user.id
    admins_k = types.InlineKeyboardMarkup(row_width=1)
    admins_k.add(b5)
    if call.data in ['MyButton89', 'MyButton98'] and len(new_client)==2:
        cur.execute('INSERT INTO Users(id, phone, instanse, real_name) VALUES(?, ?, ?, ?)',
                    (new_client[0], new_client[1], 'friend', new_client[1],))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text='Пользователь внесён в базу', parse_mode='MarkDown', reply_markup=admins_k)
    elif call.data in ['MyButton89', 'MyButton98'] and len(new_client)==1:
        cur.execute('INSERT INTO Users(id, phone, instanse, real_name) VALUES(?, ?, ?, ?)',
                    (new_client[0], new_client[0], 'friend', new_client[0],))
        bd.commit()

        await bot.send_message(chat_id=user_id,
                               text='Пользователь внесён в базу. Для доступа к админке понадобится секретный ключ', parse_mode='MarkDown', reply_markup=admins_k)

    elif call.data == 'MyButton95' and len(new_client)==1:
        cur.execute('INSERT INTO Users(id, phone, instanse, real_name) VALUES(?, ?, ?, ?)',
                    (new_client[0], new_client[0], 'admin', 'Администратор',))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text='Администратор внесён в базу. Для доступа к админке понадобится секретный ключ', parse_mode='MarkDown', reply_markup=admins_k)
    elif call.data == 'MyButton95' and len(new_client)==2:
        cur.execute('INSERT INTO Users(id, phone, instanse, real_name) VALUES(?, ?, ?, ?)',
                    (new_client[0], new_client[1], 'admin', 'Администратор',))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text='Администратор внесён в базу.', parse_mode='MarkDown', reply_markup=admins_k)


@dp.callback_query_handler(text=['MyButton1'], state="*")
async def MyCallBack1(call, state: FSMContext):
    user_id = call.from_user.id
    mypvic = cur.execute('SELECT real_name, serv_book, garante, main_recom FROM Users WHERE id=?', (user_id,)).fetchone()
    myansw = (f'*Моё лечение*\n'
              f'*ФИО* {mypvic[0]}\n'
              f'*Доктор*: Айболитов \n'
              f'*Сервисная книга*:\n{mypvic[1]}\n'
              f'*Условия гарантии*:\n{mypvic[2]}\n'
              f'*Рекомендации*:\n{mypvic[3]}\n'
              )
    my_meets = cur.execute('SELECT date, time, plan, price, price_state FROM Meets WHERE id=' + str(user_id)).fetchall()
    meets_count = len(my_meets)
    dates = []
    time = []
    plan = []
    price = []
    price_state = []
    for i in my_meets:
        dates.append(i[0])
        time.append(i[1])
        plan.append(i[2])
        price.append(i[3])
        price_state.append(i[4])
    aps = f'*Мои записи*: {meets_count}\n'
    for i in range(len(dates)):
        mes = f'*Дата* {dates[i]} *Время* {time[i]} *{price_state[i]}* {price[i]}\n*План лечения* {plan[i]}'
        aps = aps + mes + '\n'

    kab_keyboard = types.InlineKeyboardMarkup(row_width=1)
    kab_keyboard.add(b2, b10, b11, b24)
    await bot.send_message(chat_id=user_id,
                           text=myansw, reply_markup=kab_keyboard, parse_mode='MarkDown')


    await bot.send_message(chat_id=user_id,
                           text=aps, parse_mode='MarkDown')

# БЛОК С ОБЩЕЙ ИНФОЙ
@dp.callback_query_handler(text=['MyButton4'], state="*")
async def MyCallBack2(call, state: FSMContext):
    user_id = call.from_user.id
    about_keyboard = types.InlineKeyboardMarkup(row_width=1)
    about_keyboard.add(b7, b8, b9, b16)
    await bot.send_message(user_id,
                           f"Стоматология, которую вы заслужили.\nТелефон: +7 (495) 123 45 55\nПочта info@dr.ru",
                           reply_markup=about_keyboard, parse_mode="MarkDown")

@dp.callback_query_handler(text=['MyButton8'], state="*")
async def MyCallBack8(call, state: FSMContext):
    user_id = call.from_user.id
    mess = '<a href="https://t.me/">Айболитов - эстетическая стоматология</a>'
    await bot.send_message(user_id,
                           text=mess, parse_mode="HTML")

@dp.callback_query_handler(text=['MyButton16'], state="*")
async def MyCallBack16(call, state: FSMContext):
    user_id = call.from_user.id
    site_link = '<a href="https://dr.ru">Официальный сайт</a>'
    await bot.send_message(user_id,
                           text=site_link, parse_mode="HTML")

@dp.callback_query_handler(text=['MyButton9'], state="*")
async def MyCallBack8(call, state: FSMContext):
    user_id = call.from_user.id
    discount_mes = (
        f'*Скидка 5%* предоставляется при согласовании плана лечения и *внесении предоплаты* в течение 24ч. после консультации.\n'
        f'*Скидка 10%* предоставляется при расчете наличными денежными средствами или онлайн переводом.')
    await bot.send_message(user_id,
                           text=discount_mes, parse_mode="MarkDown")

@dp.callback_query_handler(text=['MyButton7'], state="*")
async def MyCallBack7(call, state: FSMContext):
    user_id = call.from_user.id

    adress = (f'*Клиника "Дент"*\n'
              f' \n'
              f'ул. Лесная, д.35\n'
              f' \n'
  )

    await bot.send_message(user_id,
                           text=adress, parse_mode="MarkDown")


# Регистрация через секретный код
secret_client_id = []
@dp.message_handler(text=['Я пациент', 'я пациент', 'япациент', 'Япациент'], state="*")
async def i_am_client_func(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    secret_client_id.clear()
    secret_client_id.append(user_id)
    await message.answer(
        f'Если вы являетесь пациентом клиники и хотите подключиться к своей кабинету пришлите код доступа следующим сообщением.')
    await Client.ClientUp.set()


client_key = []
@dp.message_handler(state=Client.ClientUp)
async def i_am_client_func_f(message: types.Message, state: FSMContext):
    mes = message.text

    mypvic = cur.execute('SELECT secret_key, phone FROM Users WHERE secret_key > 0').fetchall()
    mypvic_list = [x[0] for x in  mypvic]
    if int(mes) in mypvic_list:
        await message.answer(
            f'Соединение установлено. Профиль подгружается. Для завершения загрузки укажите 5 последних цифры номера своего телефона')
        await Client.ClientUpp.set()
        client_key.append(str(mes))

    else:
        await message.answer(
            f'Подключение не удалось, обратитесь к администратору')
        await state.reset_state()


@dp.message_handler(state=Client.ClientUpp)
async def i_am_client_func_f(message: types.Message, state: FSMContext):
    mes = message.text
    user_id = secret_client_id[-1]
    check_user = cur.execute('SELECT phone, real_name FROM Users WHERE secret_key = ?', (client_key[-1],)).fetchone()
    phone_secr = str(check_user[0])
    if mes == phone_secr[-5:]:
        first_client_keyboard = types.InlineKeyboardMarkup(row_width=1)
        first_client_keyboard.add(b1)
        await message.answer(
            f'Добро пожаловать, {check_user[1]}. Доступ к личному кабинету открыт', reply_markup=first_client_keyboard)
        cur.execute('UPDATE Users SET id=? WHERE secret_key =?', (user_id, client_key[-1],))
        cur.execute('UPDATE Users SET secret_key = ? WHERE id =?', (0, user_id,))
        bd.commit()
    elif mes != phone_secr[-5:]:
        await message.answer(
            f'Введены неправильные данные. Авторизация отменена')
    await state.reset_state()


# Хендлер, которые ловит все остальные коллбеки
check_date = []
@dp.callback_query_handler(state="*")
async def MyCallBack33(call, state: FSMContext):
    if call.data in my_call_buf:
        check_date.clear()
        check_date.append(call.data)

        cor_keyboard = types.InlineKeyboardMarkup(row_width=1)
        cor_keyboard.add(b32, b34)
        await bot.send_message(chat_id=call.from_user.id,
                               text=f'Вы выбрали запись на {call.data}', reply_markup=cor_keyboard)
    elif call.data in my_call_clients:
        check_user = cur.execute('SELECT id, phone, instanse, real_name, date_birth, serv_book, garante, main_recom, secret_key FROM Users WHERE real_name == ?', (call.data,)).fetchone()
        myansw = (f'*Профиль пациента*\n'
                  f'*ID*: {check_user[0]}\n'
                  f'*Телефон*: {check_user[1]}\n'
                  f'*Статус*: {check_user[2]}\n'
                  f'*ФИО*: {check_user[3]}\n'
                  f'*День рождения*: {check_user[4]}\n'
                  f'*Сервисная книга*:\n{check_user[5]}\n'
                  f'*Условия гарантии*:\n{check_user[6]}\n'
                  f'*Общие рекомендации*:\n{check_user[7]}\n'
                  f'*Ключ подключения*: {check_user[8]}\n'
                  )
        cor_keyb = types.InlineKeyboardMarkup(row_width=1)
        cor_keyb.add(b21, b22)
        update_user.clear()
        await bot.send_message(chat_id=call.from_user.id, text=myansw, parse_mode='MarkDown', reply_markup=cor_keyb)
        update_user.append(check_user[0])
        if str(check_user[0]) == str(check_user[1]):
            await bot.send_message(chat_id=call.from_user.id, text=f'У пользователя указан некорректный ID. Для доступа к личному кабинету необходим указать корректный ID, либо использовать ключ')

    elif call.data == 'MyButton32':
        meets_id = cur.execute('SELECT id_meets FROM Meets WHERE date = ? AND id = ?',
                               (check_date[0], update_user[-1],)).fetchone()
        cur.execute('DELETE FROM Meets WHERE id_meets = ?', (meets_id[0],))
        one_keyb = types.InlineKeyboardMarkup(row_width=1)
        one_keyb.add(b22, b5)
        await bot.send_message(chat_id=call.from_user.id,
                               text=f'Запись № {meets_id[0]} удалена из базы', reply_markup=one_keyb)
    elif call.data == 'MyButton34':
        meets_id = cur.execute('SELECT id_meets FROM Meets WHERE date = ? AND id = ?',
                                (check_date[0], update_user[-1],)).fetchone()

        create_add = cur.execute("SELECT * FROM Meets WHERE id_meets=?", (meets_id[0],)).fetchone()
        new_add = (f'Номер записи *{create_add[0]}*\n'
                   f'Дата *{create_add[2]}*\n'
                   f'Время *{create_add[3]}*\n'
                   f'Цена *{create_add[4]}*\n'
                   f'Статус оплаты *{create_add[5]}*\n'
                   f'План лечения *{create_add[6]}*\n'
                   f'Рекомендации *{create_add[7]}*\n')
        time_keyboard = types.InlineKeyboardMarkup(row_width=1)
        time_keyboard.add(b40, b41, b42, b43, b44, b45, b22, b5)
        await bot.send_message(chat_id=call.from_user.id,
                               text=new_add, parse_mode='MarkDown', reply_markup=time_keyboard)
        last_id.clear()
        last_id.append(meets_id[0])

    elif call.data == 'MyButton51':
        cur.execute('UPDATE Users SET plan == ? WHERE id == ?', (path_to[0], update_user[0]))
        bd.commit()
        await bot.send_message(chat_id=call.from_user.id,
                               text=f'План лечения обновлен для юзера {update_user[0]}', parse_mode='MarkDown')
    elif call.data == 'MyButton52':
        cur.execute('UPDATE Users SET photoproc == ? WHERE id == ?', (path_to[0], update_user[0]))
        bd.commit()
        await bot.send_message(chat_id=call.from_user.id,
                               text=f'Фотопротокол обновлен для юзера {update_user[0]}', parse_mode='MarkDown')
    elif call.data == 'MyButton61':

        cur.execute('UPDATE Meets SET approve == ? WHERE id == ? AND approve == ?', ('подтверждено', call.from_user.id, 'запрошено'))
        bd.commit()
        await bot.send_message(chat_id=call.from_user.id,
                               text=f'Спасибо, ваше подтверждение отправлено в клинику')

    elif call.data == 'MyButton62':
        cur.execute('UPDATE Meets SET approve == ? WHERE id_meets == ? AND approve == ?', ('не подтверждено', call.from_user.id, 'запрошено'))
        bd.commit()
        await bot.send_message(chat_id=call.from_user.id,
                               text=f'Спасибо, мы свяжемся с вами для уточнения информации')


# кладём в буфер каждое свежее сообщение от админа
@dp.message_handler(IsAdmin(), state="*")
async def my_update_buf(message: types.Message):
    to_buf = message.text
    buf.clear()
    buf.append(to_buf)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
