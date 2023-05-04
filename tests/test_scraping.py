"""Tests the functionality in the source/library/scraping.py file."""

from library.etl import pages_to_chunks
from library.scraping import scrape_all_urls


def test_scraping_conda() -> None:
    """Test that we recurisvely scrape the urls on conda.org."""
    results = scrape_all_urls('http://conda.org')
    assert isinstance(results, set)
    assert len(results) > 10
    first_item = list(results)[0]
    assert len(first_item) == 2
    assert isinstance(first_item, tuple)
    assert 'conda.org' in first_item[0]
    assert '<!doctype html>' in first_item[1]

    # check for duplicate urls or contents
    urls = [x[0][:-1] if x[0].endswith('/') else x[0] for x in results]
    htmls = [x[1] for x in results]
    assert len(urls) == len(set(urls))
    assert len(htmls) == len(set(htmls))

    chunks = pages_to_chunks(values=results, chunk_size=200)
    assert set(urls) == {x[0] for x in chunks}
    assert all(len(x[1]) <= 200 for x in chunks)
