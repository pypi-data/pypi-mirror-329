from adsToolBox.loadEnv import env
from adsToolBox.dbMssql import dbMssql
from adsToolBox.logger import Logger
from adsToolBox.global_config import set_timer

logger = Logger(Logger.DEBUG, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')
set_timer(True)

source_mssql = dbMssql({'database': env.MSSQL_DWH_DB,
                      'user': env.MSSQL_DWH_USER,
                      'password': env.MSSQL_DWH_PWD,
                      'port': env.MSSQL_DWH_PORT_VPN,
                      'host': env.MSSQL_DWH_HOST_VPN}, logger)
source_mssql.connect()

source_table = "test_date"

source_mssql.sqlExec(f"""
DROP TABLE IF EXISTS [{source_table}];
CREATE TABLE [{source_table}](
    integer INT,
    string VARCHAR(20),
    date DATETIME
);""")

source_mssql.insert(source_table, ['integer', 'string', 'date'], [2, "test_insert", "2024-03-18 16:22:40"])

rows10 = [[i, f'chaîne_{i}', f'2024-12-{i} 08:00:00'] for i in range(1,11)]
source_mssql.insertMany(source_table, ['integer', 'string', 'date'], rows10)

rows50_000 = [[i, f'chaîne_{i}', f'2024-12-{i%30+1} 09:00:00'] for i in range(1,50_001)]
print(rows50_000[0:2])
source_mssql.insertBulk(source_table, ['integer', 'string', 'date'], "dbo", rows50_000)