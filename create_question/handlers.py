import math
import asyncio
import random
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
from python_kafka.producer import send_in_kafka
create_question_router = Router()

class Temp(StatesGroup):
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
    
    
#Хэндлер для возвращения в меню
@create_question_router.callback_query(F.data == "cancel")
async def get_projects_info(callback: CallbackQuery, state:FSMContext):
    await state.clear()
    message_text = "Список функций⚙️:"
    await callback.message.edit_text(text=message_text, reply_markup=menu_keyboards.main_table())

#Хэндлер для выбора сценария работы программы
@create_question_router.callback_query(F.data == "create_query")
async def get_projects_info(callback: CallbackQuery, state:FSMContext):
    message_text = "Хотите отправить фото сейчас или потом?"
    await state.update_data(choise = None)
    await state.set_state(Temp.nothing)
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.first())
    

#Хэндлер с требованием выслать фотографии
@create_question_router.callback_query(F.data == "send_photo")
async def get_project_info(callback: CallbackQuery, state:FSMContext):
    message_text = "Отправьте нужные фотографии:"
    data = await state.get_data()
    try:
        choise = data['choise']
        if choise == 1:
            await callback.message.edit_text(text=message_text)
        else:
            await callback.message.edit_text(text=message_text, reply_markup=cqk.back_for_choise(cqk.SecondAnswer))
    except:
        await state.update_data(choise = 1)
        await callback.message.edit_text(text=message_text, reply_markup=await cqk.back("create_query"))
    await state.set_state(Temp.photos)


