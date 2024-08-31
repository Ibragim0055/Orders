import io
import os
import shutil
import undetected_chromedriver as uc
from undetected_chromedriver import By
import time
import requests
import asyncio
from aiogram import Bot, F, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import pytz
from datetime import datetime


bot = Bot(token='7128343170:')

dp = Dispatcher(storage=MemoryStorage())

class post10(StatesGroup):
    txt = State()
    photo = State()
    phono_description = State()
    txt1 = State()
    photo1 = State()

class post100(StatesGroup):
    txt = State()
    photo = State()
    data = State()

class post1000(StatesGroup):
    url = State()

class chan(StatesGroup):
    cher = State()
    pub = State()


class post30(StatesGroup):
    photos = State()
    text = State()
    data = State()
    photos1 = State()


ID_CHANNEL_CHEr = -1002072763682
ID_CHANNEL_PUb = -1002055928288

links = list()
driver = None

uzum_url = ''

async def parse2(message: Message, tip):
    global links, driver
    links = list()
    await message.answer('Парсим сайт, это займёт несколько секунд. Пожалуйста не отправляйте ещё раз команду!')
    driver = uc.Chrome(use_subprocess=True)
    driver.get(uzum_url)
    
    for i in range(30):
            time.sleep(5)
            button = driver.find_elements(By.CLASS_NAME, 'pagination-navigation-wrapper')
            divs = driver.find_elements(By.CLASS_NAME, 'product-card-image')
            for div in divs:
                try:
                    span = div.find_element(By.XPATH, f".//span[text()='{tip}']")
                    links.append(div.find_element(By.TAG_NAME, 'a').get_attribute("href"))
                except:
                    continue
            
            button = button[-1].find_element(By.TAG_NAME, 'a').click()
            
            

            print(i)
        
            
    time.sleep(1)
    


    
    a_button = KeyboardButton(text='/parse')
    b_button = KeyboardButton(text='/post')
    button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Готово!', reply_markup=button)
    print(links)

@dp.message(Command('start'))
async def menu(message: Message):
    a_button = KeyboardButton(text='/parse')
    b_button = KeyboardButton(text='/post')
    c_button = KeyboardButton(text='Изменить канал отправки')
    button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f'Главное меню:\n\nID: <code>{message.from_user.id}</code>', reply_markup=button, parse_mode='HTML')


@dp.message(F.text == 'Изменить канал отправки')
async def izm(message: Message):
    a_button = KeyboardButton(text='Публичный канал')
    b_button = KeyboardButton(text='Черновик канал')
    c_button = KeyboardButton(text='Назад')
    button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Выберите:', reply_markup=button)

@dp.message(F.text == 'Публичный канал')
async def izm1(message: Message, state: FSMContext):
    await message.answer('Отправьте сюда айди канала:')
    await state.set_state(chan.pub)

@dp.message(StateFilter(chan.pub))
async def izm11(message: Message, state: FSMContext):
    global ID_CHANNEL_PUb
    try:
        channel = await bot.get_chat(message.text)
        print(channel)
        ID_CHANNEL_PUb = message.text
    except:
        await message.answer('Ошибка! Бот должен быть администратором в канале!')
        await menu(message)
    await state.clear()

@dp.message(F.text == 'Черновик канал')
async def izm2(message: Message, state: FSMContext):
    await message.answer('Отправьте сюда айди канала:')
    await state.set_state(chan.cher)

@dp.message(StateFilter(chan.cher))
async def izm22(message: Message, state: FSMContext):
    global ID_CHANNEL_PUb
    try:
        channel = await bot.get_chat(message.text)
        print(channel)
        ID_CHANNEL_PUb = message.text
    except:
        await message.answer('Ошибка! Бот должен быть администратором в канале!')
        await menu(message)
    await state.clear()



@dp.message((F.text.in_(['Отменить', 'Назад'])))
async def back(message: Message):
    await menu(message)



