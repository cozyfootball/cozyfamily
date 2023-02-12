from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from time import sleep
from aiogram.dispatcher.filters import CommandStart
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import BoundFilter
import random
import sqlite3
from aiogram.utils.markdown import hlink

# Базовые настройки
API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp  = Dispatcher(bot)

button1 = InlineKeyboardButton(text='Проверка🧐', callback_data='check')
button2 = InlineKeyboardButton(text='Заявление🧾', callback_data='blanc')
button3 = InlineKeyboardButton(text='Обратная связь💌', callback_data='feedback')
button4 = InlineKeyboardButton(text='Сказать спасибо✅', callback_data='thx')
button5 = InlineKeyboardButton(text='14 дней', callback_data='14day')
button6 = InlineKeyboardButton(text='💰Погашение кредита', callback_data='credit')

import sqlite3

bd = sqlite3.connect('insure.db')

cur = bd.cursor()

bd.execute('CREATE TABLE IF NOT EXISTS Users (id int NOT NULL, user_state NULL, PRIMARY KEY(id))')
bd.commit()

@dp.message_handler(text='/start')
async def first_step(message: types.Message):
    user_id = message.from_user.id
    fellows = cur.execute('SELECT * FROM Users').fetchall()
    fellows_cler = [x[0] for x in fellows]
    thx_num_all = cur.execute('SELECT COUNT(*) FROM Users').fetchone()
    thx_num = cur.execute('SELECT COUNT(*) FROM Users WHERE user_state = "yes"').fetchone()
    if user_id in fellows_cler:
        await bot.send_sticker(user_id, "CAACAgIAAxkBAAEGBYhjQKkOQNkKFbMxDsbH7DgYZFWP8wAC6wIAAqKK8Qf-zEMKYImuxCoE")
    elif user_id not in fellows_cler:
        await bot.send_sticker(user_id, "CAACAgIAAxkBAAEGBc9jQSaelW2iz2l9pZ78TV00RZxLbgAChgMAAqKK8Qcb7qV0cofXqyoE")
        cur.execute('INSERT INTO Users VALUES(?, ?)', (user_id, ''))
    bd.commit()
    hello_user = (f'Привет, я *Вадимка*🦚.\n' 
    f'Я помогаю *расторгать страховые полисы и возвращать стоимость страховки*(страховая премия💰) в тех случаях, когда это предусмотрено законом.\n'
    f'*Страхователи - физические лица* могут вернуть  страховую премию *в течение 14 дней с момента покупки страхового полиса*, такой возврат называется *\"периодом охлаждения\"*🥶.\n '
    f'В данном случае Страховщик *обязан вернуть страховую премию* 💰 по договору добровольного страхования автомобилей, жизни, имущества, ответственности, финансовых рисков.\n'
    f'Возврат части премии возможен *при полном досрочном погашении задолженности* перед банком🏦, если в рамках выдачи кредита был приобретен страховой полис обеспечивающий обязательства заемщика перед банком. В данном случае Страховщик обязан вернуть страховую премию за период от даты досрочного погашения кредита до даты окончания действия страхового полиса.\n'
    f'Страховщики зачастую не любят🙅🏻‍♂️ возвращать страховые премии клиентам, поэтому *пытаются усложнить процедуру* возврата премии.\n' 
    f'*Я 🦚 помогу* определить возможность возврата денег и *поделюсь формой заявления* на возврат.')
    await message.answer(text=hello_user, parse_mode="MarkDown")
    sleep(3)
    my_youtube = hlink('Видеоинструкция', 'https://www.youtube.com/shorts/rWiGt8wD5wg')
    await message.answer(text=my_youtube, parse_mode="HTML")

    if user_id == 29720838:
        await message.answer(text=f'Количество обратившихся: *{thx_num_all[0]}*\n'
                                    f'Количество благодарностей: *{thx_num[0]}*', parse_mode="MarkDown")
    sleep(4)
    MainMenu = InlineKeyboardMarkup(row_width=2)
    MainMenu.add(button1, button2, button3, button4)
    hello_user2 = (f'1️⃣ Жми *"Проверка"*🧐 - чтобы проверить свой полис на возможность возврата страховой премии.\n'
                   f'2️⃣ Жми *"Заявление"*🧾 - чтобы получить образец заявления и направить пакет документов Страховщику для возврата премии.\n'
                   f'3️⃣ Жми *"Обратная связь"*💌 - чтобы направить комплект своих документов на индивидуальную экспертизу на возможность возврата страховой премии по договору. Или просто связаться с нами.\n'
                   f'3️⃣ Жми *"Сказать спасибо"*✅ - если я тебе помог и ты хочешь сказать спасибо моим создателям')
    await message.answer(text=hello_user2, reply_markup=MainMenu, parse_mode="MarkDown")

