import asyncpg
from ..conn import PostgreSQLConnection

from datetime import datetime, timedelta
class User(PostgreSQLConnection):

    __tablename__ = "user_data"

    async def create_table(self):

        async with PostgreSQLConnection.cursor.acquire() as curs:

            await curs.execute("""CREATE TABLE IF NOT EXISTS users (
                            id SERIAL,
                            user_id BIGINT,
                            username TEXT,
                            full_name TEXT,
                            phone_number TEXT,
                            email TEXT,
                            referal_id BIGINT,
                            reg_date TIMESTAMP,
                            PRIMARY KEY (id))""")

    
    async def get_my_referals_count_month(self, user_id: int | str):
        async with PostgreSQLConnection.cursor.acquire() as curs:
            current_date = datetime.now()
            last_month = current_date - timedelta(days=30)
            data = await curs.fetchval(f"SELECT COUNT(*) FROM users WHERE referal_id = $1  AND reg_date > $2", user_id, last_month)
            
            return data
    
    async def get_my_referals_count(self, user_id: int | str):
        async with PostgreSQLConnection.cursor.acquire() as curs:
            data = await curs.fetchval(f"SELECT COUNT(*) FROM users WHERE referal_id = $1", user_id)
            return data
    
    async def get_my_2_referals_count(self, user_id: int | str):
        async with PostgreSQLConnection.cursor.acquire() as curs:
            data = await curs.fetchval(f"SELECT COUNT(*) FROM users WHERE referal_id = $1", user_id)
            return data
    
    async def get_my_2_referals_count_month(self, user_id: int | str):
        async with PostgreSQLConnection.cursor.acquire() as curs:
            current_date = datetime.now()
            last_month = current_date - timedelta(days=30)
            data = await curs.fetchval(f"SELECT COUNT(*) FROM users WHERE referal_id = $1  AND reg_date > $2", user_id, last_month)
            return data
    
    
    async def get_my_referal_id(self, user_id: int | str):
        async with PostgreSQLConnection.cursor.acquire() as curs:
            data = await curs.fetchrow(f"SELECT referal_id FROM users WHERE user_id = $1", user_id)
            return data["referal_id"]
            
            
    async def get_all_users(self):
        async with PostgreSQLConnection.cursor.acquire() as curs:

            await curs.execute("SELECT * FROM user_data")

    async def register_user(self, user_id, username, fullname, phone_number, email, referal_id):
        async with PostgreSQLConnection.cursor.acquire() as curs:

            await curs.execute("INSERT INTO users (user_id, username, full_name, phone_number, email, referal_id, reg_date) VALUES"\
                f"($1, $2, $3, $4, $5, $6, NOW());",
                user_id, username, fullname, phone_number, email, referal_id)



