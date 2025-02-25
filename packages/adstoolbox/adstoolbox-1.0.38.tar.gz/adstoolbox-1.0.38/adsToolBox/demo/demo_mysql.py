from adsToolBox.loadEnv import env
from dbMysql import dbMysql
from adsToolBox.dbMssql import dbMssql
from adsToolBox.logger import Logger
from adsToolBox.pipeline import pipeline

logger = Logger(Logger.INFO, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source_dbmysql = dbMysql({'database': 'pegase',
                      'user': 'onyx_prod',
                      'password': '8XFNuFtA6a62HaWe',
                      'port': 3306,
                      'host': '10.0.4.229'}, logger)
source_dbmysql.connect()

source_dbmssql = dbMssql({'user': 'app_onyx_ods01',
                          'password': 'xpoca59100!!',
                          'host': '10.10.0.222'}, logger)
source_dbmssql.connect()

source_dbmssql.sqlExec("""
DROP TABLE IF EXISTS [nws].[PEG_STA_v_bo_caces_encours];
CREATE TABLE [nws].[PEG_STA_v_bo_caces_encours] (
    PEG_STA_v_bo_caces_encours VARCHAR(255),
    PEG_STA_naissance DATETIME2,
    PEG_STA_fin DATETIME2,
    PEG_STA_type_stage VARCHAR(255),
    PEG_STA_debut DATETIME2,
    PEG_STA_document_reglementaire VARCHAR(255),
    PEG_STA_code_produit VARCHAR(255),
    PEG_STA_nom VARCHAR(255),
    PEG_STA_centre VARCHAR(255),
    PEG_STA_examens VARCHAR(255),
    PEG_STA_prenom VARCHAR(255),
    PEG_STA_date_evaluation DATETIME2,
    PEG_STA_code_stage VARCHAR(255),
    PEG_STA_dir VARCHAR(255)
);""")

query = """
SELECT CODE_CENTRE, NAISSANCE, FIN, TYPE_STAGE, DEBUT, DOCUMENT_REGLEMENTAIRE, CODE_PRODUIT, NOM, CENTRE, EXAMENS, 
    PRENOM, DATE_EVALUATION, CODE_STAGE, DIR
FROM v_bo_caces_encours;"""

destination = {
    'name': 'bdd mssql',
    'db': source_dbmssql,
    'table': "PEG_STA_v_bo_caces_encours",
    'schema': "nws",
    'cols': ['PEG_STA_code_centre', 'PEG_STA_naissance', 'PEG_STA_fin', 'PEG_STA_type_stage', 'PEG_STA_debut',
             'PEG_STA_document_reglementaire', 'PEG_STA_code_produit', 'PEG_STA_nom', 'PEG_STA_centre',
             'PEG_STA_examens', 'PEG_STA_prenom', 'PEG_STA_date_evaluation', 'PEG_STA_code_stage', 'PEG_STA_dir']
}

pipe = pipeline({
    'db_source': source_dbmysql,
    'query_source': query,
    'db_destination': destination
}, logger)

print(pipe.run())