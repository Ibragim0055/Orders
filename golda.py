import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import asyncpg
import pytz
from datetime import datetime

bot = Bot(token="7062461826:")
dp = Dispatcher(storage=MemoryStorage())

async def cr():
    conn = await asyncpg.connect(user='postgres', password='8967824ib', host='localhost', database='golda') 
    return conn 

async def golda_table():
    conn = await cr()
    await conn.execute('''create table gold (
    id BIGSERIAL PRIMARY KEY,
    user_id bigint unique,
	username text,
	balance bigint,
	sum_p bigint,
	sum_v bigint,
	referrals bigint,
	referrer bigint,
	user_start text
)''') 
    await conn.close() 

async def bot_table():
    conn = await cr()
    await conn.execute('''create table bot (
    id BIGSERIAL PRIMARY KEY,
    sum_v bigint,
	sum_users bigint,
	count_otziv bigint
)''') 
    await conn.close() 


async def data_start():
    moscow = pytz.timezone('Europe/Moscow')
    time = datetime.now(moscow)
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    return t


async def user_f(message: Message):
    conn = await cr()
    user = await conn.fetchrow('''SELECT * FROM gold WHERE user_id=$1''', message.from_user.id)
    return user


ID_CHANNEL_O = -1002094096537
ID_CHANNEL = -1002061793435

user_promo = {}
list_promo = {}
sum_user = {}
sum_user_v = {}
sum_user_p = {}


class kup_gold(StatesGroup):
    sum = State()

class kup_gold1(StatesGroup):
    sum = State()

class kup_gold2(StatesGroup):
    sum = State()


class viv(StatesGroup):
    sum = State()
    scrin = State()
    nik = State()

class pop(StatesGroup):
    sum = State()
    scrin = State()

class prom(StatesGroup):
    name = State()
    count = State()
    gold = State()

class prom_a(StatesGroup):
    name = State()



@dp.message(Command('start'))
async def start(message: Message):
    referrer_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    conn = await cr()
    user = await user_f(message)
    if user:
        await start_menu(message)
    else:
        await message.answer('Добро пожаловать в наш бот!')
        if referrer_id and int(referrer_id) != int(message.from_user.id):
            await bot.send_message(int(referrer_id), text=f"Вы пригласили нового<a href='tg://user?id={message.from_user.id}'> реферала! </a>", parse_mode='HTML')
            await conn.execute('''UPDATE gold SET referrals = referrals + 1 WHERE user_id=$1''', int(referrer_id)) 
            await conn.execute('''INSERT INTO gold (user_id, username, balance, sum_p, sum_v, referrals, referrer, user_start) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)''', message.from_user.id, message.from_user.username, 0, 0, 0, 0, int(referrer_id), await data_start()) 
        else:
            await conn.execute('''INSERT INTO gold (user_id, username, balance, sum_p, sum_v, referrals, referrer, user_start) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)''', message.from_user.id, message.from_user.username, 0, 0, 0, 0, None, await data_start()) 
        await conn.execute('''UPDATE bot SET sum_users = sum_users + 1''')
        await start_menu(message)


async def start_menu(message: Message):
    a_button = KeyboardButton(text='💰 Купить Gold')
    b_button = KeyboardButton(text='⚡ Вывести Gold')
    c_button = KeyboardButton(text='🔢 Посчитать')
    d_button = KeyboardButton(text='👤 Профиль')
    e_button = KeyboardButton(text='📖 Помощь')
    f_button = KeyboardButton(text='🤍 Отзывы')
    button   = ReplyKeyboardMarkup(keyboard=[[a_button, b_button], [c_button, d_button], [e_button, f_button]], resize_keyboard=True, one_time_keyboard=True)
    await bot.send_message(message.from_user.id, text='🏠 Главное меню\nДля взаимодействия с ботом используй клавиатуру.\n\nЧтобы перейти к покупке, перейди во вкладку «💰Купить Gold».\n\n📖 Если у тебя возникли вопросы, напиши нашей технической поддержке через копку "📖 Помощь"', reply_markup=button)

@dp.message(F.text == '🏠 Главное меню')
async def Главное_меню(message: Message, state: FSMContext):
    await state.clear()
    await start_menu(message)


