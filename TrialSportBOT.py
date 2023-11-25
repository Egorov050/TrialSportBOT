import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
import random
import time
from dotenv import load_dotenv
import os


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())



headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1; rv:50.0) Gecko/20100101 Firefox/50.0'"}
from time import sleep
import sqlite3

bot = Bot('6859006541:AAF_R9o5sL_eB1lbf-X9EaZ1iAZyTKLQthw')
dp = Dispatcher(bot=bot)

reg = ReplyKeyboardMarkup(resize_keyboard=True)
reg.add('Авторицазия')

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEK0YFlYmevgt6L--g7qg-VLV98SXiQsgAC5g8AApfOyUvclxraX1_eZTME')
    await message.answer(text='''Привет!👋 
    
Сначала, тебе нужно пройти авторизацию''', reply_markup=reg)



@dp.message_handler(text='Инфо 💬')
async def conactss(message: types.Message):
    await message.answer(
        '''Привет!
        
Я Теллеграм-бот🤖 сети специализированных спортивных магазинов *«Триал-Спорт»*.
     
Снаряжение, одежда и аксессуары для активного отдыха и спорта! 🏆🚲Велосипеды горные шоссейные и bmx, роликовые коньки, скейтборды,лонгборды и самокаты, горные и беговые лыжи, сноуборды, ледовые коньки и хоккейная экипировка, товары для альпинизма и скалолазания, туристическое снаряжение
     
_Чтобы начать работу со мной, следуй в меню_''', parse_mode='Markdown')


async def m_loading(m):
    loading = 1
    for count in range(100):
        loading += count + random.randint(1,2)
        if loading >= 100:
            await m.edit_text(f"Processing completed... 100%")
            break
        await m.edit_text(f"{m.text} {loading}%")
        time.sleep(3)


conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 user_id INTEGER, 
                 username TEXT,
                 full_name TEXT)''')

conn.commit()

async def register_user(user_id, username, full_name):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (user_id, username, full_name) VALUES (?, ?, ?)", (user_id, username, full_name))
        conn.commit()

async def login(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        await bot.send_message(user_id, "Вы успешно вошли в систему!")
        print(f"User with ID {user_id} logged in")  # Логируем действие
        return True
    else:
        await bot.send_message(user_id, "Вы не зарегистрированы. Воспользуйтесь командой /register для регистрации.")
        print(f"User with ID {user_id} is not registered")
        return False



@dp.message_handler(text= 'Авторицазия')
async def register(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    await register_user(user_id, username, full_name)
    await message.answer(f'''Авторицазия прошла успешно✅️ 
    
Добро пожаловать в Trial Sport, {message.from_user.first_name}''',
                             reply_markup=main)
    await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEK0XFlYmPVT24jikxMpB1rk5jx1LGjvgACMxsAAqCmGEltI19cYm5i8TME')



# Заказ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Инфо 💬').add('Посмотреть каталог 🔎').add('Посмотреть адреса магазинов📍').add('Посмотреть адреса сервисов📍').add('Как работает этот бот?🤷‍').add("Отправить файл с кодом бота 🗂")

@dp.message_handler(lambda message: message.text == 'Отправить файл с кодом бота 🗂')
async def send_file(message: types.Message):
    with open('/Users/vladimiregorov/PycharmProjects/lessons/botttt.py', 'rb') as file:
        await message.answer_document(file)





cataloge_list = InlineKeyboardMarkup(row_width=2)
cataloge_list.add(
    InlineKeyboardButton(text='skies', callback_data='skies'),
    InlineKeyboardButton(text='skipoles', callback_data='skipoles'),
    InlineKeyboardButton(text='roadbikes', callback_data='roadbikes'),
    InlineKeyboardButton(text='bmx', callback_data='bmx'))


@dp.message_handler(text='Посмотреть каталог 🔎')
async def conacts(message: types.Message):
   await bot.send_message(message.from_user.id, 'Выбери категорию', reply_markup=cataloge_list)



categories_links = {
    "skies": "https://trial-sport.ru/gds.php?s=51533&c1=1070639&c2=1078363&gpp=20&pg=",
    "skipoles": "https://trial-sport.ru/gds.php?change_price=&s=51533&c1=1070639&discount=1&c2%5B%5D=1078266&price_from=&price_to=&sort=",
    "roadbikes": "https://trial-sport.ru/gds.php?s=51516&c1=1070639&c2=1070790&gpp=20&pg=",
    "bmx": "https://trial-sport.ru/gds.php?s=51516&c1=1070639&c2=1073338&gpp=20&pg="
}

categories_pages = {
    "skies": 4,
    "skipoles": 6,
    "roadbikes": 4,
    "bmx": 10
}

import sqlite3

conn = sqlite3.connect('goods_data.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS goods
            (id TEXT PRIMARY KEY, photo TEXT, title TEXT, brand TEXT, collection TEXT, discount TEXT, link TEXT)''')


