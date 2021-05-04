from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import emoji


def lang():
    lang_keyboard = InlineKeyboardMarkup()
    lang_keyboard.row_width = 2
    lang_keyboard.add(InlineKeyboardButton(f'{emoji.FLAG_RUSSIA}Рус', callback_data="rus"),
                      InlineKeyboardButton(f'{emoji.FLAG_UNITED_STATES}Eng', callback_data="eng"))
    return lang_keyboard


def menu(lang):
    if lang == 'rus':
        menu_keyboard_rus = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        menu_keyboard_rus.add(KeyboardButton(text=f"Где я на Марсе?",
                                             request_location=True),
                              KeyboardButton(text=f"Список моих мест"))
        return menu_keyboard_rus
    elif lang == 'eng':
        menu_keyboard_eng = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        menu_keyboard_eng.add(KeyboardButton(text=f"Where I'm on Mars?",
                                             request_location=True),
                              KeyboardButton(text=f"List of my places"))
        return menu_keyboard_eng