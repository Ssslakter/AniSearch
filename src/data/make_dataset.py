import logging
import click
from dotenv import find_dotenv, load_dotenv
from traitlets import default
from data_writers import JsonWriter
from shikimori import ShikimoriAnimeParser
from utils import WebDriverBuilder


# @click.command()
# @click.option('--page_amount', '-p', type=int)
# @click.option('--verbose', '-v', default=True)
# @click.argument('output_filepath', type=click.Path())
def get_data(output_filepath='./', page_amount=1, verbose=True):
    logger = logging.getLogger(__name__)

    writer = JsonWriter(output_filepath)
    builder = WebDriverBuilder('chrome', verbose)

    anime_parser = ShikimoriAnimeParser(
        builder(), 'https://shikimori.me', page_amount, writer)

    anime_parser.parse()
    logger.info("Successfully parsed all data!")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    load_dotenv(find_dotenv())

    get_data()
