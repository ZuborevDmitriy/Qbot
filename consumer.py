import json
import asyncio, logging
from datetime import date
import random
import database.request as rq
from kafka import KafkaConsumer
from datetime import datetime
from python_kafka.producer import send_in_kafka1

consumer = KafkaConsumer('messages0',bootstrap_servers='localhost:9092',auto_offset_reset='earliest')

async def main():
    for message in consumer:
        data = json.loads(message.value)
        id = data['id']
        city_name = data['city_name']
        commercial_name = data['commercial_name']
        project_name = data['project_name']
        comment = data['comment']
        album = data['album']
        system_quest = data['system_quest']
        state_of_works = data['state_of_works']
        economic_effect = data['economic_effect']
        reduce_time = data['reduce_time']
        type_of_note = data['type_of_note']
        POS = data['POS']
        photos = data['photo']
        list = [0, 0.1, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2, 2.1, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10, 4.11, 4.12, 4.13, 4.14, 4.15, 5, 5.1, 5.2, 5.3, 6, 6.1, 7, 7.1, 8, 8.1]
        change_code = random.choice(list)
        set_date = str(datetime.now())
        recomendation = 'Рекомендую, замечательно.'
        author = data['author']
        kafka_message = {
            'id':id,
            'city_name':city_name,
            'commercial_name':commercial_name,
            'project_name':project_name,
            'comment':comment,
            'album':album,
            'system_quest':system_quest,
            'state_of_works':state_of_works,
            'economic_effect':economic_effect,
            'reduce_time':reduce_time,
            'type_of_note':type_of_note,
            'POS':POS,
            'photo': photos,
            'author':author,
            'change_code':change_code,
            'date':set_date,
            'recomendation':recomendation,
            'status':'created'
        }
        send_in_kafka1(dummy_message=kafka_message)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Получатель выключен')