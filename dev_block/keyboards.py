import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import database.request as rq
from config.config import PAGE_COUNT
from aiogram.filters.callback_data import CallbackData
import emoji

async def dev_questions(page: int, user):
    button_data = await rq.get_dev_queries(user)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    builder = InlineKeyboardBuilder()
    first_item = PAGE_COUNT*page
    last_item = first_item+PAGE_COUNT
    for item in button_data[first_item:last_item]:
        builder.row(InlineKeyboardButton(text=f"{item}", callback_data=f"devquest_{item}"))
    buttons = []
    if page >= 1:
        buttons.append(InlineKeyboardButton(text="<<<", callback_data=f"devquestpage_{page-1}_{pages}"))
    if page < pages:
        buttons.append(InlineKeyboardButton(text=">>>", callback_data=f"devquestpage_{page+1}_{pages}"))
    builder.row(*buttons)
    return builder.as_markup(resize_keyboard=True)

async def dev_choise(param: int):
    builder = InlineKeyboardBuilder()
    text1 = "Обновить данные"
    button1 = InlineKeyboardButton(text=text1, callback_data=f'devupdate_{param}')
    text2 = "Закрыть вопрос"
    button2 = InlineKeyboardButton(text=text2, callback_data=f'devclose_{param}')
    builder.add(button1, button2)
    return builder.adjust(1).as_markup()