@dp.message(F.text == '💰 Купить Gold')
async def КупитьГолду(message: Message, state: FSMContext):
    a_button = KeyboardButton(text='🏠 Главное меню')
    button   = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True, one_time_keyboard=True)
    await bot.send_message(message.from_user.id, text='🍯 Чтобы приобрести Голду, введи в чат сумму в рублях на которую хочешь пополнить баланс\n\n💡Например: 100', reply_markup=button)
    await state.set_state(kup_gold.sum)

@dp.message(StateFilter(kup_gold.sum))
async def КупитьГолду_ввод(message: Message, state: FSMContext):
    global sum_user
    if message.text.isdigit():
        if int(message.text) >= 30:
            sum = (int(message.text) * 0.20) + (int(message.text))
            sum_user = {}
            sum_user[message.from_user.id] = kup_gold()
            sum_user[message.from_user.id].руб = message.text
            sum_user[message.from_user.id].сумма = sum
            a_button = InlineKeyboardButton(text='Тинькофф', callback_data='Тинькофф')
            b_button = InlineKeyboardButton(text='Сбер', callback_data='Сбер')
            button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button]])
            await bot.send_message(message.from_user.id, text=f'💰 За {message.text} ₽ Вы получаете: {float(sum)}  G.\n\n👇 Выберите удобный для Вас способ оплаты:', reply_markup=button)
            await state.clear()
        else:
            await message.answer('⚠️ Минимальная сумма для пополнения 30 RUB')
    else:
        if message.text == '🏠 Главное меню':
            pass
        else:
            await message.answer('Отправьте сумму без лишних символов ⚠️')
    
        
@dp.callback_query(F.data.in_(['Тинькофф', 'Сбер', 'СБП']))
async def способ_пополнения(callback: CallbackQuery, state: FSMContext):
    try:
        rub = sum_user[callback.from_user.id].руб
        sum = sum_user[callback.from_user.id].сумма
        a_button = InlineKeyboardButton(text='<Изменить способ оплаты', callback_data='Изменить_способ_оплаты')
        button = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
        if callback.data == 'Тинькофф' or callback.data == 'Сбер':
            await callback.message.edit_text(f'☎️ Номер: <code>122</code>\n\nАлександр Сергеевич Б.\n\n💰 Сумма: {rub} RUB\n🍯 Игровая комиссия рынка на нас. Вам на аккаунт придет ровно: {sum}G.\n\n📸 После оплаты отправьте скриншот чека ⤵️', parse_mode='HTML', reply_markup=button)
            await state.set_state(pop.scrin)
    except:
       await bot.send_message(callback.from_user.id, text='Введите новую сумму!')
       await start_menu(callback)

@dp.callback_query(F.data == 'Изменить_способ_оплаты')
async def Изменить_способ_оплаты(callback: CallbackQuery):
    try:
        a_button = InlineKeyboardButton(text='Тинькофф', callback_data='Тинькофф')
        b_button = InlineKeyboardButton(text='Сбер', callback_data='Сбер')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button]])
        await callback.message.edit_text(f'💰 За {sum_user[callback.from_user.id].руб} ₽ Вы получаете: {sum_user[callback.from_user.id].сумма} G.\n\n👇 Выберите удобный для Вас способ оплаты:', reply_markup=button)
    except:
        await bot.send_message(callback.from_user.id, text='Введите новую сумму!')
        await start_menu(callback)



@dp.message(StateFilter(pop.scrin))
async def вывести_голды_scrin(message: Message, state: FSMContext):
    if message.photo:
        if message.from_user.id not in sum_user_p:
            sum_user_p[message.from_user.id] = pop()
            sum_user_p[message.from_user.id].sum = sum_user[message.from_user.id].сумма
            file = message.photo[-1].file_id
            sum_user_p[message.from_user.id].scrin = file
            await message.answer('Заявка успешна отправлена, ожидайте!')
            await start_menu(message)
            await state.clear()
            a_button = InlineKeyboardButton(text='Принять от пополнения', callback_data=f'{message.from_user.id}_p1')
            b_button = InlineKeyboardButton(text='Отказаться от пополнения', callback_data=f'{message.from_user.id}_o1')
            button = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
            await bot.send_photo(photo=sum_user_p[message.from_user.id].scrin, chat_id=1994579994, caption=f'ID: <code>{message.from_user.id}</code>\n\nСумма получения: {sum_user[message.from_user.id].сумма} G', reply_markup=button, parse_mode='HTML')
        else:
            await message.answer('Ваша заявка уже была отправлена!')
            await start_menu(message)
    else:
        if message.text == '🏠 Главное меню':
            pass
        else:
            await message.answer('Нужно фото!')
            await start_menu(message)
            await state.clear()


