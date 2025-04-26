import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.request as rq
from config.config import PAGE_COUNT

async def active_questions(page: int, user):
    button_data = await rq.get_active_queries(user)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    builder = InlineKeyboardBuilder()
    first_item = PAGE_COUNT*page
    last_item = first_item+PAGE_COUNT
    for item in button_data[first_item:last_item]:
        builder.row(InlineKeyboardButton(text=f"{item}", callback_data=f"actquest_{item}"))
    buttons = []
    if page >= 1:
        buttons.append(InlineKeyboardButton(text="<<<", callback_data=f"actquestpage_{page-1}_{pages}"))
    if page < pages:
        buttons.append(InlineKeyboardButton(text=">>>", callback_data=f"actquestpage_{page+1}_{pages}"))
    builder.row(*buttons)
    return builder.as_markup(resize_keyboard=True)

async def back_to_menu(back: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    button1 = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    builder.row(button1)
    return builder.as_markup()