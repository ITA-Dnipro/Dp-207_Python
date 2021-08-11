from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# main menu buttons
btn_random = KeyboardButton('rnd number')
btn_other = KeyboardButton('other')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_random, btn_other)


# weather menu
btn_info = KeyboardButton('info')
