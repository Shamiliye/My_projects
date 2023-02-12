from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from KeyBoardFile import kb, kb_photo_menu, ikb
import random

TOKEN_API = "Токен бота Телеграм"

bot = Bot(TOKEN_API)  # Создаём экземпляр класса бот
dp = Dispatcher(bot)

HELP_COMMAND = """<b>/start</b> - <em>Запуск бота</em>
<b>/help</b> - <em>cписок всех команд</em>
<b>/description</b> - <em>описание бота</em>
<b>/menu</b> - <em>менюшка для получания случайного фото животного</em>
<b>/location</b> - <em>дропнет Вам рандомные координаты на карте</em>
"""  # Текст который будет выведен при нажатии на кнопку /help в самом боте

photo_list = ["https://damion.club/uploads/posts/2022-01/1643187296_6-damion-club-p-pikchi-s-kotikami-7.jpg",
              "https://prodota.ru/forum/uploads/profile/photo-174859.jpg",
              "https://mem-baza.ru/_ph/1/2/396113713.jpg?1600932362"]  # Список фото

desc_photo_list = ["Котик в ведре",
                   "На фотке по-настоящему крутой пёс",
                   "Вам хомяк звонит по Фэйстайму, могли бы и ответить"]  # Список подписей к фото

photos = dict(zip(photo_list, desc_photo_list))  # Генерация словаря на основе списка фото и cписка подписей
random_photo = random.choice(list(photos.keys()))  # Выбор рандомного фото по ключу словаря

flag = False  # Флаг, который используется для определения понравилось тебе фото ранее или нет

async def on_startup(_):
    print("Я запущен. Во время оффлайн режима не работал:)")

async def send_random(message: types.Message):
    "Вынесли функцию для дальнейшего более удобного её использования"
    global random_photo  # глобальные переменные лучше не использовать, но на момент создания бота я не совсем понимал как корректно их избежать
    random_photo = random.choice(list(photos.keys()))  # выбираем рандомное фото из предварительно подготовленного списка
    await bot.send_photo(chat_id=message.chat.id,
                         photo=random_photo,
                         caption=photos[random_photo],
                         reply_markup=ikb)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    "То, что пользователь увидит при запуске бота"
    await bot.send_message(chat_id=message.chat.id,
                           text="<b>Здравствуйте, вы запустили меня</b>",
                           parse_mode="HTML",
                           reply_markup=kb)
    await message.delete()

@dp.message_handler(Text(equals='Random photo'))
async def open_new_menu(message: types.Message):
    await message.answer(text="Случайное фото",
                         reply_markup=ReplyKeyboardRemove())
    await send_random(message)
    await message.delete()

@dp.message_handler(Text(equals='Главное меню'))
async def open_main_menu(message: types.Message):
    await message.answer(text='Вы вернулись в главное меню',
                         reply_markup=kb)
    await message.delete()

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML")
    await message.delete()

@dp.message_handler(commands=["description"])
async def description_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Я могу отправить тебе фото случайного животного, а ещё и рандомную локацию)",
                           parse_mode="HTML")
    await bot.send_sticker(chat_id=message.chat.id,
                           sticker="CAACAgIAAxkBAAEHi9lj2qqP5lh_IyxlmemHwBGnBKEVNQACbRQAAvh48Ev_35tLbqKxRy4E")
    await message.delete()

@dp.message_handler(commands=["location"])
async def location_command(message: types.Message):
    await bot.send_location(chat_id=message.chat.id,
                            latitude=random.randint(-90, 90),
                            longitude=random.randint(-180, 180))
    await message.delete()

@dp.callback_query_handler()
async def callback_random_photo(callback: types.CallbackQuery):
    global random_photo
    global flag
    if callback.data == "Кайф":
        if not flag:
            await callback.answer("Вам понравилась данная фотокарточка")
            flag = not flag
        else:
            await callback.answer("Я знаю, что Вам понравилось данное фото)")
    elif callback.data == "Ну такое...":
        await callback.answer("Эээ, ну ты чего?")
    elif callback.data == 'main':
        await callback.message.answer(text="Добро пожаловать в главное меню!",
                                      reply_markup=kb)
        await callback.message.delete()
        await callback.answer()
    else:
        random_photo = random.choice(list(filter(lambda x: x != random_photo, list(photos.keys()))))
        await callback.message.edit_media(types.InputMedia(media=random_photo,
                                                           type='photo',
                                                           caption=photos[random_photo]),
                                          reply_markup=ikb)
        await callback.answer()

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