@dp.callback_query(F.data.endswith("_p1") | F.data.endswith("_o1"))
async def po(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[0])
    if callback.data[-3:] == '_p1':
        await callback.message.edit_caption(caption='Принято')
        await bot.send_message(user_id, text=f'Ваша заявка принята, вам пополнена {sum_user_p[user_id].sum} G!')
        conn = await cr()
        await conn.execute(f'''UPDATE gold SET balance = balance + {sum_user_p[user_id].sum} WHERE user_id=$1''', user_id) 
        await conn.execute(f'''UPDATE gold SET sum_p = sum_p + {sum_user_p[user_id].sum} WHERE user_id=$1''', user_id) 
    elif callback.data[-3:] == '_o1':
        await callback.message.edit_caption(caption='Отказано')
        await bot.send_message(user_id, text='Ваша заявка на пополнение отказана!')
    del sum_user_p[user_id]










@dp.message(F.text == '🔢 Посчитать')
async def посчитать(message: Message):
    a_button = KeyboardButton(text='🔢 Сколько денег за голду')
   # b_button = KeyboardButton(text='🔢 Сколько голды за денег')
    c_button = KeyboardButton(text='🏠 Главное меню')
    button = ReplyKeyboardMarkup(keyboard=[[a_button], [c_button]], resize_keyboard=True, one_time_keyboard=True)
    await bot.send_message(message.from_user.id, text='✨ Выберите вариант на клавиатуре', reply_markup=button)

@dp.message(F.text.in_(['🔢 Сколько денег за голду', '🔢 Сколько голды за денег']))
async def посчитать_с(message: Message, state: FSMContext):
    if message.text == '🔢 Сколько денег за голду':
        a_button = KeyboardButton(text='🏠 Главное меню')
        button = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('ℹ️ Сколько голды я получу за столько денег.\n\n✍️ Напишите сколько (RUB):', reply_markup=button)
        await state.set_state(kup_gold1.sum)
''' if message.text == '🔢 Сколько голды за денег':
        a_button = KeyboardButton(text='🏠 Главное меню')
        button = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('ℹ️ Сколько нужно денег что бы получить столько голды.\n\n✍️ Напишите сколько нужно голды:', reply_markup=button)
        await state.set_state(kup_gold2.sum)'''


@dp.message(StateFilter(kup_gold1.sum))
async def КупитьГолду1_ввод(message: Message, state: FSMContext):
    global sum_user
    if message.text.isdigit():
        sum = (int(message.text) * 0.20) + (int(message.text))
        sum_user = {}
        sum_user[message.from_user.id] = kup_gold1()
        sum_user[message.from_user.id].руб = message.text
        sum_user[message.from_user.id].сумма = sum
        a_button = InlineKeyboardButton(text='💰Купить Gold', callback_data='Купить голда')
        b_button = InlineKeyboardButton(text='🔢 Пересчитать', callback_data='Пересчитать')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
        await message.answer(f'🔢 За {message.text} ₽ Вы получите: {float(sum)} голды.', reply_markup=button)
        await state.clear()
    else:
        if message.text == '🏠 Главное меню':
            pass
        else:
            await message.answer('Отправьте сумму без лишних символов ⚠️')

