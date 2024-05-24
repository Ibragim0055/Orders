import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

bot = Bot(token="6795561368:AAF_V-ZDgABhTER9jH3xiAM8jF1vpGNx5Ew")
dp = Dispatcher(storage=MemoryStorage())
ID_CHANNEL = -1002140554954
ID_GROUP = -1002066486603
ID_CHANNEL_SOT = -1002113161420

tema = {}
context_text = {}
context_user = {}
context_user_msg = {}

class context_sot1(StatesGroup):
    текст = State()

class context_sot(StatesGroup):
    user_id = State()
    тикет = State()
    тема = State()
    username = State()
    текст = State()
    id_message = State()

class context(StatesGroup):
    user_id = State()
    тикет = State()
    тема = State()
    id = State()
    текст = State()
    id_message = State()

class context1(StatesGroup):
    текст = State()

class context_message(StatesGroup):
    user_id = State()
    тикет = State()
    тема = State()
    id = State()
    текст = State()
    id_message = State()



@dp.message(Command('start'))
async def start(message: Message):
    a_button = InlineKeyboardButton(text='Депозит💸', callback_data='Депозит💸')
    b_button = InlineKeyboardButton(text='Вывод💰', callback_data='Вывод💰')
    c_button = InlineKeyboardButton(text='Ставки🎰', callback_data='Ставки🎰')
    d_button = InlineKeyboardButton(text='Бонусы🎁', callback_data='Бонусы🎁')
    e_button = InlineKeyboardButton(text='Реферальная система👥', callback_data='Реферальная система👥')
    f_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    g_button = InlineKeyboardButton(text='Сотрудничество🤝', callback_data='Сотрудничество🤝')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button], [c_button], [d_button], [e_button], [f_button], [g_button]])
    await bot.send_message(message.from_user.id, text=f"👋 Привет, <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>. Я помогу тебе с решением проблем на игровом проекте Pinto.\n\nВыбери тему для своего обращения ниже и задай свой вопрос!", reply_markup=button, parse_mode="HTML")




@dp.message(StateFilter(default_state))
async def reply(message: Message):
    global context_text, context_reply, context_delete
    if message.chat.type in ['group', 'supergroup']:
        if message.reply_to_message:
            for i in context_user:
                if context_user[i].id_message == message.reply_to_message.message_id:
                    if message.text == '/q' or message.text == '/r':
                        a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
                        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
                        tiket = context_user[i].тикет
                        await bot.send_message(i, text=f'Обращение {tiket} закрыто.', reply_markup=button)
                        await message.reply(f'Обращение {tiket} закрыто.')
                        del context_user[i]
                        id_msg = context_delete.get(i, 0)
                        await bot.unpin_chat_message(ID_CHANNEL, id_msg)
                    else:
                        context_reply = {i: message.message_id}
                        a_button = InlineKeyboardButton(text='Ответить', callback_data='Ответить')
                        b_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
                        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button]])
                        await bot.send_message(i, text=message.text, reply_markup=button)
                        context_text[message.reply_to_message.message_id] = message.from_user.id
                    break
            else:
               # await message.reply('Диалог закрыт!')
               pass
    if message.chat.id == ID_GROUP:
        try:
            user_id = context_text.get(message.forward_from_message_id, 0)
            text= f'Тикет: {context_user[user_id].тикет}\nТема: {context_user[user_id].тема}\n\nID: {context_user[user_id].id}\nТекст: {context_user[user_id].текст}'
            id_msg = await message.reply(text)
            id_msg = context_user[user_id].id_message = id_msg.message_id
        except:
            pass


            
@dp.callback_query(F.data == 'Ответить')
async def Ответить(callback: CallbackQuery, state: FSMContext):
    try:
        if context_user[callback.from_user.id]:
            await callback.message.answer('Введи текст для ответа.')
            await state.set_state(context1.текст)
        else:
            await callback.message.answer('Диалог закрыт!')
    except:
        await callback.message.answer('Диалог закрыт!')

