import array
import math
import asyncio
import random
from aiogram.methods.delete_message import DeleteMessage
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import create_question.keyboards as cqk
import database.request as rq
from config.config import PAGE_COUNT
from aiogram.utils.media_group import MediaGroupBuilder
import menu.keyboards as menu_keyboards
from python_kafka.producer import send_in_kafka0
import emoji

create_question_router = Router()

class Temp(StatesGroup):
    messages_id = State()
    nothing = State()
    choise = State()
    city_name = State()
    commercial_name = State()
    project_name = State()
    comment = State()
    album = State()
    system_quest = State()
    state_of_works = State()
    economic_effect = State()
    reduce_time = State()
    type_of_note = State()
    POS = State()
    photos = State()
    files = State()
    change_number = State()
    change = State()
    
    
get_chat_id: int
get_message_id = array.array('i', [])
#Хэндлер для выбора сценария работы программы
@create_question_router.message(F.text == f"Создать вопрос {emoji.emojize(':pencil:')}")
async def get_projects_info(message: Message, state:FSMContext):
    global get_message_id
    get_message_id.clear()
    await state.clear()
    data = await state.get_data()
    message0 = await message.reply(text="Создаю вопрос...", reply_markup=await cqk.cancel_for_reply())
    message1 = await message.answer(text="Хотите отправить фото сейчас или потом?", reply_markup=await cqk.step_photo())
    await state.update_data(choise = None)
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)
    await state.set_state(Temp.nothing)




#Хэндлер для возвращения в меню
@create_question_router.callback_query(F.data == "cancel")
async def get_projects_info(callback: CallbackQuery, state:FSMContext):
    await state.clear()
    await callback.message.edit_text(text="Меню", reply_markup=menu_keyboards.main_table())
    
    
    
#Хэндлер для возвращения в меню для reply
@create_question_router.message(F.text == "Отмена")
async def get_projects_info(message: Message, bot:Bot, state:FSMContext):
    await state.set_state(Temp.nothing)
    data = await state.get_data()
    get_chat_id = message.chat.id
    for i in range(len(data.get('messages_id'))):
        if(data.get('messages_id')[i] != data.get('messages_id')[i-1]):
            print(data.get('messages_id')[i])
    for i in range(len(data.get('messages_id'))):
        if(data.get('messages_id')[i] != data.get('messages_id')[i-1]):
            await bot(DeleteMessage(chat_id=get_chat_id, message_id=data.get('messages_id')[i]))
    await message.answer(text="Меню", reply_markup=menu_keyboards.main_table())
    
    
    
#Хэндлер для получения списка городов
@create_question_router.callback_query(F.data == "chose_city")
async def get_project_info(callback: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    button_data = await rq.get_cities()
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    if(data.get('choise')!=None):
        message=await callback.message.edit_text(text=f"Выберите город из списка:\n(страница {1} из {int(pages)+1})", reply_markup=await cqk.city(0, "send_photo"))
    else:
        message=await callback.message.edit_text(text=f"Выберите город из списка:\n(страница {1} из {int(pages)+1})", reply_markup=await cqk.city1(0))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message.message_id])
    await state.update_data(messages_id = list_messages)
    
    
    
#Хэндлер для пролистывания списка городов
@create_question_router.callback_query(F.data.contains("citypage_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    if(data.get('choise')!=None):
        message=await callback.message.edit_text(text=f"Выберите город из списка:\n(страница {int(page)+1} из {int(pages)+1})", reply_markup=await cqk.city(int(page), "send_photo"))
    else:
        message=await callback.message.edit_text(text=f"Выберите город из списка:\n(страница {int(page)+1} из {int(pages)+1})", reply_markup=await cqk.city1(int(page)))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message.message_id])
    await state.update_data(messages_id = list_messages)   
        
        
