import asyncio

from db.services import create_tables


async def main():
    # запуск функции с созданием всех таблиц в БД
    await create_tables()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print('exiting program...')
