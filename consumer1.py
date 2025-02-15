import json
import asyncio, logging
import datetime
import database.request as rq
from kafka import KafkaConsumer

consumer = KafkaConsumer('messages1',bootstrap_servers='localhost:9092',enable_auto_commit=False,auto_offset_reset='earliest',heartbeat_interval_ms=3000,max_poll_interval_ms=30000,session_timeout_ms=45000)

async def main():
    for message in consumer:
        data = json.loads(message.value)
        id = int(data['id'])
        entry = await rq.search_duplicate(id)
        if not entry:
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
            change_code = data['change_code']
            date = data['date']
            datatime_obj = datetime.datetime.strptime(date[:-7], "%Y-%m-%d %H:%M:%S")
            recomendation = data['recomendation']
            author = data['author']
            status = data['status']
            await rq.send_query_after(id, city_name, commercial_name, project_name, comment, album, system_quest, state_of_works, economic_effect, reduce_time, type_of_note, POS, photos, change_code, datatime_obj, recomendation, author, status)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        consumer.close()
        print('Бот выключен')