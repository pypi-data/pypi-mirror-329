from adsToolBox.logger import Logger
from adsToolBox.loadEnv import env
from adsToolBox.global_config import set_timer
from adsToolBox.dbPgsql import dbPgsql
from adsToolBox.dbSql import dbSql

logger = Logger(Logger.INFO, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')
set_timer(True)

connection = dbSql({
    "techno": "postgresql",
    "database": env.PG_DWH_DB,
    "user": env.PG_DWH_USER,
    "password": env.PG_DWH_PWD,
    "port": env.PG_DWH_PORT,
    "host": env.PG_DWH_HOST
}, logger, 10_000)
connection.connect()

connection.sqlExec('''
DROP TABLE IF EXISTS insert_test;
CREATE TABLE IF NOT EXISTS insert_test (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    age INT
);''')

cols = ['name', 'email', 'age']
rows = [[f'name_{i}', f'email_{i}', i] for i in range(1, 101)]

result = connection.insertBulk('', 'insert_test', cols, rows)
print(f"Insert : {result}")

cols = ['id', 'name', 'email', 'age']
rows = [[i, 'UPSERT', 'UPSERT', 10_000] for i in range(50, 10_001)]
result = connection.upsertBulk('', 'insert_test', cols, rows, ["id"])
print(f"Upsert : {result}")
