import logging
import click
from dotenv import find_dotenv, load_dotenv
from src.data.utils import JsonWriter
from src.data.shikimori import ShikimoriAnimeParser, ShikimoriUserDataParser
from src.data.utils import WebDriverBuilder


def start_parsing(content_type: str, output_filepath='./', page_amount=1, with_browser_ui=True):
    """Method to start parsing data from shikimori.me
    """
    logger = logging.getLogger(__name__)

    writer = JsonWriter(output_filepath)
    builder = WebDriverBuilder('chrome', with_browser_ui)
    if content_type == 'anime':
        parser = ShikimoriAnimeParser(
            builder(), 'https://shikimori.me', page_amount, writer)
    elif content_type == 'users':
        parser = ShikimoriUserDataParser(
            builder(), 'https://shikimori.me', page_amount, writer)

    fails = parser.parse()
    if (len(fails) == 0):
        logger.info("Successfully parsed all data!")
    else:
        logger.warn(
            "Not all data was parsed succesefully. Failed: \n %s", fails
        )


@click.group()
def cli():
    click.echo("Use one of the subcommands to start scraping data")


@cli.command(help='''Gets anime data.\n
             If filename is not specified, result.json will be created in the directory''')
@click.option('--page_amount', '-p', type=int)
@click.option('--with_browser_ui', '-u', default=True)
@click.argument('out_path', type=click.Path())
def anime(out_path='./', page_amount=1, with_browser_ui=True):
    """Method run to get anime dataset
    """
    start_parsing('anime', out_path, page_amount, with_browser_ui)


@cli.command(help='''Gets users data.\n
             If filename is not specified, result.json will be created in the directory''')
@click.option('--page_amount', '-p', type=int)
@click.option('--with_browser_ui', '-u', default=True)
@click.argument('out_path', type=click.Path())
def users(out_path='./', page_amount=1, with_browser_ui=True):
    """Method run to get users dataset
    """
    start_parsing('users', out_path, page_amount, with_browser_ui)


if __name__ == '__main__':
    LOG_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)

    load_dotenv(find_dotenv())
    cli()