#Хэндлер с требованием выслать фотографии
@create_question_router.callback_query(F.data == "send_photo")
async def get_project_info(callback: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    choise = data.get('choise')
    if(choise==None):
        await state.update_data(choise=1)
        message=await callback.message.edit_text(text="Отправьте нужные фотографии:")
    if(choise==1):
        message=await callback.message.edit_text(text="Отправьте нужные фотографии:")
    if(choise==2):
        message=await callback.message.edit_text(text="Отправьте нужные фотографии:")
    await state.set_state(Temp.photos)
    list_messages = data.get('messages_id', [])
    list_messages.extend([message.message_id])
    await state.update_data(messages_id = list_messages) 
    
    
flag_group_id = []
#Хэндлер для обработки фотографий
@create_question_router.message(Temp.photos)
async def get_project_info(message: Message, state:FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id
    choise = data['choise']
    photos = data.get('photos', [])
    photos.append(photo_id)
    global flag_group_id
    flag_group_id.append(message.media_group_id)
    await state.update_data(photos=photos)
    if not message.media_group_id:
        if(choise == 1):
            await message.answer("Фотография получена.\nМожно отправить еще.", reply_markup=await cqk.second("chose_city"))
        else:
            await message.answer("Фотография получена.\nМожно отправить еще.", reply_markup=await cqk.last_step_with_photo_without_file("end_without_photo"))#Если фотографии решили добавить в конце
    else:
        if flag_group_id.count(message.media_group_id) == 1:
            if(choise == 1):
                await message.answer("Фотографии получены.\nМожно отправить еще.", reply_markup=await cqk.second("chose_city"))
            else:
                await message.answer("Фотографии получены.\nМожно отправить еще.", reply_markup=await cqk.last_step_with_photo_without_file("end_without_photo"))#Если фотографии решили добавить в конце
                
                
                
#Хэндлер для получения списка ЖК
@create_question_router.callback_query(F.data.contains("city_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    city = callback.data.split("_")[1]
    await state.update_data(city_name=city)
    message0 = await callback.message.edit_text(text=f"Вы выбрали город - <u>{city}.</u>")
    button_data = await rq.get_comm(city)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    message1 = await callback.message.answer(text=f"Выберите ЖК из списка:\n(страница {1} из {int(pages)+1})", reply_markup=await cqk.commercial_name(0, city, "chose_city"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages) 
    
    
    
#Хэндлер для пролистывания списка ЖК
@create_question_router.callback_query(F.data.contains("commpage_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    city = str(data['city_name'])
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    message = await callback.message.edit_text(text=f"Выберите ЖК из списка:\n(страница {int(page)+1} из {int(pages)+1})", reply_markup=await cqk.commercial_name(int(page), city, "chose_city"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message.message_id])
    await state.update_data(messages_id = list_messages) 
    
    
    
#Хэндлер для получения списка проектов
@create_question_router.callback_query(F.data.contains("comm_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    comm = callback.data.split("_")[1]
    await state.update_data(commercial_name=comm)
    message0 = await callback.message.edit_text(text=f"Вы выбрали ЖК - <u>{comm}</u>.")
    button_data = await rq.get_projects(comm)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    await state.set_state(Temp.nothing)
    message1 = await callback.message.answer(text=f"Выберите проект из списка:\n(страница {1} из {int(pages)+1})", reply_markup=await cqk.project_name(0, comm, "commpage_0_0"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)   
    
    
    
#Хэндлер для пролистывания списка проектов
@create_question_router.callback_query(F.data.contains("projectpage_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    comm = str(data['commercial_name'])
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    await state.set_state(Temp.nothing)
    message = await callback.message.edit_text(text=f"Выберите проект из списка:\n(страница {int(page)+1} из {int(pages)+1})", reply_markup=await cqk.project_name(int(page), comm, "commpage_0_0"))
    list_messages = data.get('messages_id', [])
    list_messages.append([message.message_id])
    await state.update_data(messages_id = list_messages)
    
#Хэндлер для получения комментария
@create_question_router.callback_query(F.data.contains("project_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    project = callback.data.split("_")[1]
    await state.update_data(project_name=project)
    global get_chat_id
    global get_message_id
    message0 = await callback.message.edit_text(text=f"Вы выбрали проект - <u>{project}</u>.")
    message1 = await callback.message.answer(text=f"Введите текстовый запрос:", reply_markup=await cqk.back(f"projectpage_0_0"))
    get_chat_id = callback.message.chat.id
    get_message_id.append(message1.message_id)
    await state.set_state(Temp.comment)
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)



#Хэндлер для получения альбома и обработки комментария
@create_question_router.message(Temp.comment)
async def get_project_info(message:Message, bot:Bot, state:FSMContext):
    data = await state.get_data()
    global get_chat_id
    global get_message_id
    await state.update_data(comment=message.text)
    message0 = await message.answer(text=f"Текстовый комментарий - <u>{message.text}</u>.")
    project = data.get('project_name')
    button_data = await rq.get_albums()
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    message1 = await message.answer(text=f"Выберите альбом из списка\n(страница {1} из {int(pages)+1})", reply_markup=await cqk.third_step(0, f"project_{project}"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)
    for i in get_message_id:
        await bot(DeleteMessage(chat_id=get_chat_id, message_id=i))
        
        
        
        

#Хэндлер для пролистывания альбомов
@create_question_router.callback_query(F.data.contains("albumpage_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    project = data['project_name']
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    await state.set_state(Temp.album)
    message0 = await callback.message.edit_text(text=f"Вы выбрали проект - <u>{project}</u>.")
    message1 = await callback.message.answer(text=f"Выберите альбом из списка\n(страница {int(page)+1} из {int(pages)+1})", reply_markup=await cqk.third_step(int(page), f"project_{project}"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)


#Хэндлер для обработки альбома + является ли вопрос системным
@create_question_router.callback_query(F.data.contains("album_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    album = callback.data.split("_")[1]
    await state.update_data(album=album)
    message0 = await callback.message.edit_text(text=f"Вы выбрали альбом - <u>{album}</u>.")
    message1 = await callback.message.answer(text="Вопрос являетя системным?", reply_markup=await cqk.choise("albumpage_0_0", "systq"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)


# Обработчик формы да/нет + определите состояние СМР по вопросу
@create_question_router.callback_query(F.data.contains("systq_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    choise = callback.data.split("_")[1]
    await state.update_data(system_quest = choise)
    if choise:
        choise = "Да"
    else:
        choise = "Нет"
    album = data.get('album')
    message0 = await callback.message.edit_text(text=f"Вопрос является системным - <u>{choise}</u>.")
    message1 = await callback.message.answer(text=f"Определите состояние на СМР по вопросу:\n<b>1)</b>Проводится тендер.\n<b>2)</b>Производится расчет бюджета по стадии П.\n<b>3)</b>Работы на СМР планируются к выполнению в течении 2х недель.\n<b>4)</b>Работы на СМР планируются к выполнению в течении месяца.\n<b>5)</b>Работы на СМР выполняются на текущий момент.\n<b>6)</b>СМР выполнены.\n<b>7)</b>Я проектировщик.", reply_markup=await cqk.state_of_work(f"album_{album}"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)


state_number = ''
#Хэндлер сохраняет состояние на СМР по вопросу и задает ожидаемый экономический эффект
@create_question_router.callback_query(F.data.contains("state_"))
async def get_project_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    state_info = callback.data.split("_")[1]
    global state_number
    state_number = state_info
    match state_info:
            case "1": state_result = "Проводится тендер."
            case "2": state_result = "Производится расчет бюджета по стадии П."
            case "3": state_result = "Работы на СМР планируются к выполнению в течении 2х недель."
            case "4": state_result = "Работы на СМР планируются к выполнению в течении месяца."
            case "5": state_result = "Работы на СМР выполняются на текущий момент."
            case "6": state_result = "СМР выполнены."
            case "7": state_result = "Я проектировщик."
    await state.update_data(state_of_works=state_result)
    await state.set_state(Temp.economic_effect)
    system_quest = data.get('system_quest')
    message0 = await callback.message.edit_text(text=f"СМР по вопросу - \n<u>{state_result}</u>.")
    message1 = await callback.message.answer(text="Введите ожидаемый экономический эффект\n(В рублях, целое или дробное):", reply_markup=await cqk.back(f"systq_{system_quest}"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)
    global get_message_id
    get_message_id.clear()
    get_message_id.append(message1.message_id)

#Хэндлер сохраняет экономический эффект и устанавливает состояние для сокращения сроков СМР
@create_question_router.message(Temp.economic_effect)
async def get_project_info(message: Message, bot:Bot, state: FSMContext):
    data = await state.get_data()
    list_messages = data.get('messages_id', [])
    global state_number
    global get_chat_id
    global get_message_id
    try:
        if(float(message.text)>0):
            message0 = await message.answer(text=f"Экономический эффект - <u>{message.text}</u>.")
            await state.update_data(economic_effect=float(message.text))
            list_messages.append(message0.message_id)
            await state.set_state(Temp.reduce_time)
            message1 = await message.answer(text="Введите ожидаемое сокращение сроков СМР (дней):", reply_markup=await cqk.back(f"state_{state_number}"))
            get_message_id.append(message1.message_id)
            for i in get_message_id[0:len(get_message_id)-1]:
                await bot(DeleteMessage(chat_id=get_chat_id, message_id=i))
        else:
            message2 = await message.answer(text="Значение должно быть <u>больше нуля</u>.")
            get_message_id.append(message2.message_id)
            return
    except:
        message3 = await message.answer(text="Введенное вами значение некорректно.\nВеличина измеряется в <u>рублях</u>, принимается как целое, так и дробное значение <u>через точку</u>.")
        get_message_id.append(message3.message_id)
        return
    await state.update_data(messages_id = list_messages)
        
# #Хэндлер дает возможность вернуться и ввести ожидаемое сокращение сроков СМР
# @create_question_router.callback_query(F.data == "change_SMR")
# async def get_project_info(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     global state_number
#     await state.set_state(Temp.reduce_time)
#     state = data.get('state_of_works')
#     message = await callback.message.answer(text="Введите ожидаемое сокращение сроков СМР (дней):", reply_markup=await cqk.back(f"state_{state_number}"))


#Хэндлер проверяет и сохраняет в FSM сокращение сроков и задает состояние для типологии замечаний
@create_question_router.message(Temp.reduce_time)
async def get_project_info(message: Message, bot:Bot, state: FSMContext):
    data = await state.get_data()
    list_messages = data.get('messages_id', [])
    global get_chat_id
    global get_message_id
    await bot(DeleteMessage(chat_id=get_chat_id, message_id=get_message_id[1]))
    input_message = message.text.isdigit()
    if input_message & input_message > 0:
        await state.update_data(reduce_time=message.text)
        await state.set_state(Temp.type_of_note)
        message0 = await message.answer(text=f"Ожидаемое сокращение сроков - <u>{message.text}</u>.")
        message1 = await message.answer(text="Определите типологию замечаний:", reply_markup=await cqk.type("change_SMR"))
        list_messages.extend([message0.message_id, message1.message_id])
    else:
        message2 = await message.answer("Введенное вами значение некорректно. Убедитесь, что вводимое вами значение - <u>положительное целое число</u>.")
        list_messages.append([message2.message_id])
        return
    await state.update_data(messages_id = list_messages)
    get_message_id.clear()
    
    
    
@create_question_router.callback_query(F.data == "change_type")
async def get_project_info(callback: CallbackQuery, state: FSMContext):
    global get_chat_id
    global get_message_id
    data = await state.get_data()
    await state.set_state(Temp.type_of_note)
    message = await callback.message.answer(text="Определите типологию замечаний:", reply_markup=await cqk.type("change_SMR"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message.message_id])
    await state.update_data(messages_id = list_messages)
    get_message_id.append(message.message_id)


#Хэндлер для сохранения типа замечания + устанавливает состояние для вопроса об изменениях в ПОС
@create_question_router.message(Temp.type_of_note)
async def get_project_info(message:Message, state:FSMContext):
    data = await state.get_data()
    message0 = await message.answer(text=f"Типология замечаний - {message.text}")
    try:
        await state.update_data(type_of_note = message.text)
    except:
        await state.update_data(type_of_note = 0)
    message1 = await message.answer(text="Изменения вносятся в ПОС?", reply_markup=await cqk.choise("change_type", "posq"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message0.message_id, message1.message_id])
    await state.update_data(messages_id = list_messages)



@create_question_router.callback_query(F.data == "skip")
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    message = await callback.message.edit_text(text="Изменения вносятся в ПОС?", reply_markup=await cqk.choise("change_type", "posq"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message.message_id])
    await state.update_data(messages_id = list_messages)




@create_question_router.callback_query(F.data == "change_POS")
async def get_project_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = await callback.message.edit_text(text="Изменения вносятся в ПОС?", reply_markup=await cqk.choise("change_type", "posq"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message.message_id])
    await state.update_data(messages_id = list_messages)


#Хэндлер обработчик формы да/нет для изменений в ПОС
@create_question_router.callback_query(F.data.contains("posq_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    pos_answer = callback.data.split("_")[1]
    await state.update_data(POS = pos_answer)
    choise = data.get('choise')
    if choise == 1:
    #Если пользователь прикрепил фото в начале.
        message = await callback.message.edit_text(text="Вопрос практически готов, осталось пару шагов.", reply_markup=await cqk.last_step_with_photo_without_file("change_POS"))
    elif choise == None:
        await state.update_data(choise=2)
        message = await callback.message.edit_text(text="Вопрос практически готов, осталось пару шагов.", reply_markup=await cqk.last_step_without_photo("change_POS"))
    else:
        #Если пользователь нажал кнопку отправить фото и сразу вернулся.
        await callback.message.edit_text(text="Вопрос практически готов, осталось пару шагов777.", reply_markup=await cqk.last_step_without_photo_without_file("change_POS"))
        #Если пользователь не прикрепил фото в начале.
        await state.update_data(choise=2)
        await callback.message.edit_text(text="Вопрос практически готов, осталось пару шагов666.", reply_markup=await cqk.last_step_without_photo("change_POS"))
    list_messages = data.get('messages_id', [])
    list_messages.extend([message.message_id])
    await state.update_data(messages_id = list_messages)


#Хэндлер для прикрепления файла.
@create_question_router.callback_query(F.data == "add_file")
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    message_text = "Отправьте файл"
    await callback.message.edit_text(text=message_text)
    await state.set_state(Temp.files)




@create_question_router.message(Temp.files)
async def get_project_info(message:Message, state:FSMContext):
    file_info = f"{message.document.file_name}_{message.document.file_id}"
    data = await state.get_data()
    photos = data['photos']
    files = data.get('files', [])
    files.append(file_info)
    await state.update_data(files=files)
    if photos != None:
        await message.answer("Файл получен.\nМожно отправить еще.", reply_markup=await cqk.last_step_with_photo_with_file('hi'))
    else:
        await message.answer("Файл получен.\nМожно отправить еще.", reply_markup=await cqk.last_step_without_photo_with_file('hi'))



#Хэндлер для вывода конечного сообщения со всеми результатами.
@create_question_router.callback_query(F.data == "conclude")
async def get_project_info(callback:CallbackQuery, bot:Bot, state:FSMContext):
    data = await state.get_data()
    city_name = data['city_name']
    commercial_name = data['commercial_name']
    project_name = data['project_name']
    comment = data['comment']
    album = data['album']
    system_quest = data['system_quest']
    syst_q = ""
    match system_quest:
        case 'true' : syst_q = "Да"
        case 'false' : syst_q = "Нет"
    state_of_works = data['state_of_works']
    economic_effect = data['economic_effect']
    reduce_time = data['reduce_time']
    try:
        type_of_note = data['type_of_note']
        typologia_zamechaniya = type_of_note
    except:
        typologia_zamechaniya = "Не указано"
    POS = data['POS']
    pos = ""
    match POS:
        case 'true' : pos = "Да"
        case 'false' : pos = "Нет"
    photos = data['photos']
    try:
        files = data['files']
        files_title = []
        for files_name in files:
            files_title.append(files_name.split('_')[0])
        message_text = f"Город: <b><u>{city_name}</u></b>\nЖК: <b><u>{commercial_name}</u></b>\nПроект: <b><u>{project_name}</u></b>\nТекстовый запрос: <b><u>{comment}</u></b>\nАльбом ПД: <b><u>{album}</u></b>\nСчитаю вопрос системным: <b><u>{syst_q}</u></b>\nСостояние работ на СМР по вопросу: <b><u>{state_of_works}</u></b>\nОжидаемый экономический эффект: <b><u>{economic_effect}</u></b>\nОжидаемое сокращение сроков СМР (дней): <b><u>{reduce_time}</u></b>\nТипология замечаний: <b><u>{typologia_zamechaniya}</u></b>\nИзменения вносятся в ПОС: <b><u>{pos}</u></b>\nСохраненные файлы:\n<b><u>{';\n'.join(files_title)}</u></b>"
    except:
        message_text = f"Город: <b><u>{city_name}</u></b>\nЖК: <b><u>{commercial_name}</u></b>\nПроект: <b><u>{project_name}</u></b>\nТекстовый запрос: <b><u>{comment}</u></b>\nАльбом ПД: <b><u>{album}</u></b>\nСчитаю вопрос системным: <b><u>{syst_q}</u></b>\nСостояние работ на СМР по вопросу: <b><u>{state_of_works}</u></b>\nОжидаемый экономический эффект: <b><u>{economic_effect}</u></b>\nОжидаемое сокращение сроков СМР (дней): <b><u>{reduce_time}</u></b>\nТипология замечаний: <b><u>{typologia_zamechaniya}</u></b>\nИзменения вносятся в ПОС: <b><u>{pos}</u></b>"
    photo_group = MediaGroupBuilder(caption=message_text)
    for photo in photos:
        photo_group.add_photo(photo)
    await bot.send_media_group(chat_id=callback.message.chat.id, media=photo_group.build())
    message_text1 = "Внимательно просмотрите готовый вопрос и нажмите <u>Отправить</u>.\nЕсли что-то не так - нажмите кнопку <u>отмена</u> и начните заново."
    await callback.message.answer(text=message_text1, reply_markup=await cqk.end())



#Хэндлер для предложения прикрепить файл, при отсутствии фотографий
@create_question_router.callback_query(F.data == "end_without_photo")
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    message_text = "Вопрос практически готов, осталось пару шагов."
    data = await state.get_data()
    POS = data['POS']
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.last_step_without_photo_without_file(f'posq_{POS}'))



#Хэндлер для вывода конечного сообщения со всеми результатами без фотографий.
@create_question_router.callback_query(F.data == "conclude_without")
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    city_name = data['city_name']
    commercial_name = data['commercial_name']
    project_name = data['project_name']
    comment = data['comment']
    album = data['album']
    system_quest = data['system_quest']
    syst_q = ""
    match system_quest:
        case 'true' : syst_q = "Да"
        case 'false' : syst_q = "Нет"
    state_of_works = data['state_of_works']
    economic_effect = data['economic_effect']
    reduce_time = data['reduce_time']
    try:
        type_of_note = data['type_of_note']
        typologia_zamechaniya = type_of_note
    except:
        typologia_zamechaniya = "Не указано"
    POS = data['POS']
    pos = ""
    match POS:
        case 'true' : pos = "Да"
        case 'false' : pos = "Нет"
    try:
        files = data['files']
        files_title = []
        for files_name in files:
            files_title.append(files_name.split('_')[0])
        message_text = f"Город: <b><u>{city_name}</u></b>\nЖК: <b><u>{commercial_name}</u></b>\nПроект: <b><u>{project_name}</u></b>\nТекстовый запрос: <b><u>{comment}</u></b>\nАльбом ПД: <b><u>{album}</u></b>\nСчитаю вопрос системным: <b><u>{syst_q}</u></b>\nСостояние работ на СМР по вопросу: <b><u>{state_of_works}</u></b>\nОжидаемый экономический эффект: <b><u>{economic_effect}</u></b>\nОжидаемое сокращение сроков СМР (дней): <b><u>{reduce_time}</u></b>\nТипология замечаний: <b><u>{typologia_zamechaniya}</u></b>\nИзменения вносятся в ПОС: <b><u>{pos}</u></b>\nСохраненные файлы:\n<b><u>{';\n'.join(files_title)}</u></b>"
    except:
        message_text = f"Город: <b><u>{city_name}</u></b>\nЖК: <b><u>{commercial_name}</u></b>\nПроект: <b><u>{project_name}</u></b>\nТекстовый запрос: <b><u>{comment}</u></b>\nАльбом ПД: <b><u>{album}</u></b>\nСчитаю вопрос системным: <b><u>{syst_q}</u></b>\nСостояние работ на СМР по вопросу: <b><u>{state_of_works}</u></b>\nОжидаемый экономический эффект: <b><u>{economic_effect}</u></b>\nОжидаемое сокращение сроков СМР (дней): <b><u>{reduce_time}</u></b>\nТипология замечаний: <b><u>{typologia_zamechaniya}</u></b>\nИзменения вносятся в ПОС: <b><u>{pos}</u></b>"
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.end())



@create_question_router.callback_query(F.data == "change_line")
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    message_text = "Выберите номер строки, которую хотите изменить:\n1)Текстовый запрос;\n2)Ожидаемый экономический эффект;\n3)Ожидаемие сокращение сроков СМР;\n4)Типология замечаний."
    await callback.message.answer(text=message_text, reply_markup=await cqk.change_line())



@create_question_router.callback_query(F.data.contains('change_'))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    change_info = callback.data.split("_")[1]
    await state.update_data(change_number = change_info)
    await state.set_state(Temp.change)
    message_text = "Введите нужное значение:"
    await callback.message.answer(text=message_text)



@create_question_router.message(Temp.change)
async def get_project_info(message: Message, state: FSMContext):
    data = await state.get_data()
    line_number = data['change_number']
    choise = data['choise']
    match line_number:
        case "1": await state.update_data(comment = message.text)
        case "2":
            try:
                float_number = float(message.text)
                if float_number >= 0:
                    await state.update_data(economic_effect=float_number)
                else:
                    await message.answer("Введенное вами значение некорректно.\nВеличина измеряется в <u>рублях</u>, принимается как целое, так и дробное значение <u>через точку</u>.")
            except ValueError:
                await message.answer("Введенное вами значение некорректно.\nВеличина измеряется в <u>рублях</u>, принимается как целое, так и дробное значение <u>через точку</u>.")
        case "3":
            input_message = message.text.isdigit()
            if input_message & input_message > 0:
                await state.update_data(reduce_time=message.text)
            else:
                await message.answer("Введенное вами значение некорректно. Убедитесь, что вводимое вами значение - <u>положительное целое число</u>.")
                return
        case "4": await state.update_data(type_of_note = message.text)
    message_text = "Изменения приняты"
    if choise == 1:
        await message.answer(text=message_text, reply_markup=await cqk.last_step_with_photo_with_file(f"change_{line_number}"))
    else:
        await message.answer(text=message_text, reply_markup=await cqk.last_step_without_photo_with_file(f"change_{line_number}"))



@create_question_router.callback_query(F.data == "send")
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    user_id = callback.from_user.id
    FIO = await rq.get_FIO(user_id)
    data = await state.get_data()
    city_name = data['city_name']
    commercial_name = data['commercial_name']
    project_name = data['project_name']
    comment = data['comment']
    album = data['album']
    system_quest = data['system_quest']
    state_of_works = data['state_of_works']
    economic_effect = data['economic_effect']
    reduce_time = data['reduce_time']
    id = int(economic_effect)+int(reduce_time)+int(user_id)+int(random.randint(0,100))
    try:
        type_of_note = data['type_of_note']
        typologia_zamechaniya = type_of_note
    except:
        typologia_zamechaniya = None
    POS = data['POS']
    try:
        photos = data['photos']
        send_photos = f'{','.join(photos)}'
    except:
        send_photos = None
    message = "Ваш вопрос успешно отправлен на рассмотрение"
    kafka_message = {
        'id':id,
        'city_name':city_name,
        'commercial_name':commercial_name,
        'project_name':project_name,
        'comment':comment,
        'album':album,
        'system_quest':bool(system_quest),
        'state_of_works':state_of_works,
        'economic_effect':float(economic_effect),
        'reduce_time':int(reduce_time),
        'type_of_note':typologia_zamechaniya,
        'POS':bool(POS),
        'photo': send_photos,
        'author':FIO
    }
    send_in_kafka0(dummy_message=kafka_message)
    await callback.message.answer(text=message, reply_markup=await cqk.back_to_menu())