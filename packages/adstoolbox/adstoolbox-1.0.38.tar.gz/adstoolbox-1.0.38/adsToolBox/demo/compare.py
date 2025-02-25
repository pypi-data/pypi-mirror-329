from adsToolBox.global_config import set_timer
from adsToolBox.logger import Logger
from adsToolBox.loadEnv import env
from adsToolBox.dbMssql import dbMssql
from adsToolBox.dataComparator import dataComparator

table_name = '[data].[D365_CustomersV3]'
table = 'D365_CustomersV3'
batch_size = 50_000

set_timer(True)
logger = Logger(Logger.INFO, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source_conn = dbMssql({'database': env.MSSQL_DWH_DB,
                      'user': env.MSSQL_DWH_USER,
                      'password': env.MSSQL_DWH_PWD,
                      'port': env.MSSQL_DWH_PORT_VPN,
                      'host': env.MSSQL_DWH_HOST_VPN}, logger)
dest_conn = dbMssql({'database': env.MSSQL_DWH_DB,
                      'user': env.MSSQL_DWH_USER,
                      'password': env.MSSQL_DWH_PWD,
                      'port': env.MSSQL_DWH_PORT_VPN,
                      'host': env.MSSQL_DWH_HOST_VPN}, logger)

comparator = dataComparator({
    'db_source_1': source_conn,
    'query_source_1': f"SELECT * FROM {table_name}",
    'db_source_2': dest_conn,
    'query_source_2': f"SELECT * FROM {table}"
}, logger)

comparator.compare()

