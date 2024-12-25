import asyncio

from services.services import create_tables


async def main():
    # запуск функции с созданием всех таблиц в БД
    await create_tables()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print('There are some problems running application...exiting program...')
