import os
import asyncio, asyncpg, logging
import json
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from regist.handlers import regist_router
from create_question.handlers import create_question_router
from active_question.handlers import active_question_router
from archive_question.handlers import archive_question_router
from dev_block.handlers import dev_question_router
from menu.handlers import menu_router
from aiogram.enums import ParseMode
from database.models import async_main
import database.request as rq
from config.config import SQL_URL

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def query_appear(conn, pid, channel, payload):
    data = json.loads(payload)
    author_id = data.get('author')
    query_id = data.get('query')
    await bot.send_message(int(author_id), text=f"Добавилась новая запись №{query_id}.")

async def on_query_change(conn, pid, channel, payload):
    data = json.loads(payload)
    query_id = data.get('query_id')
    author_id = data.get('author_id')
    result_text = ''
    for field, value in data["changes"].items():
        match field:
            case "change_code": field = "Код изменения"
            case "date": field = "Дата"
            case "recomendation": field = "Рекомендация"
            case "status": field = "Статус"
        result_text += f"🔸{field} → {value}\n"
    await bot.send_message(int(author_id), text=f"Анкета №{query_id} изменилась:\n{result_text.strip()}")

async def main():
    conn = await asyncpg.connect(SQL_URL)
    await conn.add_listener("user_notifications", query_appear)
    await conn.add_listener("query_changes", on_query_change)
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(menu_router, regist_router, create_question_router, active_question_router, archive_question_router, dev_question_router)
    # await async_main()
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')