@dp.message(Command('parse'))
async def parse(message: Message):
    a_button = KeyboardButton(text='Парсить выбранную категорию')
    c_button = KeyboardButton(text='Назад')
    button = ReplyKeyboardMarkup(keyboard=[[a_button], [c_button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Выберите какую категорию парсить:', reply_markup=button)

@dp.message(F.text.in_(['Парсить выбранную категорию', 'Парсить всю категорию']))
async def parse1(message: Message, state: FSMContext):
    global uzum_url
    if message.text == 'Парсить всю категорию':
        uzum_url = 'https://uzum.uz/ru'
        a_button = KeyboardButton(text='Акция')
        b_button = KeyboardButton(text='Временная скидка')
        c_button = KeyboardButton(text='Скидка')
        d_button = KeyboardButton(text='Назад')
        button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button], [d_button]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Выберите что парсить:', reply_markup=button)
    else:
        await message.answer('Скиньте сюда ссылку на категорию')
        await state.set_state(post1000.url)

@dp.message(StateFilter(post1000.url))
async def parse0(message: Message, state: FSMContext):
    global uzum_url
    uzum_url = message.text
    if message.text.startswith('https://uzum.uz/'):
        a_button = KeyboardButton(text='Акция')
        b_button = KeyboardButton(text='Временная скидка')
        c_button = KeyboardButton(text='Скидка')
        d_button = KeyboardButton(text='Назад')
        button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button], [d_button]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Выберите что парсить:', reply_markup=button)
    else:
        await message.answer('Нужен сайт uzum!')
        await menu(message)
    await state.clear()


@dp.message(F.text.in_(['Акция', 'Временная скидка', 'Скидка']))
async def parse3(message: Message):
    global ID_CHANNEL_CHEr
    if message.text == 'Акция':
        await parse2(message, 'Акция')
    if message.text == 'Временная скидка':
        await parse2(message, 'Временная скидка')
    if message.text == 'Скидка':
        await parse2(message, 'Скидка')
    if message.text == 'Назад':
        pass
    await message.answer('Парсим сайт и отправляем в черновик канал. Пожалуйста не отправляйте ещё раз команду!')
    for link in links:
        driver.get(link)
        time.sleep(3)
        print(link)
        images = driver.find_elements(By.CLASS_NAME, 'image-wrapper')
        title = driver.find_element(By.TAG_NAME, 'h1').text
        try:
            price = driver.find_element(By.CLASS_NAME, 'price-wrapper').find_elements(By.TAG_NAME, 'span')
            price_new = price[0].get_attribute("textContent")
            price_old = price[1].get_attribute("textContent")
        except:
            continue
        print(f'{title}\nЦена сейчас: {price}\nРаньше: {price_old}')

        input_media = []
        for i, image in enumerate(images[:3]):
            image_elements = image.find_elements(By.TAG_NAME, 'img')
            if image_elements:
                image_url = image_elements[0].get_attribute("src")
                image_url1 = image_url.rfind('/')
                image_url = image_url[:image_url1+1] + 'original.jpg'


            p = requests.get(image_url)

    # Create the directory if it does not exist
            try:
                link = link.split('-')
                link = link[-1]
                os.makedirs(f"{link}", exist_ok=True)
            except:
                link = link[:link.find('?')]

    # Open the file in write mode
            with open(f"{link}_{i}.jpg", "wb") as out:
                out.write(p.content)
                print(p)
    
            await asyncio.sleep(1)
            input_media_photo = types.InputMediaPhoto(media=types.FSInputFile(f"{link}_{i}.jpg"))
            price_new = price_new.lstrip()
            price_old = price_old.lstrip()
            input_media_photo.caption = f"{title}\nЦена сейчас:\n{price_new}\nРаньше:\n{price_old}" if i == 0 else None
            input_media.append(input_media_photo)
            

            print(i)

        if input_media:
            await bot.send_media_group(ID_CHANNEL_CHEr, media=input_media)
            try:
                os.remove(f"{link}_0.jpg")
                os.remove(f"{link}_1.jpg")
                os.remove(f"{link}_2.jpg")
            except:
                try:
                    os.remove(f"{link}_0.jpg")
                    os.remove(f"{link}_1.jpg")
                except:
                    try:
                        os.remove(f"{link}_0.jpg")
                    except:
                        print('none')
            shutil.rmtree(link)

        print(i)


print('готово')


@dp.message(Command('post'))
async def post(message: Message):
    a_button = KeyboardButton(text='Добавить пост')
    b_button = KeyboardButton(text='Добавить пост из канала черновик')
    c_button = KeyboardButton(text='Назад')
    button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Выберите:', reply_markup=button)

@dp.message((F.text.in_(['Добавить пост', 'Назад'])))
async def post1(message: Message, state: FSMContext):
    if message.text == 'Назад':
        pass
    else:
        a_button = KeyboardButton(text='Отправить сейчас')
        b_button = KeyboardButton(text='Отправить по указанному времени')
        c_button = KeyboardButton(text='Отменить')
        button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Отправьте сюда фото:', reply_markup=button)
        await state.set_state(post10.photo)

@dp.message((F.text.in_(['Отправить сейчас', 'Отправить по указанному времени', 'Отменить'])))
async def post1111(message: Message, state: FSMContext):
    global i
    i = 0
    if message.text == 'Отменить':
        pass
    if message.text == 'Отправить сейчас':
        a_button = KeyboardButton(text='Отменить')
        button = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Отправьте сюда фото:', reply_markup=button)
        await state.set_state(post10.photo)
    if message.text == 'Отправить по указанному времени':
        await message.answer('Введите дату и время по московскому %Y-%M-%D %H:%M:%S. Пример: 2024-05-07 8:23:50')
        await state.set_state(post100.data)
    
i = 0
@dp.message(StateFilter(post10.photo))
async def photo(message: Message, state: FSMContext):
    global i
    if message.content_type == types.ContentType.PHOTO:
        user_id = message.from_user.id
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        src = 'data/new_post/' + str(user_id) + '/'
        os.makedirs(src, exist_ok=True)
        with open(src + str(len(os.listdir(src)) + 1) + '.jpg', 'wb') as new_file:
            new_file.write(downloaded_file.read())
        print(i)
        i+=1
        if i == 1:
            await message.answer('Введите описание:')
        await state.set_state(post10.txt)
    else:
        if message.text == 'Отменить':
            await state.clear()
        else:
            await message.answer('Нужно фото!')
            await state.clear()
            await menu(message)





@dp.message(StateFilter(post10.txt))
async def description(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.clear()
        shutil.rmtree(src)
    else:
        global ID_CHANNEL_PUb
        chat_id = ID_CHANNEL_PUb
        src = 'data/new_post/' + str(message.from_user.id) + '/'
        img_list = [os.path.join(src, f) for f in os.listdir(src)]
        
        media = []
        i = 0
        for img in img_list:
            # создаем объект для каждого фото
            input_media_photo = types.InputMediaPhoto(media=types.FSInputFile(img))
            input_media_photo.caption = message.text if i == 0 else None
            media.append(input_media_photo)
            i+=1

        # отправляем все фото вместе с описанием
        await bot.send_media_group(chat_id=chat_id, media=media)
        shutil.rmtree(src)
        await message.answer("Успешно опубликовано!")
        await state.clear()
        await menu(message)










data_t = ''
@dp.message(StateFilter(post100.data))
async def data(message: Message, state: FSMContext):
    global data_t, i
    i = 0
    data_t = message.text
    a_button = KeyboardButton(text='Отменить')
    button = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Отправьте сюда фото:', reply_markup=button)
    await state.set_state(post100.photo)


photo_t = []
i = 0
@dp.message(StateFilter(post100.photo))
async def photo(message: Message, state: FSMContext):
    global data_t, i
    if message.content_type == types.ContentType.PHOTO:
        user_id = message.from_user.id
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        data_t1 = data_t.replace('-', '').replace(':', '').replace(' ', '')
        src = 'data/new_post/' + str(data_t1) + '/'
        os.makedirs(src, exist_ok=True)
        with open(src + str(len(os.listdir(src)) + 1) + '.jpg', 'wb') as new_file:
            new_file.write(downloaded_file.read())
        i+=1
        if i == 1:
            await message.answer('Введите описание:')
        await state.set_state(post100.txt)
    else:
        if message.text == 'Отменить':
            await state.clear()
        else:
            await message.answer('Нужно фото!')
            await state.clear()
            await menu(message)


@dp.message(StateFilter(post100.txt))
async def description(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.clear()
        shutil.rmtree(src)
    else:
        global ID_CHANNEL_PUb
        chat_id = ID_CHANNEL_PUb
        data_t1 = data_t.replace('-', '').replace(':', '').replace(' ', '')
        src = 'data/new_post/' + str(data_t1) + '/'
        img_list = [os.path.join(src, f) for f in os.listdir(src)]
        
        media = []
        i = 0
        for img in img_list:
            # создаем объект для каждого фото
            input_media_photo = types.InputMediaPhoto(media=types.FSInputFile(img))
            input_media_photo.caption = message.text if i == 0 else None
            media.append(input_media_photo)
            i+=1
        global photo_t
        photo_t = media
        
        await message.answer(f"Успешно опубликовано! Будет отправлено в канал публичный в {data_t}!")
        await state.clear()
        await menu(message)
        class GreetingsScheduler:
            def __init__(self):
                self.schedule = {}  

            def add_schedule_time(self, time_str, greeting_text):
                self.schedule[time_str] = greeting_text

            async def send_greetings(self):
                for time_str, greeting_text in self.schedule.items():
                    date = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    date = pytz.timezone('Europe/Moscow').localize(date)
                    now = datetime.now(pytz.timezone('Europe/Moscow'))
                    delta = date - now

                    if delta.total_seconds() <= 0:
                        await bot.send_media_group(chat_id=chat_id, media=media)
                        asyncio.sleep(2)
                        shutil.rmtree(src)
                    else:
                        await asyncio.sleep(delta.total_seconds())
                        await bot.send_media_group(chat_id=chat_id, media=media)
                        asyncio.sleep(2)
                        shutil.rmtree(src)
        
        scheduler = GreetingsScheduler()
        scheduler.add_schedule_time(data_t, photo_t)
        await scheduler.send_greetings()















@dp.message(F.text == 'Добавить пост из канала черновик')
async def post3(message: Message, state: FSMContext):
    a_button = KeyboardButton(text='Указать время')
    b_button = KeyboardButton(text='Назад')
    button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Когда отправить?', reply_markup=button)

@dp.message(F.text == 'Указать время')
async def post33(message: Message, state: FSMContext):
    await message.answer('Введите дату и время по московскому %Y-%M-%D %H:%M:%S. Пример: 2024-05-07 8:23:50')
    await state.set_state(post30.data)

@dp.message(StateFilter(post30.data))
async def data(message: Message, state: FSMContext):
    global data_t, i
    i = 0
    data_t = message.text
    a_button = KeyboardButton(text='Отменить')
    button = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Перешлите сюда пост из канала черновика', reply_markup=button)
    await state.set_state(post30.photos)

textp = ''
i = 0
@dp.message(StateFilter(post30.photos))
async def post333(message: Message, state: FSMContext):
    global data_t, textp, i
    if message.content_type == types.ContentType.PHOTO:
        if i == 0:
            i+=1
            print(message.caption, "lellff")
            textp = message.caption
            print(i)
            a_button = KeyboardButton(text='Изменить описание')
            b_button = KeyboardButton(text='Изменить фото')
            c_button = KeyboardButton(text='Готово')
            d_button = KeyboardButton(text='Отменить')
            button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button], [d_button]], one_time_keyboard=True, resize_keyboard=True)
            await message.answer('Выберите:', reply_markup=button)
            i+=1
        user_id = message.from_user.id
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        data_t1 = data_t.replace('-', '').replace(':', '').replace(' ', '')
        src = 'data/new_post10/' + str(data_t1) + '/'
        os.makedirs(src, exist_ok=True)
        with open(src + str(len(os.listdir(src)) + 1) + '.jpg', 'wb') as new_file:
            new_file.write(downloaded_file.read())
        i+=1
            
    else:
        if message.text == 'Отменить':
            await state.clear()
        else:
            await message.answer('Нужно фото!')
            await state.clear()
            await menu(message)
    await state.clear()

