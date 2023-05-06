import logging
import click
from dotenv import find_dotenv, load_dotenv
from data_writers import JsonWriter
from shikimori import ShikimoriAnimeParser
from utils import WebDriverBuilder


@click.command()
@click.option('--page_amount', '-p', type=int)
@click.option('--verbose', '-v', default=True)
@click.argument('output_filepath', type=click.Path())
def get_data(output_filepath='./', page_amount=1, verbose=True):
    """Method to run to get anime dataset
    """
    logger = logging.getLogger(__name__)

    writer = JsonWriter(output_filepath)
    builder = WebDriverBuilder('chrome', verbose)

    anime_parser = ShikimoriAnimeParser(
        builder(), 'https://shikimori.me', page_amount, writer)

    fails = anime_parser.parse()
    if (len(fails) == 0):
        logger.info("Successfully parsed all data!")
    else:
        logger.warn(
            f"Not all data was parsed succesefully. Failed: \n {fails}")


if __name__ == '__main__':
    LOG_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)

    load_dotenv(find_dotenv())

    get_data()
