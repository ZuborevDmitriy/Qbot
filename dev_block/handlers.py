import math
import asyncio
import random
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import dev_block.keyboards as dbk
import database.request as rq
from config.config import PAGE_COUNT
from aiogram.utils.media_group import MediaGroupBuilder
import menu.keyboards as menu_keyboards
from python_kafka.producer import upd_with_kafka

dev_question_router = Router()

#Хэндлер для получения списка вопросов
@dev_question_router.callback_query(F.data == 'list_queries_to_update')
async def obtain_project_info(callback:CallbackQuery):
    user = await rq.get_FIO(callback.from_user.id)
    button_data = await rq.get_dev_queries(user)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    message_text = f"Выберите вопрос из списка ({1}/{int(pages)+1})"
    await callback.message.edit_text(text=message_text, reply_markup=await dbk.dev_questions(0, user))
#Хэндлер для пролистывания списка вопросов
@dev_question_router.callback_query(F.data.contains("devquestpage_"))
async def obtain_project_info(callback:CallbackQuery):
    user = await rq.get_FIO(callback.from_user.id)
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    message_text = f"Выберите вопрос из списка ({int(page)+1}/{int(pages)+1})"
    await callback.message.edit_text(text=message_text, reply_markup=await dbk.dev_questions(int(page), user))



#Хэндлер для обработки выбранного вопроса
@dev_question_router.callback_query(F.data.contains("devquest_"))
async def obtain_project_info(callback:CallbackQuery):
    query_id = callback.data.split("_")[1]
    message_text = "Что вы хотите сделать с вопросом?"
    await callback.message.edit_text(text=message_text, reply_markup=await dbk.dev_choise(query_id))
    
#Хэндлер для обновления выбранного вопроса
@dev_question_router.callback_query(F.data.contains("devupdate_"))
async def obtain_project_info(callback:CallbackQuery):
    query_id = callback.data.split("_")[1]
    list_code = [0, 0.1, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2, 2.1, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10, 4.11, 4.12, 4.13, 4.14, 4.15, 5, 5.1, 5.2, 5.3, 6, 6.1, 7, 7.1, 8, 8.1]
    change_code = random.choice(list_code)
    list_recomendation = ['Сойдет, неплохо.', 'Требуется устранить неточности.', 'Требуется больше информации.', 'Нужно построить зиккурат.', 'Необходимо исправить проблему.', 'Тут могла быть ваша рекомендация']
    recomendation = random.choice(list_recomendation)
    kafka_message = {
        'id': query_id,
        'change_code':change_code,
        'recomendation':recomendation,
        'devdate':str(datetime.now())
    }
    upd_with_kafka(dummy_message=kafka_message)
    message_text = 'Все сработало, можете проверить'
    await callback.message.edit_text(text=message_text, reply_markup= await dbk.go_to_menu())
    
#Хэндлер для закрытия выбранного вопроса
@dev_question_router.callback_query(F.data.contains("devclose_"))
async def obtain_project_info(callback:CallbackQuery):
    query_id = callback.data.split("_")[1]
    kafka_message = {
        'id': query_id,
        'status':'closed',
        'devdate':str(datetime.now())
    }
    upd_with_kafka(dummy_message=kafka_message)
    message_text = 'Все сработало, можете проверить'
    await callback.message.edit_text(text=message_text, reply_markup= await dbk.go_to_menu())