@dp.message(StateFilter(context1.текст))
async def context_message(message: Message, state: FSMContext):
    try:
        user_id = context_user[message.from_user.id].user_id
        тикет = context_user[message.from_user.id].тикет
        тема = context_user[message.from_user.id].тема
        id = context_user[message.from_user.id].id
        id_msg = context_reply.get(message.from_user.id, 0)
        await message.answer('Ваше сообщение отправлено.\nОжидайте ответ.')
        id_msg = await bot.send_message(chat_id=ID_GROUP, text=f'Тикет: {тикет}\nТема: {тема}\n\nID: {id}\nТекст: {message.text}', reply_to_message_id=id_msg)
        context_user[message.from_user.id].id_message = id_msg.message_id
        context_user[message.from_user.id].текст = message.text
        await state.clear()
    except:
        await message.answer('Диалог закрыт!')




@dp.callback_query(F.data == 'Отменить обращение')
async def Отменить_обращение(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        id_msg = context_delete.get(user_id, 0)
        await bot.unpin_chat_message(ID_CHANNEL, id_msg)
        await bot.send_message(chat_id=ID_GROUP, text='Пользователь отменил обращение!', reply_to_message_id=context_user[callback.from_user.id].id_message)
        del context_delete[user_id]
        await callback.message.answer('Твое обращение успешно отменено.')
    except:
        await callback.message.answer('Твое обращение не было создано!')



            
@dp.callback_query(F.data == '🏠 В начало')
async def В_начало(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await start(callback)

async def dialog(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Да', callback_data='Да_ди')
    b_button = InlineKeyboardButton(text='Нет', callback_data='Нет_ди')
    button = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button]])
    await callback.message.answer('Внимание: при открытии нового обращения старое закроется.\nСоздать новое обращение?', reply_markup=button)

@dp.callback_query(F.data.in_(['Да_ди', 'Нет_ди']))
async def di(callback: CallbackQuery):
    if callback.data == 'Да_ди':
        del context_user[callback.from_user.id]
        await callback.message.edit_text('Старое обращение успешно закрылось.\nТеперь можете повторить новое обращение.')
        await start(callback)
    if callback.data == 'Нет_ди':
        await callback.message.edit_text('Благодарим за ответ.\nДождитесь обработки старого обращения.')
        await start(callback)




async def ввод(callback: CallbackQuery, state: FSMContext):
    for i in context_user:
        if context_user[i].user_id == callback.from_user.id:
            print('1')
            if context_user[i].id != None:
                print('2')
                await dialog(callback)
                break 
    else:
        a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
        await callback.message.answer('🤔Странно...\n\nПришли в чат свой ID для обработки запроса.', reply_markup=button)
        await state.set_state(context.id)

@dp.message(StateFilter(context.id))
async def ввод_id(message: Message, state: FSMContext):
    if message.from_user.id not in context_user:
        context_user[message.from_user.id] = context()
    context_user[message.from_user.id].id = message.text
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await message.answer('🙂Отлично!\n\nОпиши подробно свою проблему, а мы тебе поможем!', reply_markup=button)
    await state.set_state(context.текст)

@dp.message(StateFilter(context.текст))
async def ввод_текст(message: Message, state: FSMContext):
    global context_text, context_user, context_delete
    if message.from_user.id not in context_user:
        context_user[message.from_user.id] = context()
    context_user[message.from_user.id].текст = message.text
    while True:
        num = random.randint(1000000, 9999999)
        if num not in context_user:
            break
        else:
            print('есть')
    context_user[message.from_user.id].тикет = '№' + str(num)
    a_button = InlineKeyboardButton(text='Отменить обращение', callback_data='Отменить обращение')    
    b_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
    await message.answer(f'🏃‍♂️Бежим на помощь!\n\nОбращение номер №{num} создано.\nСреднее время ответа 15 минут.', reply_markup=button)
    text= f'Тикет: {context_user[message.from_user.id].тикет}\nТема: {context_user[message.from_user.id].тема}\n\nID: {context_user[message.from_user.id].id}\nТекст: {context_user[message.from_user.id].текст}'
    id_msg1 = await bot.send_message(ID_CHANNEL, text=text)
    await bot.pin_chat_message(ID_CHANNEL, id_msg1.message_id)
    context_user[message.from_user.id].id_message = id_msg1.message_id
    context_user[message.from_user.id].user_id = message.from_user.id
    context_text = {id_msg1.message_id: message.from_user.id}
    context_delete = {message.from_user.id: id_msg1.message_id}
    await state.clear()





