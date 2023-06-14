import logging
import json
from pathlib import Path
import click
from dotenv import find_dotenv, load_dotenv
from src.data.artifacts import merge_data
from src.data.shikimori import (
    ShikimoriAnimeParser,
    ShikimoriUserDataParser,
    SHIKIMORI_URL,
)


def start_parsing(content_type: str, output_filepath="./", page_amount=1):
    """Method to start parsing data from shikimori.me"""

    if content_type == "anime":
        parser = ShikimoriAnimeParser(SHIKIMORI_URL, page_amount)
    elif content_type == "users":
        parser = ShikimoriUserDataParser(SHIKIMORI_URL, page_amount)
    else:
        raise ValueError(f"Incorrect content type: '{content_type}'")

    data, fails = parser.parse()
    file_path = Path(output_filepath)
    if file_path.is_dir():
        file_path /= "result.json"
    with open(file_path, "w+", encoding="utf-8") as file_path:
        json.dump(data, file_path)

    if len(fails) == 0:
        print("Successfully parsed all data!")
    else:
        print("Not all data was parsed succesefully. Failed: \n %s", fails)


@click.group()
def cli():
    """Run cli"""


@cli.command(
    help="""Gets anime data.\n
             If filename is not specified, result.json will be created in the directory"""
)
@click.option("--page_amount", "-p", type=int)
@click.argument("out_path", type=click.Path())
def parse_anime(out_path="./", page_amount=1):
    """Method run to get anime dataset"""
    start_parsing("anime", out_path, page_amount)


@cli.command(
    help="""Gets users data.\n
             If filename is not specified, result.json will be created in the directory"""
)
@click.option("--max_users", "-m", type=int)
@click.argument("out_path", type=click.Path())
def parse_users(out_path="./", max_users=10):
    """Method run to get users dataset"""
    start_parsing("users", out_path, max_users)


@cli.command(help="""Merges csv and jl data and save to out-path""")
@click.argument("csv_path", type=click.Path())
@click.argument("jl_path", type=click.Path())
@click.argument("out_path", type=click.Path())
def merge_datasets(csv_path="./data", jl_path="./data", out_path="./"):
    """Merges csv and jl data"""
    merged = merge_data(csv_path, jl_path)
    merged.to_csv(out_path, index=False)


if __name__ == "__main__":
    LOG_FMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)

    load_dotenv(find_dotenv())
    cli()
