from adsToolBox.loadEnv import env
from adsToolBox.dbPgsql import dbPgsql
from adsToolBox.dbMssql import dbMssql
from adsToolBox.pipeline import pipeline
from adsToolBox.logger import Logger
from adsToolBox.global_config import set_timer

logger = Logger(Logger.DEBUG, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')
set_timer(True)

pg = dbPgsql({
    "database": env.PG_DWH_DB,
    "user": env.PG_DWH_USER,
    "password": env.PG_DWH_PWD,
    "port": env.PG_DWH_PORT,
    "host": env.PG_DWH_HOST
}, logger, 1_000)

mssql = dbMssql({
    "database": env.MSSQL_DWH_DB,
    "user": env.MSSQL_DWH_USER,
    "password": env.MSSQL_DWH_PWD,
    "host": env.MSSQL_DWH_HOST,
    "package": "pytds"
}, logger, 1_000)

dest = {
    'name': 'test',
    'db': mssql,
    'schema': 'dbo',
    'table': 'insert_test',
    'cols': ['name', 'email', 'age'],
    'cols_def': ['VARCHAR(255)', 'VARCHAR(255)', 'INT'],
    'conflict_cols': ["name"]
}

cols = ["name", "email", "age"]
rows = [[f"nom_{i}", f"émail_{i}", i] for i in range(1, 10_002)]

pipe = pipeline({
    'tableau': rows,
    'db_destination': dest,
    'operation_type': 'insert',
    'insert_method': 'bulk',
    'batch_size': 1_000
}, logger)

pipe.create_destination_table(True)

print(f"Pipe: {pipe.run()}")