'''
@dp.message(StateFilter(kup_gold2.sum))
async def КупитьГолду2_ввод(message: Message, state: FSMContext):
    global sum_user
    if message.text.isdigit():
        sum = (int(message.text)) - (int(message.text) * 0.20)
        sum_user = {}
        sum_user[message.from_user.id] = kup_gold2()
        sum_user[message.from_user.id].руб = message.text
        sum_user[message.from_user.id].сумма = sum
        a_button = InlineKeyboardButton(text='💰Купить Gold', callback_data='Купить голда')
        b_button = InlineKeyboardButton(text='🔢 Пересчитать', callback_data='Пересчитать')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
        await message.answer(f'🔢 За {message.text} ₽ Вы получите: {float(sum)} голды.', reply_markup=button)
        await state.clear()
    else:
        if message.text == '🏠 Главное меню':
            pass
        else:
            await message.answer('Отправьте сумму без лишних символов ⚠️')
'''

@dp.callback_query(F.data.in_(['Купить голда', 'Пересчитать']))
async def per_kup(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Купить голда':
        await КупитьГолду(callback, state)
    if callback.data == 'Пересчитать':
        await посчитать(callback)




@dp.message(F.text == '👤 Профиль')
async def profile(message: Message):
    a_button = InlineKeyboardButton(text='💰 Пригласи друга за деньги!', callback_data='Реферал')
    b_button = InlineKeyboardButton(text='🎁 Активировать промокод', callback_data='промо')
    button = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
    user = await user_f(message)
    await bot.send_message(message.from_user.id, text=f'🆔: <code>{message.from_user.id}</code>\n🍯 Баланс: {user[3]} G\n\n💵 Всего пополнено: на {user[4]} RUB\n🍯 Всего выведено: {user[5]} G\n\n⏳ Вы с нами: {user[8]} день', parse_mode='HTML', reply_markup=button)


@dp.callback_query(F.data == 'Реферал')
async def referral(callback: CallbackQuery):
    user = await user_f(callback)
    await callback.message.answer(f'🤑 Получай КЕШ за друзей! - Очень быстро и просто, подойдет для ВСЕХ!\n\n❗️Твоя задача заключается в том, чтобы делиться реферальной ссылкой с друзьями и в комментариях на разных площадках (телеграм, YouTube, ВКонтакте, Instagram и т.д.).\n\n🔥 Твой доход за пополнение друзей 3% от суммы пополнений!\n\n🤑 Вот пример: ты рассказываешь своему другу о нашем магазине и делишься ссылкой. Он покупает 1000G, а ты получаешь 30G, за усердные старания, выдаётся бонус, за успешное сотрудничество!\n\n🔗 Ваша реферальная ссылка:\n<code>https://t.me/Purple_gold_shop_bot?start={callback.from_user.id}</code>\n\n📤 Отправьте её вашим друзьям. Если Ваш друг зарегистрируется по ссылке и купит у нас голду, то вы получите процент с его покупок!\n\n👤 У вас {user[6]} рефералов.', parse_mode='HTML')




@dp.message(F.text == '📖 Помощь')
async def помощь(message: Message):
    a_button = InlineKeyboardButton(text='1️⃣', callback_data='1')
    b_button = InlineKeyboardButton(text='2️⃣', callback_data='2')
    c_button = InlineKeyboardButton(text='3️⃣', callback_data='3')
    d_button = InlineKeyboardButton(text='4️⃣', callback_data='4')
    e_button = InlineKeyboardButton(text='5️⃣', callback_data='5')
    f_button = InlineKeyboardButton(text='👨‍💻 Поддержка', url='tg://user?id=6442173169')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button, c_button], [d_button, e_button], [f_button]])
    await message.answer('❔ Часто задаваемые вопросы:\n\n1. Как пользоваться Вашим ботом?\n2. Сколько по времени проверяют чек?\n3. Сколько по времени выводят Голду?\n4. Безопасно ли у нас покупать?\n5. Как получить Голду бесплатно?\n\nЕсли Вы не смогли найти ответ на свой вопрос, нажмите "👨‍💻 Поддержка"', reply_markup=button)