flag_group_id = []
#Хэндлер для обработки фотографий
@create_question_router.message(Temp.photos)
async def get_project_info(message: Message, state:FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
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
            await message.answer("Фотография получена.\nМожно отправить еще.", reply_markup=cqk.last_step_with_photo())#Если фотографии решили добавить в конце
    else:
        if flag_group_id.count(message.media_group_id) == 1:
            if(choise == 1):
                await message.answer("Фотографии получены.\nМожно отправить еще.", reply_markup=await cqk.second("chose_city"))
            else:
                await message.answer("Фотографии получены.\nМожно отправить еще.", reply_markup=cqk.last_step_with_photo())#Если фотографии решили добавить в конце


#Хэндлер для получения списка городов
@create_question_router.callback_query(F.data == "chose_city")
async def get_project_info(callback: CallbackQuery, state:FSMContext):
    button_data = await rq.get_cities()
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    message_text = f"Выберите город из списка ({1}/{int(pages)+1})"
    data = await state.get_data()
    try:
        choise = data['choise']
        await callback.message.edit_text(text=message_text, reply_markup=await cqk.city(0, "send_photo"))
    except:
        await callback.message.edit_text(text=message_text, reply_markup=await cqk.city1(0))
#Хэндлер для пролистывания списка городов
@create_question_router.callback_query(F.data.contains("citypage_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    message_text = f"Выберите город из списка ({int(page)+1}/{int(pages)+1})"
    data = await state.get_data()
    try:
        choise = data['choise']
        await callback.message.edit_text(text=message_text, reply_markup=await cqk.city(int(page), "send_photo"))
    except:
        await callback.message.edit_text(text=message_text, reply_markup=await cqk.city1(int(page)))


#Хэндлер для получения списка ЖК
@create_question_router.callback_query(F.data.contains("city_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    city = callback.data.split("_")[1]
    await state.update_data(city_name=city)
    data = await state.get_data()
    city = str(data['city_name'])
    button_data = await rq.get_comm(city)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    message_text = f"Вы выбрали {city}.\nВыберите ЖК из списка ({1}/{int(pages)+1})"
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.commercial_name(0, city, "chose_city"))
#Хэндлер для пролистывания списка ЖК
@create_question_router.callback_query(F.data.contains("commpage_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    city = str(data['city_name'])
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    message_text = f"Выберите ЖК из списка ({int(page)+1}/{int(pages)+1})"
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.commercial_name(int(page), city, "chose_city"))
    
    
#Хэндлер для получения списка проектов
@create_question_router.callback_query(F.data.contains("comm_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    comm = callback.data.split("_")[1]
    await state.update_data(commercial_name=comm)
    data = await state.get_data()
    comm = str(data['commercial_name'])
    button_data = await rq.get_projects(comm)
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    message_text = f"Вы выбрали {comm}.\nВыберите прокт из списка ({1}/{int(pages)+1})"
    await state.set_state(Temp.nothing)
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.project_name(0, comm, "commpage_0_0"))
#Хэндлер для пролистывания списка проектов
@create_question_router.callback_query(F.data.contains("projectpage_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    comm = str(data['commercial_name'])
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    message_text = f"Выберите прокт из списка ({int(page)+1}/{int(pages)+1})"
    await state.set_state(Temp.nothing)
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.project_name(int(page), comm, "commpage_0_0"))
    
    
#Хэндлер для получения комментария
@create_question_router.callback_query(F.data.contains("project_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    project = callback.data.split("_")[1]
    await state.update_data(project_name=project)
    message_text="Введите текстовый запрос:"
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.back(f"projectpage_0_0"))
    await state.set_state(Temp.comment)


#Хэндлер для получения альбома и обработки комментария
@create_question_router.message(Temp.comment)
async def get_project_info(message:Message, state:FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    project = data['project_name']
    button_data = await rq.get_albums()
    array_lenght = len(button_data)
    pages = math.ceil(array_lenght/int(PAGE_COUNT)) - 1
    message_text = f"Выберите альбом из списка ({1}/{int(pages)+1})"
    await message.answer(text=message_text, reply_markup=await cqk.third_step(0, f"project_{project}"))
#Хэндлер для пролистывания альбомов
@create_question_router.callback_query(F.data.contains("albumpage_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    project = data['project_name']
    page = callback.data.split("_")[1]
    pages = callback.data.split("_")[2]
    message_text = f"Выберите альбом из списка ({int(page)+1}/{int(pages)+1})"
    await state.set_state(Temp.album)
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.third_step(int(page), f"project_{project}"))


#Хэндлер для обработки альбома + является ли вопрос системным
@create_question_router.callback_query(F.data.contains("album_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    album = callback.data.split("_")[1]
    await state.update_data(album=album)
    message_text = "Вопрос являетя системным?"
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.choise("albumpage_0_0", "systq"))

# Обработчик формы да/нет + определите состояние СМР по вопросу
@create_question_router.callback_query(F.data.contains("systq_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    choise = callback.data.split("_")[1]
    await state.update_data(system_quest = choise)
    message_text = f"Определите состояние на СМР по вопросу:\n<b>1)</b>Проводится тендер.\n<b>2)</b>Производится расчет бюджета по стадии П.\n<b>3)</b>Работы на СМР планируются к выполнению в течении 2х недель.\n<b>4)</b>Работы на СМР планируются к выполнению в течении месяца.\n<b>5)</b>Работы на СМР выполняются на текущий момент.\n<b>6)</b>СМР выполнены.\n<b>7)</b>Я проектировщик."
    data = await state.get_data()
    album = data['album']
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.state_of_work(f"album_{album}"))

state_number = ''
#Хэндлер сохраняет состояние на СМР по вопросу и задает ожидаемый экономический эффект
@create_question_router.callback_query(F.data.contains("state_"))
async def get_project_info(callback: CallbackQuery, state: FSMContext):
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
    data = await state.get_data()
    system_quest = data['system_quest']
    message_text = "Введите ожидаемый экономический эффект\n(В рублях, целое или дробное):"
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.back(f"choise_{system_quest}"))


#Хэндлер сохраняет экономический эффект и устанавливает состояние для сокращения сроков СМР
@create_question_router.message(Temp.economic_effect)
async def get_project_info(message: Message, state: FSMContext):
    global state_number
    try:
        float_number = float(message.text)
        if float_number >= 0:
            await state.update_data(economic_effect=float_number)
            await state.set_state(Temp.reduce_time)
            message_text = "Введите ожидаемое сокращение сроков СМР (дней):"
            data = await state.get_data()
            state = data['state_of_works']
            await message.answer(text=message_text, reply_markup=await cqk.back(f"state_{state_number}"))
        else:
            await message.answer("Введенное вами значение некорректно.\nВеличина измеряется в <u>рублях</u>, принимается как целое, так и дробное значение <u>через точку</u>.")
    except ValueError:
        await message.answer("Введенное вами значение некорректно. Убедитесь, что вводимое вами значение - <u>число</u>.")
#Хэндлер дает возможность вернуться и ввести ожидаемое сокращение сроков СМР
@create_question_router.callback_query(F.data == "change_SMR")
async def get_project_info(callback: CallbackQuery, state: FSMContext):
    global state_number
    await state.set_state(Temp.reduce_time)
    message_text = "Введите ожидаемое сокращение сроков СМР (дней):"
    data = await state.get_data()
    state = data['state_of_works']
    await callback.message.answer(text=message_text, reply_markup=await cqk.back(f"state_{state_number}"))


#Хэндлер проверяет и сохраняет в FSM сокращение сроков и задает состояние для типологии замечаний
@create_question_router.message(Temp.reduce_time)
async def get_project_info(message: Message, state: FSMContext):
    input_message = message.text.isdigit()
    if input_message & input_message > 0:
        await state.update_data(reduce_time=message.text)
        await state.set_state(Temp.type_of_note)
        message_text = "Определите типологию замечаний:"
        await message.answer(text=message_text, reply_markup=await cqk.type("change_SMR"))
    else:
        await message.answer("Введенное вами значение некорректно. Убедитесь, что вводимое вами значение - <u>положительное целое число</u>.")
        return
@create_question_router.callback_query(F.data == "change_type")
async def get_project_info(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Temp.type_of_note)
    message_text = "Определите типологию замечаний:"
    await callback.message.answer(text=message_text, reply_markup=await cqk.type("change_SMR"))


#Хэндлер для сохранения типа замечания + устанавливает состояние для вопроса об изменениях в ПОС
@create_question_router.message(Temp.type_of_note)
async def get_project_info(message:Message, state:FSMContext):
    try:
        await state.update_data(type_of_note = message.text)
    except:
        await state.update_data(type_of_note = 0)
    message_text = "Изменения вносятся в ПОС?"
    await message.answer(text=message_text, reply_markup=await cqk.choise("change_type", "posq"))
@create_question_router.callback_query(F.data == "skip")
async def get_project_info(callback:CallbackQuery):
    message_text = "Изменения вносятся в ПОС?"
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.choise("change_type", "posq"))
@create_question_router.callback_query(F.data == "change_POS")
async def get_project_info(callback: CallbackQuery, state: FSMContext):
    message_text = "Изменения вносятся в ПОС?"
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.choise("change_type", "posq"))

#Хэндлер обработчик формы да/нет для изменений в ПОС
@create_question_router.callback_query(F.data.contains("posq_"))
async def get_project_info(callback:CallbackQuery, state:FSMContext):
    pos_answer = callback.data.split("_")[1]
    await state.update_data(POS = pos_answer)
    message_text = "Вопрос практически готов, осталось пару шагов."
    data = await state.get_data()
    try:
        choise = data['choise']
        if choise == 1:
            #Если пользователь прикрепил фото в начале.
            await callback.message.edit_text(text=message_text, reply_markup=await cqk.last_step_with_photo_without_file("change_POS"))
        elif choise == 2:
            await callback.message.edit_text(text=message_text, reply_markup=await cqk.last_step_without_photo("change_POS"))
        else:
            #Если пользователь нажал кнопку отправить фото и сразу вернулся.
            await callback.message.edit_text(text=message_text, reply_markup=await cqk.last_step_without_photo_without_file("change_POS"))
    except:
        #Если пользователь не прикрепил фото в начале.
        await state.update_data(choise=2)
        await callback.message.edit_text(text=message_text, reply_markup=await cqk.last_step_without_photo("change_POS"))


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
    choise = data['choise']
    files = data.get('files', [])
    files.append(file_info)
    await state.update_data(files=files)
    if choise == 1:
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
    message_text1 = "Внимательно просмотрите готовый вопрос и нажмите <u>Отправить</u>.\nЕсли что-то не так - нажмите кнопку <u>Меню</u> и начните заново."
    await callback.message.answer(text=message_text1, reply_markup=await cqk.end())


#Хэндлер для предложения прикрепить файл, при отсутствии фотографий
@create_question_router.callback_query(F.data == "end_without_photo")
async def get_project_info(callback:CallbackQuery):
    message_text = "Вопрос практически готов, осталось пару шагов."
    await callback.message.edit_text(text=message_text, reply_markup=await cqk.last_step_without_photo_without_file('hi'))


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
    await rq.send_query_before(id, city_name, commercial_name, project_name, comment, album, system_quest, state_of_works, economic_effect, reduce_time, typologia_zamechaniya, POS, send_photos, FIO)
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
    send_in_kafka(dummy_message=kafka_message)
    await callback.message.answer(text=message, reply_markup=await cqk.back_to_menu())