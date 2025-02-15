import json
import asyncio, logging
import datetime
import database.request as rq
from kafka import KafkaConsumer

consumer = KafkaConsumer('updmess',bootstrap_servers='localhost:9092',enable_auto_commit=False,auto_offset_reset='earliest',heartbeat_interval_ms=3000,max_poll_interval_ms=30000,session_timeout_ms=45000)

async def main():
    for message in consumer:
        data = json.loads(message.value)
        id = int(data['id'])
        date = data['devdate']
        date = datetime.datetime.strptime(date[:-7], '%Y-%m-%d %H:%M:%S')
        check = await rq.research_query(id, date)
        try:
            status = data['status']
            if check:
                await rq.upd_dev_query(id, status)
        except:
            change_code = data['change_code']
            recomendation = data['recomendation']
            if check:
                await rq.update_dev_query(id, change_code, recomendation)
            

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        consumer.close()
        print('Бот выключен')