from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def authorization() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    button = KeyboardButton(text="Войти")
    builder.add(button)
    return builder.adjust(1).as_markup(resize_keyboard=True)
    
def get_number() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    button = KeyboardButton(text='Отправить номер', request_contact=True)
    builder.add(button)
    return builder.adjust(1).as_markup(resize_keyboard=True, input_field_placeholder="Нажмите на кнопку!")