@dp.callback_query(F.data.in_(['1', '2', '3', '4', '5']))
async def помощь_ответ(callback: CallbackQuery):
    back_button = InlineKeyboardButton(text='< Назад', callback_data='backn')
    if callback.data == '1':
        a_button = InlineKeyboardButton(text='📖 Инструкция', url='https://t.me/purple_gold_shop_canal/2')
        button = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
        await callback.message.edit_text('Ответ на 1️⃣ вопрос:\n\nЕще раз Привет, друг! Мы рады видеть тебя в нашем магазине!\n\nИнструкцию как пользоваться ботом ты можешь в нашем канале, либо перейти по кнопке "📖 Инструкция"', reply_markup=button)
    if callback.data == '2':
        a_button = InlineKeyboardButton(text='⏳ Прошло больше 24 часов!', url='tg://user?id=6442173169')
        button2 = InlineKeyboardMarkup(inline_keyboard=[[a_button], [back_button]])
        await callback.message.edit_text('Ответ на 2️⃣ вопрос:\n\nЧеки проверяются в ручную, а не автоматически. Сотрудники не смогут проверить чек, если Вы пополнили в позднее время или раним вечером. До 24 часов максимум может занимать проверка чека.', reply_markup=button2)
    if callback.data == '3':
        a_button = InlineKeyboardButton(text='⏳ Прошло больше 24 часов!', url='tg://user?id=6442173169')
        button2 = InlineKeyboardMarkup(inline_keyboard=[[a_button], [back_button]])
        await callback.message.edit_text('Ответ на 3️⃣ вопрос:\n\nВывод игровой валюты занимает до 24 часов. Мы стараемся вывести ее как можно скорее! Если Вы ждете долгое время то скорее всего сотрудник взял перерыв или Ваш скин трудно найти.', reply_markup=button2)
    if callback.data == '4':
        button = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
        await callback.message.edit_text('Ответ на 4️⃣ вопрос:\n\nВесь товар в нашем магазине, получен честным путем. Мы тщательно проверяем каждого нашего поставщика на способы получения игровой валюты. Если Вы сомневаетесь, то рекомендуем приобрести на официальном сайте игры.', reply_markup=button)
    if callback.data == '5':
        a_button = InlineKeyboardButton(text='🎁 Наш канал', url='https://t.me/purple_gold_shop_canal')
        b_button = InlineKeyboardButton(text='💰 Пригласи друга за деньги!', callback_data='Реферал')
        button = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [back_button]])
        await callback.message.edit_text('Ответ на 5️⃣ вопрос:\n\nТы можешь действительно и без обмана получить Голду двумя способами, которые доступны каждому!\n\n🎁 Принимай активное участие в нашем канале! Участвуй в конкурсах и забирай промокоды. Так ты действительно сможешь либо хорошо сэкономить, либо получить что то бесплатно!\n\nЕще один способ, это пригласить друга который купит у нас любой товар. Об этом ты можешь узнать подробнее нажав на кнопку!', reply_markup=button)

@dp.callback_query(F.data == 'backn')
async def помощь_назад(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='1️⃣', callback_data='1')
    b_button = InlineKeyboardButton(text='2️⃣', callback_data='2')
    c_button = InlineKeyboardButton(text='3️⃣', callback_data='3')
    d_button = InlineKeyboardButton(text='4️⃣', callback_data='4')
    e_button = InlineKeyboardButton(text='5️⃣', callback_data='5')
    f_button = InlineKeyboardButton(text='👨‍💻 Поддержка', url='tg://user?id=6442173169')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button, c_button], [d_button, e_button], [f_button]])
    await callback.message.edit_text('❔ Часто задаваемые вопросы:\n\n1. Как пользоваться Вашим ботом?\n2. Сколько по времени проверяют чек?\n3. Сколько по времени выводят Голду?\n4. Безопасно ли у нас покупать?\n5. Как получить Голду бесплатно?\n\nЕсли Вы не смогли найти ответ на свой вопрос, нажмите "👨‍💻 Поддержка"', reply_markup=button)



