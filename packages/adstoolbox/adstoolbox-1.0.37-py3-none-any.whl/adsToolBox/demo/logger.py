from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger

from adsToolBox.global_config import set_timer

set_timer(True)
logger = Logger(Logger.DEBUG, "EnvLogger", timestamp_display=False, name_display=False)
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

logger.info("Message d'info")
logger.debug("Message de debug")
logger.warning("Message de warning")
logger.error("Message d'erreur")
logger.custom_log(25, "Message custom")

logger.log_close("Réussite", "Tout le script a fonctionné")

logger.info("Cela ne devrait pas s'afficher.")
