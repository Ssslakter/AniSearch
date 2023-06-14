import click
import logging
import pandas as pd
from src.data.artifacts import upload_artifacts
from dotenv import find_dotenv, load_dotenv
from src.anisearch.core import Storage, get_embeddings
from src.anisearch.configs import load_configs


@click.group()
def upload():
    """Run cli"""


@upload.command(help="""Upload artifacts to wandb with default settings""")
@click.argument("out_path", type=click.Path())
def to_wandb(out_path="./"):
    """Method run to upload artifacts"""
    upload_artifacts(out_path)


@upload.command(help="""Upload data to qdrant database""")
@click.argument("csv_path", type=click.Path())
def to_qdrant(csv_path="./data.csv"):
    """Method run to upload artifacts"""
    configs = load_configs()
    embeddings = get_embeddings(configs.models_dir)
    storage = Storage(embeddings, configs.qdrant)
    df = pd.read_csv(csv_path)
    storage.insert_df(df)


if __name__ == "__main__":
    LOG_FMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)
    load_dotenv(find_dotenv())
    upload()
