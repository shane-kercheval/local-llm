"""Functions for scraping webpages."""

import asyncio
import logging
from urllib.parse import urlparse, urlunparse, urljoin
import aiohttp
from bs4 import BeautifulSoup


def is_same_domain(url_a: str, url_b: str) -> bool:
    """
    Returns True if `url_a` and `url_b` are the same url e.g. ignores http vs https.

    TODO: DOES NOT HANDLE `www`

    Args:
        url_a: first url
        url_b: url to compare against url_a

    Examples:
        >>> is_same_domain('https://example.com/page', 'https://example.com/page#section')
        True
        >>> is_same_domain('https://examples.com/page', 'https://example.com/page#section')
        False
    """
    return urlparse(url_a).netloc == urlparse(url_b).netloc


def remove_fragment(url: str) -> str:
    """
    Removes a fragments from a url.

    Args:
        url: url to remove fragment from, if applicable.

    Examples:
        >>> remove_fragment('https://example.com/page#section')
        'https://example.com/page'
        >>> remove_fragment('https://example.com/page')
        'https://example.com/page'
    """
    parsed_url = urlparse(url)
    cleaned_url_tuple = parsed_url._replace(fragment='')
    return urlunparse(cleaned_url_tuple)


async def _fetch_html(session: aiohttp.ClientSession, url: str) -> tuple[str, str]:
    """
    Returns a tuple containing the url in the first index and the extracted html in the second
    index. The url from the response is returned so that if there is a redirect, we retain the
    actual/redirected URL.
    """
    async with session.get(url) as response:
        text = await response.text()
        return response.status, str(response.url), text


def url_contains_file_name(url: str) -> bool:
    """
    Indicates whether or not the url contains a file name, which currently means whether or not a
    '.' appears in the section of the url after the last '/'.
    """
    if not url:
        return False
    return '.' in url.split('/')[-1]


async def _recursive_extract(
        session: aiohttp.ClientSession,
        url: str,
        base_url: str,
        visited: set[str],
        results: set[str]) -> None:
    """
    For the url provided, recursively extracts and builds a list of all referenced URLs (of the
    same domain).

    We separate the set of `visited` urls from the `results` to handle the case where some urls
    may result in redirects. For example, visiting `https://python.langchain.com` results in a
    redirect to `https://python.langchain.com/en/latest/`. The `results` contains the original and
    redirected urls to prevent revisiting.

    Args:
        session: ClientSession
        url: the url of the webpage to get the referenced urls
        base_url: the original/base-url; used to join relative urls to the base-url
        visited: set of all URLs that have already been visited
        results: set of all of the urls that have been found
    """
    url = remove_fragment(url)
    if url in visited:
        return

    visited.add(url)  # add url to the list of URLs we're building
    status, url, html = await _fetch_html(session, url)  # overwrite the url in case of redirect
    if status == 404:
        logging.info(f"404: {url}")
        return
    # Remove trailing slash from URL to avoid re-visiting same page
    # e.g `example.com` and `example.com/`
    if url.endswith('/'):
        url = url[:-1]
    visited.add(url)  # re-add in case of redirect which would return a different url
    results.add((url, html))

    # link = list(soup.find_all('a'))[10]

    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        next_url = link.get('href')

        if not next_url:
            continue

        # if there is no hostname, it is a partial/relative url and we need to join with base-url
        if urlparse(next_url).hostname is None:
            if not url.endswith('/') and not url_contains_file_name(url):
                next_url = urljoin(url + '/', next_url)
            else:
                next_url = urljoin(url, next_url)

        # skip if the domain is different i.e. external url
        elif not is_same_domain(url, next_url):
            continue

        # Recursively scrape the next URL
        await _recursive_extract(session, next_url, base_url, visited, results)


async def _scrape_all_urls(url: str) -> list[str]:
    """
    For a given url, returns a list of all urls refered to on the website (with the same domain).

    Args:
        url: url of the base-page.
    """
    async with aiohttp.ClientSession() as session:
        visited = set()
        results = set()
        await _recursive_extract(session, url, url, visited, results)
        return results


def scrape_all_urls(url: str) -> set[tuple[str, str]]:
    """
    Scrapes the html for a given url, finds all urls referenced in the html (with the same domain)
    and recursively scrapes those urls.

    Returns a set of tuples. The first index of the tuple is a url and the second index is the html
    of the correpsonding url.

    Args:
        url: url of the base-page.
    """
    # get the base url using r.url in case the website redirects
    # e.g `https://python.langchain.com` redirects to `https://python.langchain.com/en/latest`
    import requests
    r = requests.get(url)
    assert r.status_code == 200
    url = r.url
    if not url.endswith('/'):
        url += '/'
    return asyncio.run(_scrape_all_urls(url=url))


# async def _scrape_urls(urls: list[str]) -> list[str]:
#     """Async function for scraping the urls provded and returns the raw html."""
#     async with aiohttp.ClientSession() as session:
#         tasks = [_fetch_html(session, url) for url in urls]
#         return await asyncio.gather(*tasks)


# def scrape_urls(urls: list[str]) -> list[str]:
#     """Scrapes the urls provded and returns the raw html."""
#     return asyncio.run(_scrape_urls(urls=urls))