@dp.callback_query_handler(text='blanc')
async def blanc_call(call):
    blancmes1 = (f'Чтобы получить форму📄 заявления в Word выбери *тип* заявления:\n'
                 f'14 *дней* - форма для возврата страховой премии в первые 14 дней с момента покупки полиса.\n*Срок возврата*: от 7 до 10 рабочих дней с момента получения заявления.\n'
                 f'💰*Погашение кредита* - форма для  для возврата части премии при досрочном погашении кредита.\n*Возврат*: 7 раб. дней.\n')
    await bot.send_message(chat_id=call.from_user.id, text=blancmes1, parse_mode="MarkDown")
    sleep(4)

    blancmes2 = (f'Для возврата страховой премии Страховщику(или третьему лицу действующему в интересах Страховщика, например, банк🏦) необходимо направить следующий пакет документов:\n'
                 f'✅ Заполненное заявление c реквизитами счета на который необходимо произвести возврат\n'
                 f'✅ Скан/Фото Паспорта Страхователя\n'
                 f'✅ Оригинал/Копию страхового полиса\n'
                 f'☑ Документ подтверждающий закрытие кредита (только для типа 💰"Погашение кредита")')
    Blanc_choise = InlineKeyboardMarkup(row_width=2)
    Blanc_choise.add(button5, button6)
    await bot.send_message(chat_id=call.from_user.id, text=blancmes2, reply_markup=Blanc_choise, parse_mode="MarkDown")

@dp.callback_query_handler(text='14day')
async def blanc_14d(call):
    file1 = open('blanc1.docx', 'rb')
    await bot.send_document(call.from_user.id, file1)

@dp.callback_query_handler(text='credit')
async def blanc_cred(call):
    file2 = open('blanc2.docx', 'rb')
    await bot.send_document(call.from_user.id, file2)

@dp.callback_query_handler(text='feedback')
async def feedback(call):
    feedbmes1 = (f'*Вадимка 🦚 это бот - страховой помощник*. Его главная задача - *помочь клиентам* страховых компаний не быть обманутыми страховыми компаниями.  За последние несколько лет был принят ряд законов защищающих права клиентов страховых компаний.\n'
                f'Несмотря на это, *многие страховые компании продолжают попытки обмана клиентов*, не возвращая им деньги, положенные по закону.  Некоторые страховые создают максимально сложную процедуру для получения заявления на возврат стоимости страховки.\n'
                f' *Вадимка*🦚:\n'
                f' ✅ поможет *определить возможность возврата денег* оплаченных за страхование\n'
                f' ✅ *предоставит форму заявления* на возврат страховой премии.\n'
                f' ✅ *подскажет как обратиться к нашим экспертам* для экспертизы сложных случаев.')
    await bot.send_message(chat_id=call.from_user.id, text=feedbmes1, parse_mode="MarkDown")
    sleep(4)
    feedbmes2 = (f'*Вадимка 🦚 напоминает*:\n'
                 f'⚠️ При покупки страхового полиса в банке(автосалоне), *фактическая стоимость страхования составляет не более 10-15%* от стоимости озвученной банком. Всё остальное *это комиссия банка* за оформление полиса🙄.  Готовы ли вы платить десятки тысяч рублей за *посредничество в оформлении* полиса?\n'
                 f' Помните, даже если вы *уже оплатили* страховку, вы *можете отказаться* от неё в течение 14 дней с момента оформления и получить возврат стоимости. Банки будут вас пугать изменением процентной ставки, НО если вы оформите страховой полис по покрытию обеспечивающему кредит (риски указаны в индивидуальных условиях), то вы сможете сэкономить до 90% от стоимости страховки озвученной банком.\n'
                 f' ⚠️ Если вы считаете, что страховая компания нарушает требования законодательства по возврату, то вы можете обратиться к *финансовому уполномоченному*:\n'
                 f'https://finombudsman.ru/\n'
                 f'*Финансовый уполномоченный помогает решать споры со страховщиком в досудебном порядке.*\n')
    await bot.send_message(chat_id=call.from_user.id, text=feedbmes2, parse_mode="MarkDown")
    sleep(4)
    feedbmes3 = (f'*Электронная почта для связи с авторами проекта *- strahh.bot@gmail.com\n'
                 f'*Напишите нам*, если:\n'
                 f'✅ У вас возникли вопросы или предложения по работе Вадимка🦚.\n'
                 f'✅ Вы хотите получить заключение по возможности возврата от наших экспертов.\n'
                 f'☑️ В других случаях...')
    await bot.send_message(chat_id=call.from_user.id, text=feedbmes3, parse_mode="MarkDown")


