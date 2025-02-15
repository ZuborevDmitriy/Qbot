from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import emoji

def main_table() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    text1 = f"Создать вопрос {emoji.emojize(':pencil:')}"
    button1 = InlineKeyboardButton(text=text1, callback_data='create_query')
    text2 = f"Активные вопросы {emoji.emojize(':closed_mailbox_with_raised_flag:')}"
    button2 = InlineKeyboardButton(text=text2, callback_data='active_query')
    text3 = f"Архив вопросов {emoji.emojize(':card_index_dividers:')}"
    button3 = InlineKeyboardButton(text=text3, callback_data='archive_query')
    text4 = f"DEV {emoji.emojize(':radioactive:')}"
    button4 = InlineKeyboardButton(text=text4, callback_data='list_queries_to_update')
    builder.add(button1,button2,button3, button4)
    return builder.adjust(1).as_markup()