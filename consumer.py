import json
import asyncio, logging
from datetime import date
import random
import database.request as rq
from kafka import KafkaConsumer

consumer = KafkaConsumer('messages',bootstrap_servers='localhost:9092',auto_offset_reset='earliest')

async def main():
    for message in consumer:
        data = json.loads(message.value)
        id = int(data['id'])
        city_name = data['city_name']
        commercial_name = data['commercial_name']
        project_name = data['project_name']
        comment = data['comment']
        album = data['album']
        system_quest = bool(data['system_quest'])
        state_of_works = data['state_of_works']
        economic_effect = float(data['economic_effect'])
        reduce_time = int(data['reduce_time'])
        type_of_note = data['type_of_note']
        POS = data['POS']
        try:
            photos = data['photo']
        except:
            photos = None
        list = [0, 0.1, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2, 2.1, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10, 4.11, 4.12, 4.13, 4.14, 4.15, 5, 5.1, 5.2, 5.3, 6, 6.1, 7, 7.1, 8, 8.1]
        change_code = random.choice(list)
        # match change_code:
        #     case 0: change_comm = f"{}"
        #     case 0.1: change_comm = f"{}"
        #     case 1: change_comm = f"{}"
        #     case 1.1: change_comm = f"{}"
        #     case 1.2: change_comm = f"{}"
        #     case 1.3: change_comm = f"{}"
        #     case 1.4: change_comm = f"{}"
        #     case 1.5: change_comm = f"{}"
        #     case 1.6: change_comm = f"{}"
        #     case 2: change_comm = f"{}"
        #     case 2.1: change_comm = f"{}"
        #     case 3: change_comm = f"{}"
        #     case 3.1: change_comm = f"{}"
        #     case 3.2: change_comm = f"{}"
        #     case 3.3: change_comm = f"{}"
        #     case 3.4: change_comm = f"{}"
        #     case 3.5: change_comm = f"{}"
        #     case 4: change_comm = f"{}"
        #     case 4.1: change_comm = f"{}"
        #     case 4.2: change_comm = f"{}"
        #     case 4.3: change_comm = f"{}"
        #     case 4.4: change_comm = f"{}"
        #     case 4.5: change_comm = f"{}"
        #     case 4.6: change_comm = f"{}"
        #     case 4.7: change_comm = f"{}"
        #     case 4.8: change_comm = f"{}"
        #     case 4.9: change_comm = f"{}"
        #     case 4.10: change_comm = f"{}"
        #     case 4.11: change_comm = f"{}"
        #     case 4.12: change_comm = f"{}"
        #     case 4.13: change_comm = f"{}"
        #     case 4.14: change_comm = f"{}"
        #     case 4.15: change_comm = f"{}"
        #     case 5: change_comm = f"{}"
        #     case 5.1: change_comm = f"{}"
        #     case 5.2: change_comm = f"{}"
        #     case 5.3: change_comm = f"{}"
        #     case 6: change_comm = f"{}"
        #     case 6.1: change_comm = f"{}"
        #     case 7: change_comm = f"{}"
        #     case 7.1: change_comm = f"{}"
        #     case 8: change_comm = f"{}"
        #     case 8.1: change_comm = f"{}"
        set_date = date.today()
        recomendation = 'Рекомендую, замечательно.'
        author = data['author']
        entry = await rq.search_duplicate(id)
        if not entry:
            await rq.send_query_after(id, city_name, commercial_name, project_name, comment, album, system_quest, state_of_works, economic_effect, reduce_time, type_of_note, POS, photos, change_code, set_date, recomendation, author)
        
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Получатель выключен')