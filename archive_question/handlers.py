import math
import asyncio
import random
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import archive_question.keyboards as aqk
import database.request as rq
from config.config import PAGE_COUNT
from aiogram.utils.media_group import MediaGroupBuilder
import menu.keyboards as menu_keyboards
import emoji

archive_question_router = Router()

#Хэндлер для получения списка вопросов
@archive_question_router.message(F.text == f"Архив вопросов {emoji.emojize(':card_index_dividers:')}")
async def obtain_project_info(message:Message):
    user = await rq.get_FIO(message.from_user.id)
    button_data = await rq.get_archive_queries(user)
    array_lenght = len(button_data)
    await message.reply(text="Переходим в архивные вопросы...")
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    await message.answer(text=f"Список архивных вопросов: {array_lenght}\nСтраниа {1} из {int(pages)+1}.\nВыберите вопрос из списка:", reply_markup=await aqk.archive_questions(0, user))
    


#Хэндлер для пролистывания списка вопросов
@archive_question_router.callback_query(F.data.contains("arcquestpage_"))
async def obtain_project_info(callback:CallbackQuery):
    user = await rq.get_FIO(callback.from_user.id)
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    message_text = f"Выберите вопрос из списка ({int(page)+1}/{int(pages)+1})"
    await callback.message.edit_text(text=message_text, reply_markup=await aqk.archive_questions(int(page), user))



#Хэндлер для обработки выбранного вопроса
@archive_question_router.callback_query(F.data.contains("arcquest_"))
async def obtain_project_info(callback:CallbackQuery, bot:Bot):
    query_id = callback.data.split("_")[1]
    query_info = await rq.get_archive_query(int(query_id))
    city_name = query_info.city_name
    commercial_name = query_info.commercial_name
    project_name = query_info.project_name
    comment = query_info.comment
    album = query_info.album
    system_quest = query_info.system_quest
    syst_q = ""
    match system_quest:
        case True : syst_q = "Да"
        case False : syst_q = "Нет"
    state_of_works = query_info.state_of_works
    economic_effect = query_info.economic_effect
    reduce_time = query_info.reduce_time
    type_of_note = query_info.type_of_note
    if type_of_note == None:
        type_of_note = "Не указано"
    POS = query_info.POS
    pos = ""
    match POS:
        case True : pos = "Да"
        case False : pos = "Нет"
    change_code = query_info.change_code
    date = query_info.date
    recomendation = query_info.recomendation
    message_text = f"Город: <b><u>{city_name}</u></b>\nЖК: <b><u>{commercial_name}</u></b>\nПроект: <b><u>{project_name}</u></b>\nТекстовый запрос: <b><u>{comment}</u></b>\nАльбом ПД: <b><u>{album}</u></b>\nСчитаю вопрос системным: <b><u>{syst_q}</u></b>\nСостояние работ на СМР по вопросу: <b><u>{state_of_works}</u></b>\nОжидаемый экономический эффект: <b><u>{economic_effect}</u></b>\nОжидаемое сокращение сроков СМР (дней): <b><u>{reduce_time}</u></b>\nТипология замечаний: <b><u>{type_of_note}</u></b>\nИзменения вносятся в ПОС: <b><u>{pos}</u></b>\nКод изменения: <b><u>{change_code}</u></b>\nДата: <b><u>{date}</u></b>\nРекомендация: <b><u>{recomendation}</u></b>"
    photo = query_info.photo
    if photo != None:
        photos = photo.split(",")
        photo_group = MediaGroupBuilder(caption=message_text)
        for ph in photos:
            photo_group.add_photo(ph)
        await bot.send_media_group(chat_id=callback.message.chat.id, media=photo_group.build())
        await callback.message.answer(text="Выберите действие:", reply_markup=await aqk.back_to_menu("archive_query"))
    else:
        await callback.message.edit_text(text=message_text, reply_markup=await aqk.back_to_menu("archive_query"))