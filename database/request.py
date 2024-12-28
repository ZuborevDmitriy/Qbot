from database.models import async_session
from database.models import User, Project, Album, Query_b, Query_a
from sqlalchemy import select, update
            
#Проверка пользователя на регистрацию
async def check_users(phnumb):
    async with async_session() as session:
        authorized_user = await session.scalar(select(User).where((User.phone_number==phnumb) & (User.is_authorized == True)))
        non_authorized_user = await session.scalar(select(User).where(User.phone_number==phnumb))
        await session.close()
        if authorized_user:
            return "1"
        elif non_authorized_user:
            return "2"
        else:
            return "3"
        
#Регистрация пользователя
async def reg_user(tgid, phnumb, usrinfo):
    async with async_session() as session:
        await session.execute(update(User).where(User.phone_number==phnumb).values(tg_id=tgid, user_info=usrinfo, is_authorized=True))
        await session.commit()
        await session.close()
        
#Список городов
async def get_cities():
    async with async_session() as session:
        cities = await session.execute(select(Project.city).distinct())
        cities = cities.scalars().all()
        await session.close()
    return cities

#Список жк
async def get_comm(city: str):
    async with async_session() as session:
        comm_name = await session.execute(select(Project.name).where(Project.city==city))
        comm_name = comm_name.scalars().all()
        await session.close()
    return comm_name

#Список проектов
async def get_projects(comm: str):
    async with async_session() as session:
        projects = await session.execute(select(Project.project).where(Project.name==comm))
        projects = projects.scalars().all()
        await session.close()
    return projects

#Список альбомов
async def get_albums():
    async with async_session() as session:
        albums = await session.execute(select(Album))
        albums = albums.scalars().all()
        await session.close()
    return albums

#Получения ФИО пользователя
async def get_FIO(user_tg_id):
    async with async_session() as session:
        FIO = await session.scalar(select(User.user_info).where(User.tg_id==user_tg_id))
        await session.close()
    return FIO

#Отправление данных о вопросе в БД до отправки в kafka
async def send_query_before(make_id, cityname, commname, prname, comm, album, systquest, stateofworks, econeff, reducetime, typeofnote, POS, photos, author):
    async with async_session() as session:
        query = Query_b(
        id = make_id,
        city_name = cityname,
        commercial_name = commname,
        project_name = prname,
        comment = comm,
        album = album,
        system_quest = bool(systquest),
        state_of_works = stateofworks,
        economic_effect = float(econeff),
        reduce_time = int(reducetime),
        type_of_note = typeofnote,
        POS = bool(POS),
        photo = photos,
        author = author
        )
        session.add(query)
        await session.commit()
        await session.close()

#Отправление данных о вопросе в БД после отправки в kafka
async def send_query_after(make_id, cityname, commname, prname, comm, album, systquest, stateofworks, econeff, reducetime, typeofnote, POS, photos, changecode, date, recomend, author):
    async with async_session() as session:
        query = Query_a(
        id = make_id,
        city_name = cityname,
        commercial_name = commname,
        project_name = prname,
        comment = comm,
        album = album,
        system_quest = bool(systquest),
        state_of_works = stateofworks,
        economic_effect = float(econeff),
        reduce_time = int(reducetime),
        type_of_note = typeofnote,
        POS = bool(POS),
        photo = photos,
        change_code = int(changecode),
        date = date,
        recomendation = recomend,
        author = author
        )
        session.add(query)
        await session.commit()
        await session.close()
        
#Поиск уже имеющихся записей
async def search_duplicate(id):
    async with async_session() as session:
        entry = await session.execute(select(Query_a).where(Query_a.id==id))
        entry = entry.scalars().first()
        await session.close()
    return entry

#Получение списка активных вопросов пользователя
async def get_queries(user):
    async with async_session() as session:
        queries = await session.execute(select(Query_a.id).where(Query_a.author==user))
        queries = queries.scalars().all()
        await session.close()
    return queries

#Получение информации о выбранном вопросе
async def get_query(id):
    async with async_session() as session:
        query = await session.execute(select(Query_a).where(Query_a.id==id))
        query = query.scalars().first()
        await session.close()
    return query