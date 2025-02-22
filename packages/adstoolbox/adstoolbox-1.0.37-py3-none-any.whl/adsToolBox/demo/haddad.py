from adsToolBox.global_config import set_timer
from adsToolBox.logger import Logger
from adsToolBox.loadEnv import env
from adsToolBox.dbMssql import dbMssql
from adsToolBox import pipeline

schema = 'data'
table = 'D365_SPLCustExternalItemData'
batch_size = 20_000
set_timer(True)
logger = Logger(Logger.DEBUG, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source = dbMssql({'database': env.HADDAD_DWH_SRC,
                  'user': env.HADDAD_DWH_USER,
                  'password': env.HADDAD_DWH_PWD,
                  'host': env.HADDAD_DWH_HOST}, logger, batch_size)

cible = dbMssql({'database': env.HADDAD_DWH_CIBLE,
                  'user': env.HADDAD_DWH_USER,
                  'password': env.HADDAD_DWH_PWD,
                  'host': env.HADDAD_DWH_HOST}, logger, batch_size)
query = f"""
SELECT
    c.COLUMN_NAME AS ColumnName,
    t.NAME AS DataType,
    c.CHARACTER_MAXIMUM_LENGTH AS MaxLength,
    c.NUMERIC_PRECISION AS NumericPrecision,
    c.NUMERIC_SCALE AS NumericScale
FROM INFORMATION_SCHEMA.COLUMNS c
JOIN sys.types t ON c.DATA_TYPE = t.name
WHERE c.TABLE_NAME = '{table}' AND c.TABLE_SCHEMA = '{schema}'
ORDER BY c.ORDINAL_POSITION;
"""

source.connect()
gen = source.sqlQuery(query)
res = list(gen)[0]
cols = [elem[0] for elem in res]
cols_def = [
    f"{elem[1]}(MAX)" if elem[2] == -1 else f"{elem[1]}({elem[2]})"
    if elem[2] and elem[1] not in {"text", "ntext", "xml"}
    else elem[1]
    for elem in res
]

destination = {
    'name': 'Copie table',
    'db': cible,
    'schema': schema,
    'table': table,
    'cols': cols,
    'cols_def': cols_def
}



pipe = pipeline({
    'db_source': source,
    'query_source': query,
    'db_destination': destination,
    'batch_size': batch_size
}, logger)

pipe.create_destination_table(drop=True)

results = pipe.run()

print(results["nb_lines_success"], results["nb_lines_error"])