photo_t = []

@dp.message(F.text == 'Готово')
async def post4(message: Message):
    global data_t, photo_t
    data_t1 = data_t.replace('-', '').replace(':', '').replace(' ', '')
    src = 'data/new_post10/' + str(data_t1) + '/'
    img_list = [os.path.join(src, f) for f in os.listdir(src)]
        
    media = []
    i = 0
    print(textp)
    for img in img_list:
            # создаем объект для каждого фото
        input_media_photo = types.InputMediaPhoto(media=types.FSInputFile(img))
        input_media_photo.caption = textp if i == 0 else None
        media.append(input_media_photo)
        i+=1
        print(textp)
    global photo_t
    photo_t = media
    chat_id = ID_CHANNEL_PUb
    print(media)
    await message.answer(f"Успешно опубликовано! Будет отправлено в канал публичный в {data_t}!")
    class GreetingsScheduler:
            def __init__(self):
                self.schedule = {}  

            def add_schedule_time(self, time_str, greeting_text):
                self.schedule[time_str] = greeting_text

            async def send_greetings(self):
                for time_str, greeting_text in self.schedule.items():
                    date = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    date = pytz.timezone('Europe/Moscow').localize(date)
                    now = datetime.now(pytz.timezone('Europe/Moscow'))
                    delta = date - now

                    if delta.total_seconds() <= 0:
                        await bot.send_media_group(chat_id=chat_id, media=media)
                        await message.answer('Пост опубликован в канал успешно!')
                        asyncio.sleep(2)
                        shutil.rmtree(src)
                        await menu(message)
                    else:
                        await asyncio.sleep(delta.total_seconds())
                        await bot.send_media_group(chat_id=chat_id, media=media)
                        await message.answer('Пост опубликован в канал успешно!')
                        asyncio.sleep(2)
                        shutil.rmtree(src)
                        await menu(message)
        
    scheduler = GreetingsScheduler()
    scheduler.add_schedule_time(data_t, photo_t)
    await scheduler.send_greetings()





