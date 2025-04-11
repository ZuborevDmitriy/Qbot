import os
import asyncio, logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from regist.handlers import regist_router
from create_question.handlers import create_question_router
from active_question.handlers import active_question_router
from archive_question.handlers import archive_question_router
from dev_block.handlers import dev_question_router
from aiogram.enums import ParseMode
from database.models import async_main
import database.request as rq
from regist.handlers import dict

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def checker():
    old_values = {'id':str}
    flag = True
    while flag==True:
        await asyncio.sleep(10)
        try:
            old_values['id']=await rq.return_last_query(dict.get('phone'))
            flag = False
        except:
            print("Не могу найти данные!")
    while flag==False:
        await asyncio.sleep(10)
        new_values = await rq.return_last_query(dict.get('phone'))
        if old_values['id'] != new_values:
            await bot.send_message(dict.get('user_id'), text=f"Добавилась новая запись {new_values}.")
            old_values['id'] = new_values


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(regist_router, create_question_router, active_question_router, archive_question_router, dev_question_router)
    asyncio.create_task(checker())
    # await async_main()
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')