@dp.callback_query_handler(text='thx')
async def feedback(call):

    thx_num = cur.execute('SELECT COUNT(*) FROM Users WHERE user_state = "yes"').fetchone()
    thx_id = cur.execute('SELECT * FROM Users WHERE user_state = "yes"').fetchall()
    fellows_cler = [x[0] for x in thx_id]


    await bot.send_message(chat_id=call.from_user.id, text=f'Количество благодарностей: *{thx_num[0]}*\n'
                                                           f'Если я был тебе полезен, то не стесняйся, жми кнопку. Это придаст заряда моей 🔋', parse_mode="MarkDown")
    sleep(1)
    if call.from_user.id not in fellows_cler:
        await bot.send_message(chat_id=call.from_user.id, text=f'Теперь мне так радостно🤟🏻')
        user_id = call.from_user.id
        cur.execute('UPDATE Users SET user_state == ? WHERE id == ?', ('yes', user_id))
        bd.commit()
    elif call.from_user.id in fellows_cler:
        await bot.send_message(chat_id=call.from_user.id, text=f'Спасибо, я помню, что я смог тебе помочь')
        bd.commit()
    else:
        await bot.send_message(chat_id=call.from_user.id, text=f'Неизвестная ошипка')

@dp.callback_query_handler(text='check')
async def check_1(call):
    check_mes1 = (f'Для *определения возможности возврата* стоимости страховки💰 вам необходимо ответить на несколько вопросов.\n'
                 f'Используйте *кнопки*🖲 под сообщениям для ответа на вопросы.\n'
                 f'В случае возникновения вопросов рекомендуем воспользоваться разделом *"Обратная связь"* 💌.')
    await bot.send_message(chat_id=call.from_user.id, text=check_mes1, parse_mode="MarkDown")
    sleep(2)
    q1 = f'Вы обращались в страховую компанию по поводу страхового случая/для получения страховой выплаты по данной страховке?'
    button8 = InlineKeyboardButton(text='Да✅', callback_data='yes1')
    button9 = InlineKeyboardButton(text='Нет🚫', callback_data='no1')
    q1_choise = InlineKeyboardMarkup(row_width=2)
    q1_choise.add(button8, button9)
    await bot.send_message(chat_id=call.from_user.id, text=q1, reply_markup=q1_choise, parse_mode="MarkDown")
@dp.callback_query_handler(text='yes1')
async def check_yes1(call):
    no1 = f'В случае если по страховке был *урегулирован убыток💸*(произведена страховая выплата), либо *заявлен убыток*🧾 (вы обратились к страховщику за выплатой, но еще не получили выплату или отказ в выплате) страховщик *имеет право не возвращать*❌ стоимость страховки (согласно действующему законодательству).'
    await bot.send_message(chat_id=call.from_user.id, text=no1, parse_mode="MarkDown")
