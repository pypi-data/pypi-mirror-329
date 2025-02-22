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

source_table = "D365_CustomersV3"

res = list(source_mssql.sqlQuery(f"SELECT TOP 4 nx_hash FROM {source_table}"))[0]

print(res)