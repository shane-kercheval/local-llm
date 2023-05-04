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
from library.etl import pages_to_chunks
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
    """Transform scraped urls/docs."""
    langchain_docs = DATA.langchain_docs.load()

    logging.info(f"Transforming {len(langchain_docs)} pages from Langchain Docs")
    # remove trailing `/` in url so it doesn't cause duplication or downstream issues
    urls_htmls = [
        (x[0][:-1] if x[0].endswith('/') else x[0], x[1]) for x in langchain_docs
    ]
    # exclude files that have the following extensions
    exclude_extensions = ['.css', '.ipynb', '.md', '.xml']
    urls_htmls = [
        x for x in urls_htmls if not any(x[0].endswith(ext) for ext in exclude_extensions)
    ]
    urls_htmls = sorted(urls_htmls, key=lambda x: x[0])

    chunk_size = 400
    with Timer("Chunking Langchain Docs"):
        # for each url, break html/text into smaller chunks
        chunks = pages_to_chunks(
            values=urls_htmls,
            chunk_size=chunk_size,
            search_div_class='bd-article',
            # ignore_div_classes=[
            #     'bd-header-article'
            #     'bd-sidebar-primary',
            #     'bd-sidebar-secondary',

            # ]
        )

    logging.info(f"Chunked into {len(chunks)} parts.")
    # there shouldn't be any chunks larger than the limit
    assert len([x for x in chunks if len(x[1]) > chunk_size]) == 0

    # remove small chunks, they are mostly junk and don't provide much value.
    num_chunks = len(chunks)
    chunks = [x for x in chunks if len(x[1]) > 50]
    logging.info(f"Removed {num_chunks - len(chunks)} chunks with <= 50 characters.")



    # from bs4 import BeautifulSoup
    # #soup = BeautifulSoup(urls_htmls[700][1])
    # temp = [x for x in urls_htmls if x[0] == 'https://python.langchain.com/en/latest/modules/agents/tools/examples/requests.html']
    # soup = BeautifulSoup(temp[0][1], 'html.parser')
    # soup.text
    # soup.get_text(separator=' ', strip=True)
    # urls_htmls[700][1]

    # chunks[1000][1]
    # chunks[1000][0]
    # temp = [x for x in chunks if len(x[1]) > 400]
    # temp[0][0]
    # temp[0][1]

    logging.info(f"Saving {len(chunks)} chunks.")
    DATA.langchain_doc_chunks.save(chunks)


@main.command()
def embed() -> None:
    """TBD."""
    langchain_doc_chunks = DATA.langchain_doc_chunks.load()

    from langchain.vectorstores import Chroma
    persist_directory = '/code/.vectordb/'

    texts = []
    metadatas = []

    for url, chunk in langchain_doc_chunks:
        texts.append(chunk)
        metadatas.append({'url': url})

    persist_directory = '/code/.vectordb/'
    vectordb = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        ids=[str(x) for x in range(len(texts))],
        persist_directory=persist_directory)
    vectordb.persist()



if __name__ == '__main__':
    main()
