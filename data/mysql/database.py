from aiomysql import Pool
from .connect import db_connect
import csv


class DataBase:
    pool: Pool = db_connect

    async def insert(self, sql, data=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, data)

    async def select_all(self, sql, data=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, data)
                return [i[0] for i in await cur.fetchall()]

    async def select_one(self, sql, data=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, data)
                return list(await cur.fetchone())[0]
    
    async def db_to_csv(self, table_name, table_columns):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'SELECT * FROM {table_name}')
                file_path = f'temp/{table_name}.csv'  
                data = [i for i in await cur.fetchall()]
                with open(file_path, 'w') as f:
                    writer = csv.writer(f)
                    for column in table_columns:
                        writer.writerow(column)
                    for row in data:
                        writer.writerow(row)
                return file_path
            
            
    async def check_user_in_database(self, user):
        all_users = await self.select_all('SELECT user_id FROM users')
        if user not in all_users:
            await self.insert('INSERT INTO users (user_id, categories) VALUES (%s, %s)', (user, None))
            
    # async def top_up_balance(self, user, amount):
    #     await self.insert('UPDATE users_info SET balance = balance + %s WHERE user_id = %s', (amount, user))
    #     await self.insert('UPDATE users_info SET total_balance = total_balance + %s WHERE user_id = %s', (amount, user))
    
    # async def get_ur_balance(self, acc):
    #     balance = await self.select_one('SELECT balance FROM ur_accounts WHERE phone_number = %s', (acc,))
    #     return balance
    
    # async def get_ur_empty_accounts(self):
    #     accounts = await self.select_all('SELECT phone_number FROM ur_accounts WHERE valid = %s AND user_id IS %s AND description IS %s', 
    #                     (1, None, None))
    #     return accounts

    # async def get_all_ur_accounts_data(self):
    #     return await self.db_to_csv('ur_accounts', [['phone_number', 'refresh_token', 'balance', 'user_id', 'auto_stop_ride', 'valid', 'promo', 'description']])
    