@dp.message(F.text == '🤍 Отзывы')
async def отзывы(message: Message):
    a_button = InlineKeyboardButton(text='🤍 Отзывы', url='https://t.me/Otzivi_purple_gold_shop')
    b_button = InlineKeyboardButton(text='📰 Новости', url='https://t.me/purple_gold_shop_canal')
    c_button = InlineKeyboardButton(text='👔 Владелец', url='tg://user?id=6442173169')
    d_button = InlineKeyboardButton(text='👨‍💻 Программист', url='tg://user?id=1994579994')
    button = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button], [c_button, d_button]])
    conn = await cr()
    user = await conn.fetchrow('''SELECT * FROM bot''')
    await message.answer(f'⭐️ STENDSHOP - Магазин по продаже игровой валюты. Радуем вас низкими ценами и быстрыми выводами! ⚡️\n\n🍯 Выведено через бота: {user[1]}\n🆔 Наших клиентов: {user[2]}\n\n📝 Количество отзывов: {user[3]}', reply_markup=button)








@dp.message(F.text == '⚡ Вывести Gold')
async def вывести_голды(message: Message, state: FSMContext):
    user = await user_f(message)
    if user[3] >= 100:
        if message.from_user.id not in sum_user_v:
            a_button = KeyboardButton(text='🏠 Главное меню')
            button = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True, one_time_keyboard=True)
            await message.answer('Введите сумму', reply_markup=button)
            await state.set_state(viv.sum)
        else:
            await message.answer('Ваша заявка уже была отправлена!') 
            await start_menu(message)
    else:
        await message.answer('❗️ Вывод работает от 100 G')

@dp.message(StateFilter(viv.sum))
async def вывести_голды_sum(message: Message, state: FSMContext):
    if message.text.isdigit():
        user = await user_f(message)
        if user[3] >= int(message.text):
            sum_user_v[message.from_user.id] = viv()
            sum_user_v[message.from_user.id].sum = int(message.text)
            await message.answer('Введите ник Standoff:')
            await state.set_state(viv.nik)
        else:
            await message.answer(f'На вашем балансе всего лишь {user[3]} G!')
            await start_menu(message)
            await state.clear()
    else:
        if message.text == '🏠 Главное меню':
            pass
        else:
            await message.answer('Отправьте сумму без лишних символов ⚠️')

@dp.message(StateFilter(viv.nik))
async def вывести_голды_nik(message: Message, state: FSMContext):
    sum_user_v[message.from_user.id].nik = message.text
    await message.answer('Отправьте скриншот скина:')
    await state.set_state(viv.scrin)
 

@dp.message(StateFilter(viv.scrin))
async def вывести_голды_scrin(message: Message, state: FSMContext):
    if message.photo:
        file = message.photo[-1].file_id
        sum_user_v[message.from_user.id].scrin = file
        user = await user_f(message)
        if user[3] >= sum_user_v[message.from_user.id].sum:
            conn = await cr()
            await conn.execute(f'''UPDATE gold SET balance = balance - {sum_user_v[message.from_user.id].sum} WHERE user_id=$1''', message.from_user.id) 
            await message.answer('Заявка успешна отправлена, ожидайте!')
            await start_menu(message)
            await state.clear()
            a_button = InlineKeyboardButton(text='Принять', callback_data=f'{message.from_user.id}_p')
            b_button = InlineKeyboardButton(text='Отказаться', callback_data=f'{message.from_user.id}_o')
            button = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
            await bot.send_photo(photo=sum_user_v[message.from_user.id].scrin, chat_id=1994579994, caption=f'ID: <code>{message.from_user.id}</code>\n\nНик Standoff: <code>{sum_user_v[message.from_user.id].nik}</code>\n\nСумма: {sum_user_v[message.from_user.id].sum} G', reply_markup=button, parse_mode='HTML')
    else:
        if message.text == '🏠 Главное меню':
            pass
        else:
            await message.answer('Нужно фото!')
            await start_menu(message)
            await state.clear()


