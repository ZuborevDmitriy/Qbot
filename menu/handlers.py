from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.methods.delete_message import DeleteMessage
import menu.keyboards as menu_keyboards
from create_question.handlers import Temp
menu_router = Router()
#Хэндлер для возвращения в меню для reply
@menu_router.message(F.text == "В меню")
async def get_projects_info(message: Message, bot:Bot, state:FSMContext):
    await state.set_state(Temp.nothing)
    data = await state.get_data()
    get_chat_id = message.chat.id
    for values in data.get('messages_id').values():
        await bot(DeleteMessage(chat_id=get_chat_id, message_id=values))
    await state.clear()
    await message.answer(text="Меню", reply_markup=menu_keyboards.main_table())