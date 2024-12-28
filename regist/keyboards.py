from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def authorization() -> InlineKeyboardMarkup:
    reg_k = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Войти', callback_data='regist')],
    ])
    return reg_k

def get_number() -> ReplyKeyboardMarkup:
    reg_numb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Отправить номер', request_contact=True)],
    ], resize_keyboard=True, input_field_placeholder='Нажмите на кнопку!')
    return reg_numb