@dp.callback_query_handler(text='no1')
async def check_no1(call):
    q2 = f'Данная страховка была приобретена в банке/автосалоне *при получении/выдаче* потребительского💸 или авто🛻 кредита?'
    button8 = InlineKeyboardButton(text='Да✅', callback_data='yes2')
    button9 = InlineKeyboardButton(text='Нет🚫', callback_data='no2')
    q2_choise = InlineKeyboardMarkup(row_width=2)
    q2_choise.add(button8, button9)
    await bot.send_message(chat_id=call.from_user.id, text=q2, reply_markup=q2_choise, parse_mode="MarkDown")
@dp.callback_query_handler(text='no2')
async def check_no2(call):
    q3 = (f'С даты приобретения страховки прошло менее 14 дней?\n'
         f'⚠*Отсчёт 14 дней* осуществляется с даты следующей за датой приобретения страховки.\n'
         f'*Пример*: дата покупки: 01.09.2022, возврат стоимости возможен до 15.09.2022 (включительно).')
    q3_choise = InlineKeyboardMarkup(row_width=2)
    button8 = InlineKeyboardButton(text='Да✅', callback_data='yes3')
    button9 = InlineKeyboardButton(text='Нет🚫', callback_data='no3')
    q3_choise.add(button8, button9)
    await bot.send_message(chat_id=call.from_user.id, text=q3, reply_markup=q3_choise, parse_mode="MarkDown")

@dp.callback_query_handler(text='yes3')
async def check_yes3(call):
    yes3mes = (f' *Законодательством предусмотрен возврат страховой премии в течение 14 дней с момента оформления полиса.* Данный период называется *\"периодом охлаждения\"*🥶. Подразумевается, что у клиента страховой компании *есть 14 дней на то, чтобы передумать* страховаться. Если клиент передумал, то он может обратиться к страховщику с заявлением о возврате. Большинство страховых компании в данном случае возвращают *полностью стоимость* страховки.\n'
              f'⚠️Но есть страховые компании, которые возвращают только 90-95% от стоимости страховки, в случае *если на момент обращения страховка вступила в силу*.\n'
              f'*Пример*: страховой полис оформлен *01.05.2022*, начало срока страхования - *05.05.2022*, клиент обратился за возвратом *09.05.2022*. В данном случае страховая компания имеет право оставить себе стоимость страхования за срок *от 05.05.2022 до 09.05.2022*.\n'
              f'⚠️ Возврат стоимости страховки в *период охлаждения*🥶 возможен только при условии *отсутствия заявленных и урегулированных убытков* по данной страховке.')
    blanc = InlineKeyboardMarkup()
    blanc.insert(button5)
    await bot.send_message(chat_id=call.from_user.id, text=yes3mes, reply_markup=blanc, parse_mode="MarkDown")
@dp.callback_query_handler(text='no3')
async def check_no3(call):
    no3 = f'📛 В случае если с даты приобретения страховки прошло более 14 дней и страховой полис оформлен не для обеспечения кредита, *страховщик имеет право отказать* в возврате денег за страховку.'
    dfind = InlineKeyboardMarkup()
    button10 = InlineKeyboardButton(text='🔬Другие причины возврата', callback_data='noev')
    dfind.insert(button10)
    await bot.send_message(chat_id=call.from_user.id, text=no3, parse_mode="MarkDown", reply_markup=dfind)
@dp.callback_query_handler(text='yes2')
async def check_yes2(call):
    q4 = f'Дата выдачи кредита(к которому оформлена страховка🧾) после *01.09.2020?*'
    q4_choise = InlineKeyboardMarkup(row_width=2)
    button8 = InlineKeyboardButton(text='Да✅, после 01.09.20', callback_data='yes4')
    button9 = InlineKeyboardButton(text='Нет🚫, до 01.09.20', callback_data='no4')
    q4_choise.add(button8, button9)
    await bot.send_message(chat_id=call.from_user.id, text=q4, reply_markup=q4_choise, parse_mode="MarkDown")