def fetch_goods_data(category):
    all_goods_data = {}
    for count in range(1, categories_pages[category] + 1):
        url = categories_links[category] + str(count)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        data = soup.find_all("div", class_="object ga")
        for index, item in enumerate(data):
            good_id = f"{category}_{count}_{index}"
            all_goods_data[good_id] = {
                "photo": "https://trial-sport.ru/" + item.find("img").get("src"),
                "title": item.find("a", class_="title").text,
                "brand": item.find("span", class_="blue").text,
                "collection": item.find("span", class_="collection").text,
                "discount": item.find("span", class_="discount").text,
                "link": "https://trial-sport.ru/" + item.find("a", class_="title").get("href")
            }
            c.execute('INSERT OR IGNORE INTO goods VALUES (?, ?, ?, ?, ?, ?, ?)',
                      (good_id, all_goods_data[good_id]["photo"], all_goods_data[good_id]["title"],
                       all_goods_data[good_id]["brand"], all_goods_data[good_id]["collection"],
                       all_goods_data[good_id]["discount"], all_goods_data[good_id]["link"]))
        sleep(3)
    conn.commit()
    return all_goods_data


async def send_goods_data(brand, chat_id, offset=0):
    c.execute("SELECT * FROM goods WHERE brand =?", (brand,))
    rows = c.fetchall()

    for row in rows[offset:offset + 5]:
        message = f"_Описание_: {row[2]}\n\n_Коллекция_: {row[4]}\n\n_Цена со скидкой_: {row[5]}\n\n_Ссылка на товар_: {row[6]}"
        await bot.send_message(chat_id, message, parse_mode='Markdown')

    if offset + 5 < len(rows):
        await bot.send_message(chat_id, "Нажми на Next чтобы увидеть больше",
                               reply_markup=types.InlineKeyboardMarkup().add(
                                   types.InlineKeyboardButton(text="Next", callback_data=f"next_{offset + 5}_{brand}")))


@dp.callback_query_handler(lambda query: query.data.startswith('next_'))
async def send_next_goods_data(callback_query: types.CallbackQuery):
    _, offset, brand = callback_query.data.split('_')
    chat_id = callback_query.message.chat.id
    await send_goods_data(brand, chat_id, int(offset))


