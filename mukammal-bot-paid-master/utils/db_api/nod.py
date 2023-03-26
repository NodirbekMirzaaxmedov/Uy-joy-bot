from typing import Union
from environs import Env
import asyncpg
from asyncpg import Connection
from asyncpg import Pool
import os

env = Env()
env.read_env()

# from data import config

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
DB_HOST=env.str("DB_HOST")
class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None


    async def create(self):
        self.pool = await asyncpg.create_pool(
            user="postgres",
            password="V5KpU5QF3KHpLV9rYy0O",
            host="containers-us-west-45.railway.app",
            database="railway",
            port=7613
        )

    async def execute(self, command, *args,
                       fetch: bool=False,
                       fetchval: bool=False,
                       fetchrow: bool=False,
                       execute: bool=False 
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            username varchar(255) NULL,
            telegram_id BIGINT NOT NULL UNIQUE,
            telefon_raqami VARCHAR(255) NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod 
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=${num}" for num, item in enumerate(parameters.keys(),
                                                        start=1)
        ])
        return sql, tuple(parameters.values())

    
    async def create_table_Uylar(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Uylar (
            id SERIAL PRIMARY KEY,
            shaxar VARCHAR(255) NOT NULL,
            xonalari BIGINT NOT NULL,
            manzil VARCHAR(255) NOT NULL UNIQUE,
            narx VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=${num}" for num, item in enumerate(parameters.keys(),
                                                        start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_table_Kvartiralar(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Kvartiralar (
            id SERIAL PRIMARY KEY,
            shaxar VARCHAR(255) NOT NULL,
            manzil VARCHAR(255) NOT NULL,
            kvadrat BIGINT NOT NULL,
            xonalari BIGINT NOT NULL,
            qavat BIGINT NOT NULL,
            romlari VARCHAR(255) NOT NULL,
            eshiklari VARCHAR(255) NOT NULL,
            gishtlari VARCHAR(255) NOT NULL,
            isitish VARCHAR(255) NOT NULL,
            xolati VARCHAR(255) NOT NULL,
            qoladigan VARCHAR(255) NOT NULL,
            narx VARCHAR(255) NOT NULL,
            rasmlari VARCHAR(255) NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=${num}" for num, item in enumerate(parameters.keys(),
                                                        start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_table_Hovlilar(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Hovlilar (
            id SERIAL PRIMARY KEY,
            shaxar VARCHAR(255) NOT NULL,
            manzil VARCHAR(255) NOT NULL,
            kvadrat BIGINT NOT NULL,
            xonalari BIGINT NOT NULL,
            romlari VARCHAR(255) NOT NULL,
            eshiklari VARCHAR(255) NOT NULL,
            gishtlari VARCHAR(255) NOT NULL,
            isitish VARCHAR(255) NOT NULL,
            xolati VARCHAR(255) NOT NULL,
            qoladigan VARCHAR(255) NOT NULL,
            narx VARCHAR(255) NOT NULL,
            rasmlari VARCHAR(255) NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=${num}" for num, item in enumerate(parameters.keys(),
                                                        start=1)
        ])
        return sql, tuple(parameters.values())



    
    async def add_kvartira(self, shaxar, manzil, kvadrat,xonalari,qavat,romlari,eshiklari,gishtlari,isitish,xolati,qoladigan,narx,rasmlari):
        sql = "INSERT INTO Kvartiralar (shaxar,manzil,kvadrat,xonalari,qavat,romlari,eshiklari,gishtlari,isitish,xolati,qoladigan,narx,rasmlari) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13) returning *"
        return await self.execute(sql,shaxar,manzil,kvadrat,xonalari,qavat,romlari,eshiklari,gishtlari,isitish,xolati,qoladigan,narx,rasmlari, fetchrow=True)

    async def add_hovli(self, shaxar, manzil, kvadrat,xonalari,romlari,eshiklari,gishtlari,isitish,xolati,qoladigan,narx,rasmlari):
        sql = "INSERT INTO Hovlilar (shaxar,manzil,kvadrat,xonalari,romlari,eshiklari,gishtlari,isitish,xolati,qoladigan,narx,rasmlari) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12) returning *"
        return await self.execute(sql,shaxar,manzil,kvadrat,xonalari,romlari,eshiklari,gishtlari,isitish,xolati,qoladigan,narx,rasmlari, fetchrow=True)


    async def add_user(self, full_name, username, telegram_id,telefon_raqami):
        sql = "INSERT INTO Users (full_name, username, telegram_id,telefon_raqami) VALUES($1,$2,$3,$4) returning *"
        return await self.execute(sql,full_name,username,telegram_id,telefon_raqami, fetchrow=True)

    
    async def add_uy(self, shaxar,xonalari,manzil,narx):
        sql = "INSERT INTO Uylar (shaxar, xonalari, manzil,narx) VALUES($1,$2,$3,$4) returning *"
        return await self.execute(sql,shaxar, xonalari, manzil,narx, fetchrow=True)
    
    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_uylar(self):
        sql = "SELECT * FROM Uylar"
        return await self.execute(sql, fetch=True)

    async def select_uy(self,shaxar_ber,xona_ber,**kwargs):
        sql = f"SELECT * FROM Uylar Where shaxar='{shaxar_ber}' and xonalari={xona_ber}"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_uy_count(self,shaxar_ber,xona_ber,**kwargs):
        sql = f"SELECT COUNT(*) FROM Uylar Where shaxar='{shaxar_ber}' and xonalari={xona_ber}"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    
    async def select_kvartira(self,shaxar_ber,kvadrat_ber,xona_ber, qavat_ber,isitish_ber,xolat_ber,**kwargs):
        sql = f"SELECT * FROM Kvartiralar Where shaxar='{shaxar_ber}' and kvadrat >= {kvadrat_ber} and xonalari = {xona_ber} and qavat = {qavat_ber} and isitish='{isitish_ber}' and xolati='{xolat_ber}'"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    
    async def select_kvartira_count(self,shaxar_ber,kvadrat_ber,xona_ber, qavat_ber,isitish_ber,xolat_ber,**kwargs):
        sql = f"SELECT COUNT(*) FROM Kvartiralar Where shaxar='{shaxar_ber}' and kvadrat >= {kvadrat_ber} and xonalari = {xona_ber} and qavat = {qavat_ber} and isitish='{isitish_ber}' and xolati='{xolat_ber}'"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)


    
    async def select_hovli(self,shaxar_ber,kvadrat_ber,xona_ber,isitish_ber,xolat_ber,**kwargs):
        sql = f"SELECT * FROM Hovlilar Where shaxar='{shaxar_ber}' and kvadrat > {kvadrat_ber} and xonalari = {xona_ber} and isitish='{isitish_ber}' and xolati='{xolat_ber}'"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)


    async def select_user(self,telegram_id,**kwargs):
        sql = f"SELECT * FROM Users WHERE telegram_id={telegram_id}"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)
    
    async def count_uylar(self):
        sql = "SELECT COUNT(*) FROM Uylar"
        return await self.execute(sql, fetchval=True)
    
    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    