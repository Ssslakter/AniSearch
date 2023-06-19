from src.anisearch import configs
from src.anisearch.core.services import Services

config = configs.load_configs(".env")
services = Services(config)