@dp.message(F.text == 'Изменить описание')
async def post44(message: Message, state: FSMContext):
    await message.answer('Введите описание:')
    await state.set_state(post30.text)

@dp.message(StateFilter(post30.text))
async def post6(message: Message, state: FSMContext):
    global textp
    textp = message.text
    await message.answer('Описание изменено!')
    a_button = KeyboardButton(text='Изменить описание')
    b_button = KeyboardButton(text='Изменить фото')
    c_button = KeyboardButton(text='Готово')
    d_button = KeyboardButton(text='Отменить')
    button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button], [d_button]], one_time_keyboard=True, resize_keyboard=True)
    await message.answer('Выберите:', reply_markup=button)
    await state.clear()



@dp.message(F.text == 'Изменить фото')
async def post44(message: Message, state: FSMContext):
    global data_t
    await message.answer('Отправьте сюда фото:')
    await state.set_state(post30.photos1)
    data_t1 = data_t.replace('-', '').replace(':', '').replace(' ', '')
    src = 'data/new_post10/' + str(data_t1) + '/'
    shutil.rmtree(src)

@dp.message(StateFilter(post30.photos1))
async def photo(message: Message, state: FSMContext):
    global data_t, i, photo_t
    i = 0
    if message.content_type == types.ContentType.PHOTO:
        user_id = message.from_user.id
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        data_t1 = data_t.replace('-', '').replace(':', '').replace(' ', '')
        src = 'data/new_post10/' + str(data_t1) + '/'
        os.makedirs(src, exist_ok=True)
        with open(src + str(len(os.listdir(src)) + 1) + '.jpg', 'wb') as new_file:
            new_file.write(downloaded_file.read())
        i+=1
        if i == 1:
            await message.answer('Фото изменено!')
            a_button = KeyboardButton(text='Изменить описание')
            b_button = KeyboardButton(text='Изменить фото')
            c_button = KeyboardButton(text='Готово')
            d_button = KeyboardButton(text='Отменить')
            button = ReplyKeyboardMarkup(keyboard=[[a_button], [b_button], [c_button], [d_button]], one_time_keyboard=True, resize_keyboard=True)
            await message.answer('Выберите:', reply_markup=button)
            await state.clear()
    else:
        if message.text == 'Отменить':
            await state.clear()
        else:
            await message.answer('Нужно фото!')
            await state.clear()
            await menu(message)



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
