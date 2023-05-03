"""
Function definitions for the command line interface. The makefile calls the commands defined in
this file.

For help in terminal, navigate to the project directory, run the docker container, and from within
the container run the following examples:
    - `source/scripts/commands.py --help`
    - `source/scripts/commands.py extract --help`
"""

import logging.config
import logging
import click
from helpsk.logging import Timer
from library.scraping import scrape_all_urls

# import source.library.openai as openai
# import source.library.etl as etl
from source.service.datasets import DATA


logging.config.fileConfig(
    "source/config/logging_to_file.conf",
    defaults={'logfilename': 'output/log.log'},
    disable_existing_loggers=False,
)


@click.group()
def main() -> None:
    """Logic For Extracting and Transforming Datasets."""
    pass


@main.command()
def extract() -> None:
    """Extracts the data."""
    with Timer("Scraping Langchain Docs"):
        results = scrape_all_urls('https://python.langchain.com')

    logging.info(f"Scraped {len(results)} pages from Langchain Docs")
    assert len(results) > 500
    assert len(list(results)[0]) == 2
    DATA.langchain_docs.save(results)


@main.command()
def transform() -> None:
    """Transforms the reddit data."""
    pass


if __name__ == '__main__':
    main()
