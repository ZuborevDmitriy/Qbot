import json
import asyncio, logging
from datetime import datetime
import database.request as rq
from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer('updmess',bootstrap_servers='localhost:9092',enable_auto_commit=False,auto_offset_reset='earliest',heartbeat_interval_ms=3000,max_poll_interval_ms=30000,session_timeout_ms=45000)

async def main():
    for message in consumer:
        data = json.loads(message.value)
        date = data.get('devdate')
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        db_info = await rq.research_query()
        print(data)
        print(db_info)
        for values in db_info:
            if(values[0]==int(data.get('id'))):
                if(date>values[1]):
                    try:
                        status = data['status']
                        await rq.upd_dev_query(values[0], status)
                    except:
                        change_code = data['change_code']
                        recomendation = data['recomendation']
                        await rq.update_dev_query(values[0], change_code, recomendation)
                    


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        consumer.close()
        print('Бот выключен')