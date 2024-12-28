import os
import asyncio, logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from regist.handlers import regist_router
from create_question.handlers import create_question_router
from active_question.handlers import active_question_router
from aiogram.enums import ParseMode
from database.models import async_main

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    # logging.basicConfig(level=logging.INFO)
    dp.include_routers(regist_router, create_question_router, active_question_router)
    # await async_main()
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')