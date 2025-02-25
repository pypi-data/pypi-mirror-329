from adsToolBox.global_config import set_timer
from adsToolBox.logger import Logger
from adsToolBox.loadEnv import env
from adsToolBox.dbMssql import dbMssql
from adsToolBox.pipeline import pipeline

source_table = "D365_CustomersV3"
dest_table = "D365_CustomersV4"
batch_size = 1_000

set_timer(True)
logger = Logger(Logger.INFO, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/Demo/.env')

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
source_conn.connect()
dest_conn.connect()

query_columns = f"""
    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE table_name='{source_table}' AND table_schema='dbo';"""
result = list(source_conn.sqlQuery(query_columns))[0]

list_cols = []
col_def = []
for item in result:
    col_name = item[0]
    data_type = item[1]
    max_length = item[2]
    num_prec = item[3]
    num_scale = item[4]
    list_cols.append(col_name)
    to_add = f"[{col_name}]"
    if data_type in ['varchar', 'nvarchar', 'char', 'nchar', 'varbinary'] and max_length:
        to_add+=f" {data_type} ({max_length})"
    elif data_type in ["decimal", "numeric"]:
        prec = num_prec or 18
        scale = num_scale or 2
        to_add+=f" {data_type} ({prec}, {scale})"
    else:
        to_add+=f"  varchar (200)"
    col_def.append(to_add)
creation_query = f"CREATE TABLE {dest_table} ({', '.join(col_def)})"

logger.warning("Début du transfert !")

# Étape 1 : Obtenez le nombre total de lignes
total_row_count = source_conn.sqlScalaire(f"SELECT COUNT(*) AS total_rows FROM {source_table}")
logger.info(f"Nombre total de lignes à transférer : {total_row_count}")

# Étape 2 : Transfert par batch
num_batches = total_row_count // batch_size + 1
logger.info(f"Nombre de batchs nécessaires : {num_batches}")

logger.info("Suppression de la table si elle existe.")
dest_conn.sqlExec(f"DROP TABLE IF EXISTS {dest_table};")
logger.info("Recréation de la table.")
dest_conn.sqlExec(creation_query)

list_cols.remove('nx_hash')

destination = {
    'name': 'copie table',
    'db': dest_conn,
    'table': dest_table,
    'schema': 'dbo',
    'cols': list_cols
}
query = f"SELECT {', '.join(list_cols)} FROM {source_table}"

pipe = pipeline({
    'db_source': source_conn,
    'query_source': query,
    'db_destination': destination,
    'batch_size': batch_size
}, logger)

print(pipe.run())