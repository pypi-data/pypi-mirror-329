
import os.path
import sys

from loguru import logger
from pylizlib.os import pathutils

LOGGER_PYLIZ_AI_NAME = "PylizAI"

# Configurazione di default, disattivata
def configure_logger():
    logger.remove()  # Rimuove eventuali configurazioni esistenti

    path_log_file = os.path.join(os.getcwd(), "pylizmedia.log")

    config = {
        "handlers": [
            {"sink": sys.stdout, "format": "{time:HH:mm:ss} [{level}]: {message}", "level": "TRACE"},
            {"sink": path_log_file, "serialize": True, "level": "TRACE"},
        ]
    }
    logger.configure(**config)
    logger.disable(LOGGER_PYLIZ_AI_NAME)  # Disabilita i log all'avvio

# Configura il logger al primo import
configure_logger()

# Funzioni per attivare/disattivare i log
def enable_logging():
    logger.enable(__name__)
    logger.enable(LOGGER_PYLIZ_AI_NAME)

def disable_logging():
    logger.disable(__name__)
    logger.disable(LOGGER_PYLIZ_AI_NAME)


def pyblizai_log_test():
    logger.info("This is a test log message from PylizAi.")
    logger.debug("This is a debug message from PylizAi.")
    logger.error("This is an error message from PylizAi.")
    logger.warning("This is a warning message from PylizAi.")
    logger.critical("This is a critical message from PylizAi.")
    logger.trace("This is a trace message from PylizAi.")



# # pylizai/logging.py
# from loguru import logger as base_logger
#
# # Crea un logger specifico per PylizAi
# logger = base_logger.bind(library="PylizAi")
#
# # Mantieni una lista di ID delle destinazioni per rimuoverle
# _destinations = []
#
# # Disattiva tutti i log globali all'inizio
# base_logger.remove()
#
# def enable_logging(level="TRACE", file_path=None, to_stdout=True):
#     """Abilita il logging con il livello e il percorso file opzionali per PylizAi."""
#
#     global _destinations
#
#     # Rimuovi eventuali destinazioni già aggiunte
#     for dest in _destinations:
#         logger.remove(dest)
#     _destinations = []
#
#     # Log su file
#     if file_path:
#         dest_file = logger.add(
#             file_path,
#             level=level,
#             format="{time} {level} {extra[library]} {message}",
#             rotation="10 MB",
#             compression="zip",
#             serialize=False
#         )
#         _destinations.append(dest_file)
#
#     # Log su stdout
#     if to_stdout:
#         dest_stdout = logger.add(
#             lambda msg: print(msg, end=""),  # Stampare direttamente a stdout
#             level=level,
#             format="{time:HH:mm:ss} {level} {extra[library]} {message}"
#         )
#         _destinations.append(dest_stdout)
#
#     #logger.info("Logging abilitato per la libreria PylizAi.")


def format_log_result(text: str) -> str:
    return f"\n\n{text}\n"