@dp.callback_query_handler(text='skies')
async def get_goods_data(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    skies = callback_query.data
    m = await bot.send_message(callback_query.from_user.id, "💬Парсю данные с сайта https://trial-sport.ru")
    await m_loading(m)
    sleep(5)
    all_goods_data = fetch_goods_data(skies)
    await send_goods_data(user_id, all_goods_data)
    await bot.send_message(callback_query.from_user.id, 'Выберите бренд:', reply_markup=brand_list_skipoles)


brand_list_skipoles = InlineKeyboardMarkup(row_width=2)
brand_list_skipoles.add(
    InlineKeyboardButton(text='Tisa', callback_data='Tisa'),
    InlineKeyboardButton(text='Rossignol', callback_data='Rossignol'),
    InlineKeyboardButton(text='Fischer', callback_data='Fischer'),
    InlineKeyboardButton(text='One Way', callback_data='OneWay'))


@dp.callback_query_handler(text='Rossignol')
async def send_skies(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Rossignol", chat_id)


@dp.callback_query_handler(text='Tisa')
async def send_skies(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Tisa", chat_id)


@dp.callback_query_handler(text='Fischer')
async def send_skies(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Fischer", chat_id)


@dp.callback_query_handler(text='One Way')
async def send_skies(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("One Way", chat_id)


brand_list_roadbikes = InlineKeyboardMarkup(row_width=2)
brand_list_roadbikes.add(
    InlineKeyboardButton(text='Cannondale', callback_data='Cannondale'),
    InlineKeyboardButton(text='Corratec', callback_data='Corratec'),
    InlineKeyboardButton(text='GT', callback_data='GT'),
    InlineKeyboardButton(text='Jamis', callback_data='Jamis'),
    InlineKeyboardButton(text='Mongoose', callback_data='Mongoose'),
    InlineKeyboardButton(text='Nirve', callback_data='Nirve'),
    InlineKeyboardButton(text='Outleap', callback_data='Outleap'), )


@dp.callback_query_handler(text='roadbikes')
async def get_goods_data1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    roadbikes = callback_query.data
    m = await bot.send_message(callback_query.from_user.id, "💬Парсю данные с сайта https://trial-sport.ru")
    await m_loading(m)
    sleep(5)
    all_goods_data = fetch_goods_data(roadbikes)
    await send_goods_data(user_id, all_goods_data)
    await bot.send_message(callback_query.from_user.id, 'Выберите бренд:', reply_markup=brand_list_roadbikes)


@dp.callback_query_handler(text='Cannondale')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Cannondale", chat_id)


@dp.callback_query_handler(text='Corratec')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Corratec", chat_id)


@dp.callback_query_handler(text='GT')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("GT", chat_id)


@dp.callback_query_handler(text='Jamis')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Jamis", chat_id)


@dp.callback_query_handler(text='Mongoose')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Mongoose", chat_id)


@dp.callback_query_handler(text='Nirve')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Nirve", chat_id)


@dp.callback_query_handler(text='Outleap')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Outleap", chat_id)


brand_list_bmx = InlineKeyboardMarkup(row_width=2)
brand_list_bmx.add(
    InlineKeyboardButton(text='Eastern', callback_data='Eastern'),
    InlineKeyboardButton(text='GT', callback_data='GT'),
    InlineKeyboardButton(text='Outleap', callback_data='Outleap'),
    InlineKeyboardButton(text='Radio', callback_data='Radio'),
    InlineKeyboardButton(text='Mongoose', callback_data='Mongoose'),
    InlineKeyboardButton(text='WeThePeople', callback_data='WeThePeople'))


@dp.callback_query_handler(text='bmx')
async def get_goods_data1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    bmx = callback_query.data
    m = await bot.send_message(callback_query.from_user.id, "💬Парсю данные с сайта https://trial-sport.ru")
    await m_loading(m)
    sleep(5)
    all_goods_data = fetch_goods_data(bmx)
    await send_goods_data(user_id, all_goods_data)
    await bot.send_message(callback_query.from_user.id, 'Выберите бренд:', reply_markup=brand_list_bmx)


@dp.callback_query_handler(text='Radio')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Radio", chat_id)


@dp.callback_query_handler(text='Eastern')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Eastern", chat_id)


@dp.callback_query_handler(text='GT')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("GT", chat_id)


@dp.callback_query_handler(text='WeThePeople')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("WeThePeople", chat_id)


@dp.callback_query_handler(text='Mongoose')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Mongoose", chat_id)


@dp.callback_query_handler(text='Outleap')
async def send_roadbikes(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Outleap", chat_id)


brand_list_skipoles = InlineKeyboardMarkup(row_width=2)
brand_list_skipoles.add(
    InlineKeyboardButton(text='4KAAD', callback_data='4KAAD', ),
    InlineKeyboardButton(text='Exel', callback_data='Exel'),
    InlineKeyboardButton(text='Leki', callback_data='Leki'),
    InlineKeyboardButton(text='Loopline', callback_data='Loopline'),
    InlineKeyboardButton(text='One Way', callback_data='One Way'),
    InlineKeyboardButton(text='Rossignol', callback_data='Rossignol'),
    InlineKeyboardButton(text='Yoko', callback_data='Yoko'))


@dp.callback_query_handler(text='skipoles')
async def get_goods_data2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    skipoles = callback_query.data
    m = await bot.send_message(callback_query.from_user.id, "💬Парсю данные с сайта https://trial-sport.ru")
    await m_loading(m)
    sleep(5)
    all_goods_data = fetch_goods_data(skipoles)
    await send_goods_data(user_id, all_goods_data)
    await bot.send_message(callback_query.from_user.id, 'Выберите бренд:', reply_markup=brand_list_skipoles)


@dp.callback_query_handler(text='4KAAD')
async def send_skipoles(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("4KAAD", chat_id)


@dp.callback_query_handler(text='Exel')
async def send_skipoles(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Exel", chat_id)


@dp.callback_query_handler(text='Leki')
async def send_skipoles(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Leki", chat_id)


@dp.callback_query_handler(text='Loopline')
async def send_skipoles(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Loopline", chat_id)


@dp.callback_query_handler(text='One Way')
async def send_skipoles(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("One Way", chat_id)


@dp.callback_query_handler(text='Rossignol')
async def send_skipoles(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Rossignol", chat_id)


@dp.callback_query_handler(text='Yoko')
async def send_skipoles(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await send_goods_data("Yoko", chat_id)


# Заказ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Адреса магазинов///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

conn = sqlite3.connect('goods_data.db')
c = conn.cursor()


@dp.message_handler(text='Посмотреть адреса магазинов📍')
async def conacts(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите город🏡', reply_markup=cataloge_list_city)


cataloge_list_city = InlineKeyboardMarkup(row_width=2)
cataloge_list_city.add(
    InlineKeyboardButton(text='Москва', callback_data='Москва', ),
    InlineKeyboardButton(text='Санкт-Петербург', callback_data='Санкт-Петербург'),
    InlineKeyboardButton(text='Челябинск', callback_data='Челябинск'),
    InlineKeyboardButton(text='Новороссийск', callback_data='Новороссийск'))

c.execute('''CREATE TABLE IF NOT EXISTS address
            (address TEXT PRIMARY KEY, city TEXT)''')

cityd = {
    "Москва": "https://trialogues.ru/magaziny/moskovskaya-oblast/g-moskva",
    "Санкт-Петербург": "https://trialogues.ru/magaziny/leningradskaya-oblast/g-sankt-peterburg",
    "Челябинск": "https://trialogues.ru/magaziny/chelyabinskaya-oblast/g-chelyabinsk",
    "Новороссийск": "https://trialogues.ru/magaziny/krasnodarskiy-kray/g-novorossiysk"
}



def fetch_goods_data1(city):
    city1 = {}
    url = cityd.get(city)
    if url:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="g-table-score__item")
        for item in data:
            address = item.find("a", class_="g-table-score__name g-title-s").text
            city1[address] = {
                "address": city
            }
            if address:
                city1[address] = {"address": city}
                c.execute('INSERT OR IGNORE INTO address VALUES (?, ?)',
                          (address, city))
    conn.commit()
    return city1


async def send_goods_data1(city, chat_id):
    c.execute("SELECT address FROM address WHERE city = ?", (city,))
    rows = c.fetchall()
    addresses = [row[0] for row in rows]
    if addresses:
        address_text = "\n".join(addresses)
        await bot.send_message(chat_id, f"Адреса в городе *{city}*:\n_{address_text}_", parse_mode='Markdown')
    else:
        await bot.send_message(chat_id, f"Нет адресов для города {city}")


@dp.callback_query_handler(lambda query: query.data in cityd.keys())
async def process_city_selection(query: types.CallbackQuery):
    city = query.data
    chat_id = query.message.chat.id
    fetch_goods_data1(city)
    await send_goods_data1(city, chat_id)


# Адреса сервисов///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@dp.message_handler(text='Посмотреть адреса сервисов📍')
async def conactsss(message: types.Message):
    await bot.send_sticker(message.from_user.id,'CAACAgIAAxkBAAEK0Y9lYnN0m6rPpe3m86rUtXrjo6nIMAACKB8AAvm9GEo3bfObfzHpjzME')
    sleep(3)
    await bot.send_message(message.from_user.id, "_Упс, не могу установить соединение с сайтом. Попробуй еще раз или воспользуйся другой функцией_", parse_mode='Markdown')



@dp.message_handler(text='Как работает этот бот?🤷‍')
async def conactsss(message: types.Message):
    await bot.send_message(message.from_user.id,'''Итак,
основная идея бота заключается в парсинге данных, используя _lxml_ (он быстрее).
Мы находим на сайте нужный нам _html тэг_ с нужным классом и забираем данные. 
Эти данные изначально улетают в словарь, а оттуда уже в бд.
Абсолютно все данные, которые можно вытянуть из бота были, были взяты с двух сайтов:
- _https://trial-sport.ru_
- _https://trialogues.ru_'''
 ,parse_mode='Markdown')



if __name__ == '__main__':
    executor.start_polling(dp)