@dp.callback_query_handler(text='no4')
async def check_no4(call):
    no4mes = (f'*К сожалению*, если ваш кредит, к которому была оформлена страховка, *был выдан до 01.09.2020*, то возврат части стоимости страховки при досрочном погашении кредита *невозможен*, так как требования закона о возврате вступили в силу с 01.09.2020.\n'
             f'По страховкам оформленным до 01.09.2020 возможен возврат стоимости страховки в течение 14 дней(*период охлаждения*🥶) с момента оформления полиса.\n'
             f' Чтобы узнать в каких еще случаях возможен возврат части стоимости страховки нажми кнопку🖲 ниже.')
    dfind = InlineKeyboardMarkup()
    button10 = InlineKeyboardButton(text='🔬Другие причины возврата', callback_data='noev')
    dfind.insert(button10)
    await bot.send_message(chat_id=call.from_user.id, text=no4mes, parse_mode="MarkDown", reply_markup=dfind)

@dp.callback_query_handler(text='yes4')
async def check_yes5(call):
    yes4mes = (f'✅Если кредит выдан *после 01.09.2020* страховая компания обязана осуществить возврат части неиспользованной страховки при досрочном погашении кредита *согласно ФЗ-353*.\n'
                f'⚠ Страховые компании неохотно идут на возврат денег клиентам💰. Поэтому они придумывают *разные схемы*🤬 обхода требований федерального закона.\n'
                f'Чаще всего встречаются *следующие схемы обмана клиентов*:\n'
                f'☑ Клиенту оформляется *несколько страховых полисов*.  Возврат возможен только по одному из них(как правильно по самому дешевому), по остальным страховая компания будет настаивать, что они не обеспечивают кредит, а значит возврат по ним не предусмотрен🚫\n'
                f'☑ Клиенту оформляется *один полис с несколькими рисками*.  Страховая компания осуществит возврат стоимости по одному риску, а по остальным рискам страховая компания будет настаивать, что они не обеспечивают кредит,  значит возврат по ним не предусмотрен🚫\n')

    await bot.send_message(chat_id=call.from_user.id, text=yes4mes, parse_mode="MarkDown")
    sleep(2)
    help2 = InlineKeyboardMarkup()
    help2.insert(button3)
    yes4mes1 = f'Но есть и другие схемы по которым страховые компании пытаются обмануть🤥 своих клиентов и не возвращать деньги за страхование. *Если вам кажется, что по вашей страховке используется одна из таких схем* - направьте фото документов на проверку через раздел *"Обратная связь"*💌.'
    await bot.send_message(chat_id=call.from_user.id, text=yes4mes1, reply_markup=help2, parse_mode="MarkDown")
    sleep(2)
    yes4mes2 = f'Сколько страховых полисов вам было оформлено при *выдаче кредита*?'
    q5_choise = InlineKeyboardMarkup(row_width=2)
    button8 = InlineKeyboardButton(text='1️⃣ полис', callback_data='1')
    button9 = InlineKeyboardButton(text='2️⃣ и более', callback_data='2')
    q5_choise.add(button8, button9)
    await bot.send_message(chat_id=call.from_user.id, text=yes4mes2, reply_markup=q5_choise, parse_mode="MarkDown")
@dp.callback_query_handler(text='2')
async def check_2p(call):
    text2p = (f'При оформлении *нескольких полисов*, страховые компании предусматривают возврат части стоимости страховки только по одному из них. *Как правило, на этот полис приходится не более 10-15% от общей суммы оплаченной за страхование*.\n' 
            f'Страховой риск, который обеспечивает кредит *указывается в индивидуальных условиях(ИУ) к кредиту*.\n' 
            f'Вы можете *самостоятельно определить* по какому полису(в нём должен быть страховой риск/риски указанные в ИУ) возможен возврат части стоимости страховки, либо *направьте нам на экспертизу сканы/фотографии своих страховок и ИУ к кредиту* с помощью раздела "*Обратная связь*"💌.\n'  
            f'Мы изучим вашу документацию и оперативно *направим вам ответ по перспективам возврата части стоимости страховки* в соответствии с ФЗ-353.')
    help3 = InlineKeyboardMarkup()
    help3.insert(button3)
    await bot.send_message(chat_id=call.from_user.id, text=text2p, reply_markup=help3, parse_mode="MarkDown")
