from sqlalchemy import BigInteger, VARCHAR, BOOLEAN, TEXT, FLOAT, INTEGER, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config.config import SQLALCHEMY_URL

engine = create_async_engine(url=SQLALCHEMY_URL)
#echo=True для логов

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    user_info = mapped_column(VARCHAR(40), unique=True, nullable=False)
    phone_number = mapped_column(VARCHAR(11), unique=True, nullable=False)
    is_authorized = mapped_column(BOOLEAN, default=False, nullable=False)
    
class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(primary_key=True)
    city = mapped_column(TEXT, nullable=False)
    name = mapped_column(TEXT, nullable=False)
    project = mapped_column(TEXT, nullable=False)

class Album(Base):
    __tablename__ = 'albums'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(TEXT, nullable=False)

class Query(Base):
    __tablename__ = 'query'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    city_name = mapped_column(VARCHAR(20), nullable=False)
    commercial_name = mapped_column(VARCHAR(40), nullable=False)
    project_name = mapped_column(VARCHAR(40), nullable=False)
    comment = mapped_column(TEXT, nullable=False)
    album = mapped_column(VARCHAR(40), nullable=False)
    system_quest = mapped_column(BOOLEAN, default=False, nullable=False)
    state_of_works = mapped_column(VARCHAR(60), nullable=False)
    economic_effect = mapped_column(FLOAT, nullable=False)
    reduce_time = mapped_column(INTEGER, nullable=False)
    type_of_note = mapped_column(VARCHAR(40), nullable=True)
    POS = mapped_column(BOOLEAN, default=False, nullable=False)
    photo = mapped_column(TEXT, nullable=True)
    change_code = mapped_column(FLOAT, default=None, nullable=True)
    date = mapped_column(DateTime, default=None, nullable=True)
    recomendation = mapped_column(VARCHAR(40), default=None, nullable=True)
    status = mapped_column(VARCHAR(7), nullable=False)
    author_id = mapped_column(INTEGER, ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False)

async def async_main():
    async with engine.begin() as conn:
        # await conn.run_sync(Query.__table__.drop)
        await conn.run_sync(Base.metadata.create_all)