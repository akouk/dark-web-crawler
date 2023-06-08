import os
import sys
from queue import Queue
from typing import List

from utils.log_config import logger

class CrawlerState:
    """
    CrawlerState class maintains the state of a crawler, including the queue of URLs to be crawled and the set of 
    already crawled domains.
    """
    def __init__(self, project_name: str, project_directory: str, base_urls: List[str]) -> None:
        """
        Initializes CrawlerState with project details and base URLs.

        :param project_name: The name of the project.
        :param project_directory: The directory where the project is located.
        :param base_urls: A list of base URLs to start crawling from.
        """
        self.project_name = project_name
        self.project_directory = project_directory
        self.base_urls = base_urls

        self.crawled_domains = set()
        self.crawl_queue = Queue()
        self.initialize_crawler()

    def initialize_crawler(self) -> None:

        """
        Initializes the crawler state, creating the project directory and adding the base URLs to the crawl queue.
        """
        if not os.path.exists(self.project_directory):
            logger.critical(f"Invalid project directory: {self.project_directory}")
            sys.exit("Terminating the program")

        self.project_path = os.path.join(self.project_directory, self.project_name)
        if os.path.exists(self.project_path):
            logger.critical(f"Project directory already exists: {self.project_path}")
            sys.exit("Terminating the program")

        os.makedirs(self.project_path)
        logger.info(f"Created project directory: {self.project_path}")

        for url in self.base_urls:
            self.crawl_queue.put(url)

    def add_links_to_queue(self, links: List[str]) -> None:
        """
        Adds new links to the crawl queue, ignoring those that are already in the queue or have been crawled.

        :param links: A list of links to be added to the queue.
        """
        for link in links:
            if link in self.crawl_queue.queue or link in self.crawled_domains:
                continue
            self.crawl_queue.put(link)
