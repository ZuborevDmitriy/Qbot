from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
import database.request as rq
import regist.keyboards as regist_keyboard
import menu.keyboards as menu_keyboards
import emoji

class Register(StatesGroup):
    number = State()
    user_info = State()
    
regist_router = Router()

@regist_router.message(CommandStart())
async def start(message: Message):
    text = markdown.text("Здравствуйте, вас приветствует телеграм-бот <b>Вопрос по ПД</b>.",
                         "<u>Для начала вам необходимо авторизоваться</u>.", sep="\n")
    await message.answer(text=text, reply_markup=regist_keyboard.authorization())
    
@regist_router.message(F.text == 'Войти')
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.number)
    text = markdown.text("Для авторизации вам необходимо предоставить <b>номер вашего телефона</b>.")
    await message.answer(text=text, reply_markup=regist_keyboard.get_number())
    
@regist_router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    check_user = await rq.check_users(data['number'])
    if check_user == "1":
        await message.answer(text="Вы уже зарегистрированы!", reply_markup=menu_keyboards.main_table())
    if check_user == "2":
        await state.set_state(Register.user_info)
        await message.answer(text="Введите свое ФИО:", reply_markup=ReplyKeyboardRemove())
    if check_user == "3":
        await message.answer(text="Вашего номера нет в базе данных, похоже вы не сотрудник.", reply_markup=ReplyKeyboardRemove())
        
@regist_router.message(Register.user_info)
async def register_user_info(message:Message, state:FSMContext):
    await state.update_data(user_info=message.text)
    data = await state.get_data()
    await rq.reg_user(message.from_user.id, data['number'], data['user_info'])
    await message.answer(text="Вы успешно зарегистрированы!", reply_markup=menu_keyboards.main_table())
    await state.clear()