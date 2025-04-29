import logging
import os

# Garante que o diretório de logs existe
os.makedirs("logs", exist_ok=True)

# Configura o logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Formato das mensagens
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Configura o arquivo de saída
file_handler = logging.FileHandler("logs/api.log")
file_handler.setFormatter(formatter)

# Evitar adicionar múltiplos handlers se importar várias vezes
if not logger.hasHandlers():
    logger.addHandler(file_handler)

def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)
