from db.db import engine, Base
from models.models import *

# Создание всех таблиц в БД


async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        print('All tables are created successfully...')
