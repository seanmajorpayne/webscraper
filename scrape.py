import validators.url as valid_url
import asyncio
import aiohttp
from utils import save_html_page, get_html_tags, save_metadata_file

"""
Scraper: Version 0.0.1

Given a user provided list of urls, scrapes the sites and logs
any errors to standard output.

Currently only supports Content-Types for text/html.
"""


class Scraper:
    def __init__(self, urls):
        self.urls = urls

    def perform_scraping(self):
        """
        Begins asynchronous scraping on the user provided sites.
        """
        asyncio.get_event_loop().run_until_complete(self.download_all_sites())

    def get_content_type(self, headers):
        """
        Extracts content type and file_ext from a response header.
        ex. "text" "html"

        TODO: move static method out of class?

        :param headers: A URL Request Header
        :return: content-type (str), file_ext (str)
        """
        if "Content-Type" not in headers:
            return None, None

        type_info, charset = headers["Content-Type"].split(";")
        content_type, file_ext = type_info.split("/")
        return content_type, file_ext

    async def download_site(self, session, url):
        """
        Requests a response from the url.
        Only sites with 2XX codes should be downloaded.

        TODO: Add support for non-text/non-html pages

        :param session: aiohttp ClientSession
        :param url: str
        """
        async with session.get(url) as response:
            if 200 <= response.status < 300:
                headers = response.headers
                content_type, file_ext = self.get_content_type(headers)

                if content_type == "text":
                    body = await response.text()
                    new_url = save_html_page(url, body, file_ext)
                    html_tags = get_html_tags(body)
                    save_metadata_file(new_url, html_tags)
                else:
                    print("Non-text body found for {}".format(url))

            else:
                print("A {} response was returned for {}".format(response.status, url))

    async def download_all_sites(self):
        """
        Parses a list of site urls and makes asynchronous requests to them.
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in self.urls:
                if valid_url(url):
                    task = asyncio.ensure_future(self.download_site(session, url))
                    tasks.append(task)
                else:
                    print("Invalid url provided {}".format(url))
            await asyncio.gather(*tasks, return_exceptions=True)
