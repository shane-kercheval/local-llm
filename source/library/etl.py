"""Functions that help in ETL process."""

from bs4 import BeautifulSoup


def pages_to_chunks(
        values: list[tuple[str, str]],
        chunk_size: int = 400,
        chunk_overlap: int = 20,
        search_div_class: str | None = None) -> list[tuple[str, str]]:
    """
    Takes a list of tuples (where the first item in the tuple is a url (str), and the second item
    in the url is the raw HTML (str) scraped from the url) and returns a list of tuples where the
    text from each HTML is chunked into smaller pieces.

    For example, this:

    ```
    [('example.com', '<html>This is an HTML page!</html>')]
    ```

    becomes:

    ```
    [
        ('example.com', 'This is an'),
        ('example.com', ' HTML page!')
    ]
    ```

    Args:
        values:
            list of tuples (where the first item in the tuple is a url (str), and the second item
            in the url is the raw HTML (str) scraped from the url)
        chunk_size:
            The target/maximum number of characters of the chunk
        chunk_overlap:
            The number of characters that overlap between each chunk.
        search_div_class:
            If provided, this function will only search for the text associated with the div
            element corresponding to this class. This is a way to indicate the main content.
    """
    chunks = []
    for url, html in values:
        soup = BeautifulSoup(html, 'html.parser')
        if search_div_class and (contents := soup.find(class_=search_div_class)):
            text = contents.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)

        from langchain.text_splitter import CharacterTextSplitter
        text_splitter = CharacterTextSplitter(
            separator=" ",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        page_chunks = text_splitter.split_text(text=text)
        for chunk in page_chunks:
            # if the chunk is larger than the chunk_size that means there are no spaces
            # which means that likely junk (e.g. javascript that wasn't parsed out)
            if len(chunk) <= chunk_size:
                chunks.append((url, chunk))

    return chunks
