from adsToolBox.loadEnv import env
from adsToolBox.dbPgsql import dbPgsql
from adsToolBox.dbMssql import dbMssql
from adsToolBox.pipeline import pipeline
from adsToolBox.logger import Logger
from adsToolBox.global_config import set_timer

logger = Logger(Logger.DEBUG, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source_pg = dbPgsql({'database':env.PG_DWH_DB
                    , 'user':env.PG_DWH_USER
                    , 'password':env.PG_DWH_PWD
                    , 'port':env.PG_DWH_PORT
                    , 'host':env.PG_DWH_HOST}, logger)
source_pg.connect()
source_pg.sqlExec('''
DROP TABLE IF EXISTS insert_test;
CREATE TABLE IF NOT EXISTS insert_test (
    id SERIAL PRIMARY KEY, varchar_col VARCHAR(255), char_col CHAR(100), text_col TEXT, int_col INT,
    bigint_col BIGINT, decimal_col DECIMAL(18, 2), numeric_col NUMERIC(18, 2), float_col FLOAT, real_col REAL, 
    date_col DATE, datetime_col TIMESTAMP, datetime2_col TIMESTAMP, time_col TIME, bit_col BOOLEAN,
    uniqueidentifier_col UUID
);''')

n = 10_000
batch_size = max(n//20, 1_000)
source_pg.batch_size = batch_size

rows = [
    (f'Name {i}', f'A{i}', f'Text example {i}', i, 100000000000 + i, 123.45 + i, 123.45 + i, 123.456 + i, 123.4 + i,
     f'2025-02-21', f'2025-02-21 12:34:56', f'2025-02-21 12:34:56.123456', f'12:34:56', 1 if i % 2 == 0 else 0,
     f'{str(i).zfill(8)}-0000-0000-0000-000000000000') for i in range(1, n + 1)
]

cols = [
    'varchar_col', 'char_col', 'text_col', 'int_col', 'bigint_col', 'decimal_col', 'numeric_col', 'float_col',
    'real_col', 'date_col', 'datetime_col', 'datetime2_col', 'time_col', 'bit_col', 'uniqueidentifier_col'
]

print(source_pg.insertBulk('', 'insert_test', cols, rows)[:2])

source_mssql = dbMssql({'database': env.MSSQL_DWH_DB,
                      'user': env.MSSQL_DWH_USER,
                      'password': env.MSSQL_DWH_PWD,
                      'port': env.MSSQL_DWH_PORT,
                      'host': env.MSSQL_DWH_HOST}, logger, batch_size)
source_mssql.connect()
set_timer(True)

destination = {
    'name': 'test',
    'db': source_mssql,
    'table': 'insert_test_2',
    'schema': 'dbo',
    'cols': [
        'varchar_col', 'char_col', 'text_col', 'int_col', 'bigint_col',
        'decimal_col', 'numeric_col', 'float_col', 'real_col',
        'date_col', 'datetime_col', 'datetime2_col', 'time_col', 'bit_col', 'uniqueidentifier_col', 'nx_hash'
    ],  # Colonnes dans la table MSSQL
    'hash': 'nx_hash'  # Colonne où sera stocké le hash
}

destination["db"].sqlExec('''
IF OBJECT_ID('dbo.insert_test_2', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test_2;
CREATE TABLE dbo.insert_test_2 (
    id INT IDENTITY(1,1) PRIMARY KEY, varchar_col VARCHAR(255), char_col CHAR(100), text_col TEXT, int_col INT, 
    bigint_col BIGINT, decimal_col DECIMAL(18, 2), numeric_col NUMERIC(18, 2), float_col FLOAT, real_col REAL, 
    date_col DATE, datetime_col DATETIME, datetime2_col DATETIME2, time_col TIME, bit_col BIT, 
    uniqueidentifier_col UNIQUEIDENTIFIER, nx_hash VARCHAR(32));''')

query = '''
SELECT varchar_col, char_col, text_col, int_col, bigint_col, decimal_col, numeric_col, float_col, real_col, date_col, 
    datetime_col, datetime2_col, time_col, bit_col, uniqueidentifier_col FROM insert_test;
'''

# Déclaration du pipeline
pipe = pipeline({
    'db_source': source_pg, # La source du pipeline
    'query_source': query, # La requête qui sera exécutée sur cette source
    'db_destination': destination, # La destination du pipeline
    'batch_size': batch_size
}, logger)

print(pipe.run())

logger.info("Fin de la démonstration")
