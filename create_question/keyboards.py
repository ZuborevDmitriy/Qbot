import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import database.request as rq
from config.config import PAGE_COUNT
from aiogram.filters.callback_data import CallbackData
import emoji

async def first()->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Отправить сейчас", callback_data="send_photo"))
    builder.add(InlineKeyboardButton(text="Отложить", callback_data="chose_city"))
    return builder.adjust(1).as_markup()


async def second(next: str)->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Следующий пункт>>>", callback_data=f"{next}"))
    return builder.adjust(1).as_markup()

#Если фотографию отправили сразу
async def city(page: int, back: str):
    button_data = await rq.get_cities()
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    builder = InlineKeyboardBuilder()
    first_item = PAGE_COUNT*page
    last_item = first_item+PAGE_COUNT
    for item in button_data[first_item:last_item]:
        builder.row(InlineKeyboardButton(text=item, callback_data=f"city_{item}"))
    buttons = []
    if page >= 1:
        buttons.append(InlineKeyboardButton(text="<<<", callback_data=f"citypage_{page-1}_{pages}"))
    if page < pages:
        buttons.append(InlineKeyboardButton(text=">>>", callback_data=f"citypage_{page+1}_{pages}"))
    builder.row(*buttons)
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup(resize_keyboard=True)
#Если фотографии сразу не отправлили
async def city1(page: int):
    button_data = await rq.get_cities()
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    builder = InlineKeyboardBuilder()
    first_item = PAGE_COUNT*page
    last_item = first_item+PAGE_COUNT
    for item in button_data[first_item:last_item]:
        builder.row(InlineKeyboardButton(text=item, callback_data=f"city_{item}"))
    buttons = []
    if page >= 1:
        buttons.append(InlineKeyboardButton(text="<<<", callback_data=f"citypage_{page-1}_{pages}"))
    if page < pages:
        buttons.append(InlineKeyboardButton(text=">>>", callback_data=f"citypage_{page+1}_{pages}"))
    builder.row(*buttons)
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel)
    return builder.as_markup(resize_keyboard=True)


async def commercial_name(page: int, city: str, back: str):
    button_data = await rq.get_comm(city)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    builder = InlineKeyboardBuilder()
    first_item = PAGE_COUNT*page
    last_item = first_item+PAGE_COUNT
    for item in button_data[first_item:last_item]:
        builder.row(InlineKeyboardButton(text=item, callback_data=f"comm_{item}"))
    buttons = []
    if page >= 1:
        buttons.append(InlineKeyboardButton(text="<<<", callback_data=f"commpage_{page-1}_{pages}"))
    if page < pages:
        buttons.append(InlineKeyboardButton(text=">>>", callback_data=f"commpage_{page+1}_{pages}"))
    builder.row(*buttons)
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup(resize_keyboard=True)


async def project_name(page: int, comm: str, back: str):
    button_data = await rq.get_projects(comm)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    builder = InlineKeyboardBuilder()
    first_item = PAGE_COUNT*page
    last_item = first_item+PAGE_COUNT
    for item in button_data[first_item:last_item]:
        builder.row(InlineKeyboardButton(text=item, callback_data=f"project_{item}"))
    buttons = []
    if page >= 1:
        buttons.append(InlineKeyboardButton(text="<<<", callback_data=f"projectpage_{page-1}_{pages}"))
    if page < pages:
        buttons.append(InlineKeyboardButton(text=">>>", callback_data=f"projectpage_{page+1}_{pages}"))
    builder.row(*buttons)
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup(resize_keyboard=True)


async def back(back: str)->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup()


async def third_step(page: int, back: str):
    button_data = await rq.get_albums()
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    builder = InlineKeyboardBuilder()
    first_item = PAGE_COUNT*page
    last_item = first_item+PAGE_COUNT
    for item in button_data[first_item:last_item]:
        builder.row(InlineKeyboardButton(text=item.name, callback_data=f"album_{item.name}"))
    buttons = []
    if page >= 1:
        buttons.append(InlineKeyboardButton(text="<<<", callback_data=f"albumpage_{page-1}_{pages}"))
    if page < pages:
        buttons.append(InlineKeyboardButton(text=">>>", callback_data=f"albumpage_{page+1}_{pages}"))
    builder.row(*buttons)
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup(resize_keyboard=True)

async def choise(back: str, quest: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Да', callback_data=f'{quest}_true'))
    builder.row(InlineKeyboardButton(text='Нет', callback_data=f'{quest}_false'))
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup(resize_keyboard=True)

async def state_of_work(back: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=emoji.emojize(':keycap_1:'), callback_data="state_1"),
                InlineKeyboardButton(text=emoji.emojize(':keycap_2:'), callback_data="state_2"),
                InlineKeyboardButton(text=emoji.emojize(':keycap_3:'), callback_data="state_3"),
                InlineKeyboardButton(text=emoji.emojize(':keycap_4:'), callback_data="state_4"),
                InlineKeyboardButton(text=emoji.emojize(':keycap_5:'), callback_data="state_5"),
                InlineKeyboardButton(text=emoji.emojize(':keycap_6:'), callback_data="state_6"),
                InlineKeyboardButton(text=emoji.emojize(':keycap_7:'), callback_data="state_7"))
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup(resize_keyboard=True)


async def type(back: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Можно пропустить", callback_data="skip"))
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup()


async def last_step_with_photo_without_file(back: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Прикрепить файл", callback_data="add_file"))
    builder.row(InlineKeyboardButton(text="Подытожить", callback_data="conclude"))
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup()
async def last_step_with_photo_with_file(back: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Подытожить", callback_data="conclude"))
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup()

async def last_step_without_photo(back: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Прикрепить фото", callback_data="send_photo"))
    builder.row(InlineKeyboardButton(text="Фотографии отсутствуют", callback_data="end_without_photo"))
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup()
async def last_step_without_photo_without_file(back: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Прикрепить файл", callback_data="add_file"))
    builder.row(InlineKeyboardButton(text="Подытожить", callback_data="conclude_without"))
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup()
async def last_step_without_photo_with_file(back: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Подытожить", callback_data="conclude_without"))
    inline_button_back = InlineKeyboardButton(text="Назад", callback_data=f"{back}")
    inline_button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    builder.row(inline_button_cancel, inline_button_back)
    return builder.as_markup()


async def end() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Отправить", callback_data="send"))
    builder.add(InlineKeyboardButton(text="Изменить значение", callback_data="change_line"))
    builder.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return builder.as_markup()


async def change_line() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    button1 = InlineKeyboardButton(text=emoji.emojize(':keycap_1:'), callback_data="change_1")
    button2 = InlineKeyboardButton(text=emoji.emojize(':keycap_2:'), callback_data="change_2")
    button3 = InlineKeyboardButton(text=emoji.emojize(':keycap_3:'), callback_data="change_3")
    button4 = InlineKeyboardButton(text=emoji.emojize(':keycap_4:'), callback_data="change_4")
    builder.row(button1,button2,button3,button4)
    return builder.as_markup(resize_keyboard=True)

async def back_to_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="В меню", callback_data="cancel"))
    return builder.as_markup()