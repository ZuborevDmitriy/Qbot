from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import emoji

def main_table() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    button1 = KeyboardButton(text=f"Создать вопрос {emoji.emojize(':pencil:')}")
    button2 = KeyboardButton(text=f"Активные вопросы {emoji.emojize(':closed_mailbox_with_raised_flag:')}")
    button3 = KeyboardButton(text=f"Архив вопросов {emoji.emojize(':card_index_dividers:')}")
    button4 = KeyboardButton(text=f"DEV {emoji.emojize(':radioactive:')}")
    builder.add(button1,button2,button3, button4)
    return builder.adjust(1).as_markup(input_field_placeholder=f"Список функций{emoji.emojize(':gear:')}:")