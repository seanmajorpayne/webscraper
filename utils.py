import os
import re
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timezone

"""
Utilities for creating directories and files.

TODO: Refactor duplicate code into more generic methods
TODO: Perform different saves depending on content-type
"""


def read_metadata(urls):
    """
    Prints metadata related to the urls to standard out.

    :param urls: list (str)
    """
    print("\nMetadata:")
    for url in urls:
        protocol_remover = re.compile(r"https?://")
        new_url = protocol_remover.sub("", url)
        base_path = os.fspath(Path().resolve())
        directory = "fetch/" + new_url
        file_name = new_url + ".txt"
        with open(os.path.join(directory, file_name), "r") as f:
            print("\n" + f.read())


def create_dir(directory):
    """
    Creates a directory to store downloaded web pages.

    TODO: Add sub-directories for assets, make generic

    :param directory: str
    """
    base_path = os.fspath(Path().resolve())
    if directory != "fetch":
        base_path = os.path.join(base_path, "fetch")
    path = os.path.join(base_path, directory)
    try:
        os.mkdir(path)
    except OSError as e:
        print("{} directory already exists. Continuing...".format(directory))


def save_metadata_file(url, html_tags):
    """
    Creates a metadata file for a site with a
    timestamp of the current web scraping.

    Overwrites metadata if it already exists.

    TODO: Handle missing params

    :param url: str
    """
    directory = "fetch/" + url
    file_name = url + ".txt"
    now = datetime.now(timezone.utc)
    date_time = now.strftime("%a %b %d,%Y %H:%M:%S %Z")
    message = "Site: {}\nLast scraped: {}\nImages: {}\nLinks: {}".format(
        url, date_time, html_tags["num_img"], html_tags["num_links"]
    )
    try:
        with open(os.path.join(directory, file_name), "w+") as f:
            f.write(message)

    except:  # TODO replace generic except
        print("Unable to save {} metadata.".format(url))


def save_html_page(url, body, file_ext):
    """
    Save a response body to disk.
    Path should be CWD/fetch/www.example.com

    TODO: Remove generic excepts, handle missing params

    :param url: str
    :param body: response body
    :param file_ext: str
    """
    protocol_remover = re.compile(r"https?://")
    new_url = protocol_remover.sub("", url)
    create_dir(new_url)
    file_name = new_url + "/" + new_url + "." + file_ext  # example.com/example.com.html

    try:
        with open(os.path.join("fetch/", file_name), "w+") as f:
            f.write(body)

    except:
        print("Unable to save {} to a file.".format(url))

    return new_url


def get_html_tags(body):
    """
    Counts the number of images and links in the body

    TODO: Replace generic except

    :param body: response body
    :return: html_tags (dict)
    """
    html_tags = {}

    try:
        soup = BeautifulSoup(body, features="html.parser")
        num_img = len(soup.findAll("img"))
        num_links = len(soup.findAll("a"))
    except:
        num_img, num_links = 0, 0  # Default case?

    html_tags["num_img"] = num_img
    html_tags["num_links"] = num_links

    return html_tags