@dp.callback_query_handler(text='1')
async def check_2p(call):
    text1p = (f'*Согласно ФЗ-353📑 при полном досрочном погашении кредита заемщик имеет право на возврат части стоимости страхования за неиспользованный период*. \n'
            f'❇️ *Период с момента оформления страховки до момента  досрочно погашения кредита* - те деньги, которые заработала страховая компания.\n'
            f'✳️ *Период с момента полного досрочного погашения кредита до момента окончания действия полиса*- те деньги, которые вы можете вернуть.\n'
            f'Расчёт по данным периодам осуществляется *пропорционально*.\n'
            f'*Пример*: Полис действует с *01.05.2022 по 30.04.2023*. Досрочное погашение кредита произошло *01.10.2022*. Стоимость страховки - *100 000* руб.\n' 
            f'Страховка действовала *153* дня. С момента погашения кредита остается еще *212* дней.\n'
            f'Страховая компания заработала: *100 000 руб. / 365 (срок страхования 1 год) х 153 = 41 917 руб.*\n'
            f'Вы имеете право вернуть: *100 000 руб. / 365 х 212 =  58 028 руб*.')
    await bot.send_message(chat_id=call.from_user.id, text=text1p, parse_mode="MarkDown")
    sleep(1)
    text1p1 = f'⚠️ *Рекомендуем убедиться, что ваша страховка оформлена в качестве обеспечения кредита*. Для этого необходимо сравнить страховое покрытие указанное в *индивидуальных условиях(условия для применения пониженной ставки по кредиту)* со страховым покрытием указанным в оформленном страховом полисе. '
    await bot.send_message(chat_id=call.from_user.id, text=text1p1, parse_mode="MarkDown")
    sleep(1)
    text1p2 = (f'*Возврат стоимости возможен если*:\n'
            f'✅ от страхования зависит льготные условия по кредиту (например, *пониженная ставка*).\n'
            f'✅ *выгодоприобретателем по полису является банк*, а не застрахованный.\n'
            f'✅ страховая сумма *уменьшается на размер погашенной задолженности* по кредиту.')
    dfindd = InlineKeyboardMarkup()
    dfindd.insert(button2)
    await bot.send_message(chat_id=call.from_user.id, text=text1p2, parse_mode="MarkDown", reply_markup=dfindd)
    sleep(2)
    text1p3 = f'Если вы не уверены в возможности возврата или не нашли признаков указанных выше, нажмите 🖲кнопку *"Не нашёл признаков"*.'
    dfind = InlineKeyboardMarkup()
    button10 = InlineKeyboardButton(text='🔬Не нашёл признаков', callback_data='noev')
    dfind.insert(button10)
    await bot.send_message(chat_id=call.from_user.id, text=text1p3, reply_markup=dfind, parse_mode="MarkDown")
@dp.callback_query_handler(text='noev')
async def noevid(call):
    noevmes = (f'✅*В некоторых случаях возможен возврат стоимости страхования по отдельным рискам*. \n'
                f'Как правило, страховщики не осуществляют проверку клиентов при оформлении полиса банком. Поэтому возможны случаи неправомерного оформления страхования по рискам, которые не могут🚫 осуществиться/состояться.\n'
                f'*Пример* 1️⃣. Вы будучи инвалидом♿️ оформили страхование с риском "Инвалидность".  Так как нельзя повторно получить инвалидность, вы можете претендовать на возврать стоимости страхования по данному риску.\n'
                f'*Пример* 2️⃣. Вы будучи военнослужащим💂🏻‍♀️ или ИПшником оформили страхование с риском "Потеря работы". Как правило, военнослужащие и ИПшники являются исключениями по страхованию по данному риску.\n'
                f'Соответственно, вы можете претендовать на возврат стоимости страхования по данному риску, так как страховая компания взяла с вас деньги за то, что не может осуществиться/состояться.')
    dfind = InlineKeyboardMarkup()
    dfind.insert(button3)
    await bot.send_message(chat_id=call.from_user.id, text=noevmes, parse_mode="MarkDown", reply_markup=dfind)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)