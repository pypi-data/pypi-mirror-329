from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger
from adsToolBox.dbMssql import dbMssql
from adsToolBox.global_config import set_timer


logger = Logger(Logger.DEBUG, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source = dbMssql({'database': env.MSSQL_DWH_DB,
                        'user': env.MSSQL_DWH_USER,
                        'password': env.MSSQL_DWH_PWD,
                        'port': env.MSSQL_DWH_PORT,
                        'host': env.MSSQL_DWH_HOST,
                        'package': 'pymssql'}, logger, 50_000)
source.connect()
set_timer(True)

source.sqlExec('''
IF OBJECT_ID('dbo.insert_test', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test;
CREATE TABLE dbo.insert_test (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);''')

source.insert("insert_test", ["name", "email"], ["Hélène", "hélène@gmail.com"])

source.insertMany("insert_test", ["name", "email"], [(f'Hélène {i}', f'email{i}@example.com') for i in range(50)])

source.insertBulk("dbo", "insert_test", ["name", "email"], [(f'Hélène {i}', f'email{i}@example.com') for i in range(50_000)])

res = list(source.sqlQuery("SELECT * FROM insert_test;"))
print(len(res))