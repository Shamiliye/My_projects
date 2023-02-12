from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Определяем экземпляры классов для обычной и inline клавиатур
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb_photo_menu = ReplyKeyboardMarkup(resize_keyboard=True)
ikb = InlineKeyboardMarkup(row_width=2)

#"Создаём" кнопки для обычной клавиатуры главного меню
kb_start = KeyboardButton('/start')
kb_help = KeyboardButton('/help')
kb_description = KeyboardButton('/description')
kb_get_photo = KeyboardButton('Random photo')
kb_get_location = KeyboardButton('/location')

#Добавляем кнопки в экземпляр класса
kb.add(kb_start, kb_help).add(kb_description).insert(kb_get_photo).add(kb_get_location)

#"Создаём" кнопки для обычной клавиатуры меню с рандомными фотками
kb_random = KeyboardButton(text="Случайное фото")
kb_main_menu = KeyboardButton(text="Главное меню")

#Добавляем кнопки в экземпляр класса
kb_photo_menu.add(kb_random, kb_main_menu)

#"Создаём" кнопки для inline клавиатуры
ib1 = InlineKeyboardButton(text="😻",
                           callback_data="Кайф")
ib2 = InlineKeyboardButton(text="😒",
                           callback_data="Ну такое...")
ib3 = InlineKeyboardButton(text="Следующее фото",
                           callback_data="Следующее фото")
ib4 = InlineKeyboardButton(text="Главное меню",
                           callback_data="main")

#Добавляем кнопки в экземпляр класса inine клавиатуры
ikb.add(ib1, ib2).add(ib3).add(ib4)