@dp.callback_query(F.data == 'Депозит💸')
async def Депозит(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Не начислился депозит', callback_data='Не начислился депозит_Депозит')
    b_button = InlineKeyboardButton(text='Пришла не та сумма', callback_data='Пришла не та сумма_Депозит')
    c_button = InlineKeyboardButton(text='Не пришел бонус к депозиту', callback_data='Не пришел бонус к депозиту_Депозит')
    d_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    e_button = InlineKeyboardButton(text='Назад', callback_data='Назад_старт')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [c_button], [d_button, e_button]])
    await callback.message.answer('🤓Какой у тебя вопрос?', reply_markup=button)

@dp.callback_query(F.data == 'Не начислился депозит_Депозит')
async def Не_начислился_депозит_Депозит(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Меньше 2 часов', callback_data='Меньше 2 часов_Депозит')
    b_button = InlineKeyboardButton(text='Больше 2 часов', callback_data='Больше 2 часов_Депозит')
    c_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    d_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Депозит')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [c_button, d_button]])
    await callback.message.answer('⏳Сколько времени прошло с депозита?', reply_markup=button)

@dp.callback_query(F.data == 'Меньше 2 часов_Депозит')
async def Меньше_2_часов_Депозит(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await callback.message.answer('🔎Депозиты на сайт могут начисляться до 2х часов.\n\nЕсли по прошествии этого времени баланс не был пополнен, то обратись к нам еще раз - мы обязательно тебе поможем!', reply_markup=button)






@dp.callback_query(F.data == 'Больше 2 часов_Депозит')
async def Больше_2_часов_Депозит(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Депозит/Не начислился депозит'
    await ввод(callback, state)

@dp.callback_query(F.data == 'Пришла не та сумма_Депозит')
async def Пришла_не_та_сумма_Депозит(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Депозит/Пришла не та сумма'
    await ввод(callback, state)

@dp.callback_query(F.data == 'Не пришел бонус к депозиту_Депозит')
async def Не_пришел_бонус_к_депозиту_Депозит(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Депозит/Не пришел бонус к депозиту'
    await ввод(callback, state)
    

@dp.callback_query(F.data.in_(['Назад_старт', 'Назад_Депозит', 'Назад_Вывод', 'Назад_Не_пришел_Вывод', 'Назад_Ставки', 'Назад_Реферальная_система', 'Назад_Сотрудничество']))
async def Назад0(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Назад_старт':
        await start(callback)
    if callback.data == 'Назад_Депозит':
        await Депозит(callback)
    if callback.data == 'Назад_Вывод':
        await Вывод(callback)
    if callback.data == 'Назад_Не_пришел_Вывод':
        await Не_пришел_Вывод(callback)
    if callback.data == 'Назад_Ставки':
        await Ставки(callback)
    if callback.data == 'Назад_Реферальная_система':
        await Реферальная_система(callback)
    if callback.data == 'Назад_Сотрудничество':
        await Сотрудничество(callback)
    try:
        await state.clear()
    except:
        pass





@dp.callback_query(F.data == 'Вывод💰')
async def Вывод(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Не пришел вывод', callback_data='Не пришел вывод_Вывод')
    b_button = InlineKeyboardButton(text='Пришла не та сумма', callback_data='Пришла не та сумма_Вывод')
    d_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    e_button = InlineKeyboardButton(text='Назад', callback_data='Назад_старт')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [d_button, e_button]])
    await callback.message.answer('🤓Какой у тебя вопрос?', reply_markup=button)

@dp.callback_query(F.data == 'Не пришел вывод_Вывод')
async def Не_пришел_Вывод(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Да', callback_data='Да_Вывод')
    b_button = InlineKeyboardButton(text='Нет', callback_data='Нет_Вывод')
    d_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    e_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Вывод')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [d_button, e_button]])
    await callback.message.answer('🚀Тебе одобрили вывод на сайте?', reply_markup=button)

@dp.callback_query(F.data == 'Да_Вывод')
async def Да_Вывод(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Меньше одного дня', callback_data='Меньше одного дня_Вывод')
    b_button = InlineKeyboardButton(text='Больше одного дня', callback_data='Больше одного дня_Вывод')
    d_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    e_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Не_пришел_Вывод')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [d_button, e_button]])
    await callback.message.answer('⏳Сколько времени прошло с одобрения?', reply_markup=button)

@dp.callback_query(F.data == 'Меньше одного дня_Вывод')
async def Меньше_одного_дня_Вывод(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await callback.message.answer('🔎Выводы могут идти до одного дня, это нормально.\n\nЕсли по прошествии этого времени вывод не придет, то обратись к нам еще раз - мы обязательно тебе поможем!', reply_markup=button)

@dp.callback_query(F.data == 'Больше одного дня_Вывод')
async def Больше_одного_дня_Вывод(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Вывод/Не пришел вывод/Одобрили вывод'
    await ввод(callback, state)

@dp.callback_query(F.data == 'Нет_Вывод')
async def Нет_Вывод(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Меньше двух дней', callback_data='Меньше двух дней_Вывод')
    b_button = InlineKeyboardButton(text='Больше двух дней', callback_data='Больше двух дней_Вывод')
    d_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    e_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Не_пришел_Вывод')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [d_button, e_button]])
    await callback.message.answer('⏳Сколько времени прошло с создания заявки на вывод?', reply_markup=button)

@dp.callback_query(F.data == 'Меньше двух дней_Вывод')
async def Меньше_двух_дней_Вывод(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await callback.message.answer('🔎Одобрения вывода может задерживаться до двух дней.\n\nЕсли по прошествии этого времени вывод не одобрят, то обратись к нам еще раз - мы обязательно тебе поможем!', reply_markup=button)

@dp.callback_query(F.data == 'Больше двух дней_Вывод')
async def Больше_двух_дней_Вывод(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Вывод/Не пришел вывод/Не одобрили вывод'
    await ввод(callback, state)

@dp.callback_query(F.data == 'Пришла не та сумма_Вывод')
async def Пришла_не_та_сумма_Вывод(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Вывод/Пришла не та сумма'
    await ввод(callback, state)






@dp.callback_query(F.data == 'Ставки🎰')
async def Ставки(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Не пришел выигрыш', callback_data='Не пришел выигрыш_Ставки')
    b_button = InlineKeyboardButton(text='Пропала ставка', callback_data='Пропала ставка_Ставки')
    c_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    d_button = InlineKeyboardButton(text='Назад', callback_data='Назад_старт')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [c_button, d_button]])
    await callback.message.answer('🤓Какой у тебя вопрос?', reply_markup=button)

@dp.callback_query(F.data == 'Не пришел выигрыш_Ставки')
async def Не_пришел_выигрыш_Ставки(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Отображен', callback_data='Отображен_Ставки')
    b_button = InlineKeyboardButton(text='Не отображен', callback_data='Не отображен_Ставки')
    c_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    d_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Ставки')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [c_button, d_button]])
    await callback.message.answer('📝Внимательно проверь в своем профиле историю игр.\nТам отображен выигрыш?', reply_markup=button)

@dp.callback_query(F.data == 'Отображен_Ставки')
async def Отображен_Ставки(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await callback.message.answer('✅Если в истории отображен выигрыш, значит он пришел тебе на баланс.', reply_markup=button)

@dp.callback_query(F.data == 'Не отображен_Ставки')
async def Не_отображен_Ставки(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Ставки/Не пришел выигрыш/Не отображен'
    await ввод(callback, state)

@dp.callback_query(F.data == 'Пропала ставка_Ставки')
async def Пропала_ставка_Ставки(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Отображена', callback_data='Отображена_Ставки')
    b_button = InlineKeyboardButton(text='Не отображена', callback_data='Не отображена_Ставки')
    d_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    e_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Ставки')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [d_button, e_button]])
    await callback.message.answer('📝Внимательно проверь в своем профиле историю игр.\nТам отображена ставка?', reply_markup=button)

@dp.callback_query(F.data == 'Отображена_Ставки')
async def Отображена_Ставки(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await callback.message.answer('✅Если в истории отображена ставка, значит она играла!', reply_markup=button)

@dp.callback_query(F.data == 'Не отображена_Ставки')
async def Не_отображена_Ставки(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Ставки/Пропала ставка/Не отображена'
    await ввод(callback, state)





@dp.callback_query(F.data == 'Бонусы🎁')
async def Бонусы(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Не работает промокод', callback_data='Не работает промокод_Бонусы')
    b_button = InlineKeyboardButton(text='Не доступны бонусы', callback_data='Не доступны бонусы_Бонусы')
    c_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    d_button = InlineKeyboardButton(text='Назад', callback_data='Назад_старт')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [c_button, d_button]])
    await callback.message.answer('🤓Какой у тебя вопрос?', reply_markup=button)

@dp.callback_query(F.data == 'Не работает промокод_Бонусы')
async def Не_работает_промокод_Бонусы(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await callback.message.answer('🥺Значит у промокода закончились активации или его не сущевствует.', reply_markup=button)

@dp.callback_query(F.data == 'Не доступны бонусы_Бонусы')
async def Не_доступны_бонусы_Бонусы(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await callback.message.answer('🥺Если тебе не доступен ежедневный бонус, то сделай 2 простых шага и ты сможешь получить бонус:\n\n1. Заново привяжи свой телеграмм-аккаунт\n2. Переподпишись на наш телеграмм-канал', reply_markup=button)






@dp.callback_query(F.data == 'Реферальная система👥')
async def Реферальная_система(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Подключение RevShare', callback_data='Подключение Реферальная_система')
    b_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    c_button = InlineKeyboardButton(text='Назад', callback_data='Назад_старт')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button, c_button]])
    await callback.message.answer('🤓Какой у тебя вопрос?', reply_markup=button)

@dp.callback_query(F.data == 'Подключение Реферальная_система')
async def Подключение_RevShare_Реферальная_система(callback: CallbackQuery, state: FSMContext):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    b_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Реферальная_система')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button]])
    await callback.message.answer('👨‍💻Расскажи подробнее про свою деятельность и твой трафик. Опиши, чем ты занимаешься: может быть ютуб, стримы или ты веб-мастер.\n\nТакже пришли ссылку на свои ресурсы, это повысит твои шансы по подключению к системе RevShare!', reply_markup=button)
    await state.set_state(context_sot1.текст)

@dp.message(StateFilter(context_sot1.текст))
async def Подключение_RevShare_Реферальная_система_текст(message: Message, state: FSMContext):
    global context_text, context_user, context_delete
    while True:
        num = random.randint(1000000, 9999999)
        if num not in context_user:
            break
        else:
            print('есть')
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await message.answer('🙂Отлично!\n\nЕсли нам подойдет твоя заявка, то мы обязательно тебе напишем!', reply_markup=button)
    text= f'Тикет: №{str(num)}\nТема: Реферальная система/Подключение RevShare\n\nЮзернейм: @{message.from_user.username}\nТекст: {message.text}'
    await bot.send_message(ID_CHANNEL_SOT, text=text)
    await state.clear()








@dp.callback_query(F.data == 'Другой вопрос')
async def Другой_вопрос(callback: CallbackQuery, state: FSMContext):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await callback.message.answer('🤓Какой у тебя вопрос?', reply_markup=button)
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    context_user[callback.from_user.id].тема = 'Другой вопрос'
    context_user[callback.from_user.id].id = ' '
    await state.set_state(context.текст)








async def Сотрудничество_текст(callback: CallbackQuery, state: FSMContext):
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    b_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Сотрудничество')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button]])
    if context_user[callback.from_user.id].тема != 'Сотрудничество/Другое':
        await callback.message.answer('🔗Пришли ссылку на свой канал.', reply_markup=button)
    else:
        await callback.message.answer('✍Опиши свою деятельность или деятельность твоей компании.', reply_markup=button)
    await state.set_state(context_sot.текст)

@dp.message(StateFilter(context_sot.текст))
async def Сотрудничество_юзернейм(message: Message, state: FSMContext):
    context_user[message.from_user.id].текст = message.text
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    b_button = InlineKeyboardButton(text='Назад', callback_data='Назад_Сотрудничество')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button]])
    await message.answer('🌐Какой у тебя юзернейм в телеграме?', reply_markup=button)
    await state.set_state(context_sot.username)

@dp.message(StateFilter(context_sot.username))
async def Сотрудничество_тикет(message: Message, state: FSMContext):
    global context_text, context_user, context_delete
    context_user[message.from_user.id].username = message.text
    while True:
        num = random.randint(1000000, 9999999)
        if num not in context_user:
            break
        else:
            print('есть')
    context_user[message.from_user.id].тикет = '№' + str(num)   
    a_button = InlineKeyboardButton(text='🏠 В начало', callback_data='🏠 В начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await message.answer('🙂Отлично!\n\nЕсли нам подойдет твоя заявка, то мы обязательно тебе напишем!', reply_markup=button)
    text= f'Тикет: {context_user[message.from_user.id].тикет}\nТема: {context_user[message.from_user.id].тема}\n\nЮзернейм: {context_user[message.from_user.id].username}\nТекст: {context_user[message.from_user.id].текст}'
    await bot.send_message(ID_CHANNEL_SOT, text=text)
    await state.clear()








@dp.callback_query(F.data == 'Сотрудничество🤝')
async def Сотрудничество(callback: CallbackQuery):
    a_button = InlineKeyboardButton(text='Я ютубер', callback_data='Я ютубер')
    b_button = InlineKeyboardButton(text='Я стример', callback_data='Я стример')
    c_button = InlineKeyboardButton(text='Другое', callback_data='Другое_Сотрудничество')
    d_button = InlineKeyboardButton(text='Другой вопрос', callback_data='Другой вопрос')
    e_button = InlineKeyboardButton(text='Назад', callback_data='Назад_старт')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [c_button], [d_button, e_button]])
    await callback.message.answer('🤓Давай познакомимся!\nКто ты?', reply_markup=button)




@dp.callback_query(F.data.in_(['Я ютубер', 'Я стример', 'Другое_Сотрудничество']))
async def Сотрудничество_Я(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in context_user:
        context_user[callback.from_user.id] = context()
    else:
        del context_user[callback.from_user.id]
        context_user[callback.from_user.id] = context()
    if callback.data == 'Я ютубер':
        context_user[callback.from_user.id].тема = 'Сотрудничество/Я ютубер'
        await Сотрудничество_текст(callback, state)
    if callback.data == 'Я стример':
        context_user[callback.from_user.id].тема = 'Сотрудничество/Я стример'
        await Сотрудничество_текст(callback, state)
    if callback.data == 'Другое_Сотрудничество':
        context_user[callback.from_user.id].тема = 'Сотрудничество/Другое'
        await Сотрудничество_текст(callback, state)







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
