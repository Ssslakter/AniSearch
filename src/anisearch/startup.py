import logging
from dotenv import find_dotenv, load_dotenv
from src.anisearch import configs
from src.anisearch.core.services import Services

config = configs.load_configs(".env")
services = Services(config)


def start_up():
    LOG_FMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)
    load_dotenv(find_dotenv())
    services.storage.init_collection(config.qdrant.collection_name)
    print("Server starting...")
