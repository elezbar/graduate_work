import asyncpg
from asyncpg.exceptions import DuplicateDatabaseError


async def create_database():
    conn = await asyncpg.connect(user='postgres', password='postgres',
                                 host='localhost')
    try:
        await conn.execute('CREATE DATABASE movie_together')
        print("Database created successfully")
    except DuplicateDatabaseError:
        print("Database already exists")
    finally:
        await conn.close()