@dp.callback_query(F.data.endswith("_p") | F.data.endswith("_o"))
async def po(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[0])
    if callback.data[-2:] == '_p':
        await callback.message.edit_caption(caption='Принято')
        conn = await cr()
        await conn.execute(f'''UPDATE gold SET sum_v = sum_v + {sum_user_v[user_id].sum} WHERE user_id=$1''', user_id) 
        await bot.send_message(user_id, text='Ваша заявка на скин была принята!')
        a_button = InlineKeyboardButton(text='⭐', callback_data='1 з')
        b_button = InlineKeyboardButton(text='⭐⭐', callback_data='2 з')
        c_button = InlineKeyboardButton(text='⭐⭐⭐', callback_data='3 з')
        d_button = InlineKeyboardButton(text='⭐⭐⭐⭐', callback_data='4 з')
        e_button = InlineKeyboardButton(text='⭐⭐⭐⭐⭐', callback_data='5 з')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [c_button], [d_button], [e_button]])
        await bot.send_message(user_id, text='Оценьте пожалуйста, как вам бот?', reply_markup=button)
    elif callback.data[-2:] == '_o':
        await callback.message.edit_caption(caption='Ваша заявка на скин была отказана')
        conn = await cr()
        await conn.execute(f'''UPDATE gold SET balance = balance + {sum_user_v[user_id].sum} WHERE user_id=$1''', user_id)
    del sum_user_v[user_id]


@dp.callback_query(F.data.in_(['1 з', '2 з', '3 з', '4 з', '5 з']))
async def ocen(callback: CallbackQuery):
    if callback.data == '1 з':
        await bot.send_message(ID_CHANNEL_O, text=f"<a href='tg://user?id={callback.from_user.id}'> Пользователь </a> получил скин и оценил!\n⭐", parse_mode='HTML')
    if callback.data == '2 з':
        await bot.send_message(ID_CHANNEL_O, text=f"<a href='tg://user?id={callback.from_user.id}'> Пользователь </a> получил скин и оценил!\n⭐⭐", parse_mode='HTML')
    if callback.data == '3 з':
        await bot.send_message(ID_CHANNEL_O, text=f"<a href='tg://user?id={callback.from_user.id}'> Пользователь </a> получил скин и оценил!\n⭐⭐⭐", parse_mode='HTML')
    if callback.data == '4 з':
        await bot.send_message(ID_CHANNEL_O, text=f"<a href='tg://user?id={callback.from_user.id}'> Пользователь </a> получил скин и оценил!\n⭐⭐⭐⭐", parse_mode='HTML')
    if callback.data == '5 з':
        await bot.send_message(ID_CHANNEL_O, text=f"<a href='tg://user?id={callback.from_user.id}'> Пользователь </a> получил скин и оценил!\n⭐⭐⭐⭐⭐", parse_mode='HTML')
    conn = await cr()
    await conn.execute(f'''UPDATE bot SET count_otziv = count_otziv + 1 WHERE user_id=$1''', callback.from_user.id)

"""
@dp.message(Command('promo'))
async def c_promo(message: Message, state: FSMContext):
    await message.answer('Введите название промокода:')
    await state.set_state(prom.name)

@dp.message(StateFilter(prom.name))
async def c_promo_name(message: Message, state: FSMContext):
    global list_promo, a
    list_promo[message.text] = prom()
    list_promo[message.text].name = message.text
    a = message.text
    await message.answer('Введите GOLD получение для каждого пользователя:')
    await state.set_state(prom.gold)

@dp.message(StateFilter(prom.gold))
async def c_promo_голд(message: Message, state: FSMContext):
    list_promo[a].gold = int(message.text)
    await message.answer('Введите количество активаций')
    await state.set_state(prom.count)

@dp.message(StateFilter(prom.count))
async def c_promo_count(message: Message, state: FSMContext):
    list_promo[a].count = int(message.text)
    await message.answer('Промокод добавлен!')
    await state.clear()







@dp.callback_query(F.data == 'промо')
async def промо(callback: CallbackQuery, state: FSMContext):
    a_button = KeyboardButton(text='🏠 Главное меню')
    button = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True, one_time_keyboard=True)
    await callback.message.answer('Введите промокод:', reply_markup=button)
    await state.set_state(prom_a.name)

@dp.message(StateFilter(prom_a.name))
async def промо_имя(message: Message, state: FSMContext):
    try:
        if message.text == '🏠 Главное меню':
            pass
        else:
            try:
                print(user_promo[message.from_user.id])
                await 
            list_promo[message.text].count -= 1
    except:
        await message.answer('Такой промокод не существует или закончился!')
        await start_menu(message)


"""



async def main():
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            await asyncio.sleep(3)
            continue

if __name__ == '__main__':
    asyncio.run(main())
