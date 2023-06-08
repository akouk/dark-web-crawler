import os
import requests

from threading import Lock
from typing import Tuple, Optional, List, Dict

from fake_useragent import UserAgent

from utils.log_config import logger
from crawler.state import CrawlerState
from config_types import ConfigProxies
from scrapper.page import PageScrapper


class BaseCrawler:
    """
    BaseCrawler is a utility class for web scraping. It fetches HTML content from provided URLs, parses it for .onion
    links, and manages crawled pages and the crawl queue.
    """
    def __init__(self, state: CrawlerState, timeout: int, proxies: ConfigProxies) -> None:
        """
        Initialize BaseCrawler with CrawlerState, timeout and proxy configuration.
        
        :param state: The current state of the crawler, containing the queue of URLs to be crawled and the set of 
                      already crawled domains.
        :param timeout: Timeout for requests in seconds.
        :param proxies: Dictionary of proxies to be used for requests.
        """
        self.state = state
        self.headers = self.get_random_headers()
        self.timeout = timeout
        self.proxies = proxies
        self.lock = Lock()

    @staticmethod
    def get_random_headers() -> Dict[str, str]:
        """
        Generate random request headers with a random User-Agent.

        :return: A dictionary with request headers.
        """
        user_agents_list = UserAgent()
        user_agent = user_agents_list.random
        return {"User-Agent": user_agent}

    def crawl_page(self, thread_name: str, page_url: str) -> None:
        """
        Crawl a single web page, extract links from it, and save its HTML content to a file if it's an .onion page.

        :param thread_name: The name of the thread currently performing the crawl.
        :param page_url: The URL of the page to be crawled.
        """

        logger.info(f"{thread_name} is now crawling {page_url}")
        logger.info(f"Queue {str(self.state.crawl_queue.qsize())} | Crawled {str(len(self.state.crawled_domains))}")

        html_content, found_links = self.fetch_pages(page_url, self.proxies, thread_name)

        if ".onion" in page_url:
            if html_content is not None:
                # Save HTML before removing URL from the queue
                self.save_html_content(page_url.replace("http://", "").replace(".onion", "") + ".html", html_content)
                logger.info(f"The content of {page_url} is successfully saved")
            else:
                logger.info(f"{thread_name} did not found html content on {page_url}.")

        if found_links is not None:
            self.state.add_links_to_queue(found_links)


        # Protect the update with a lock
        with self.lock:
            self.state.crawled_domains.add(page_url)

    def save_html_content(self, page_url: str, html_content: str) -> None:
        """
        Save the HTML content of a crawled page to a local file.

        :param page_url: The URL of the page whose content will be saved.
        :param html_content: The HTML content to be saved.
        """
        # Generate a valid file name from the URL
        file_path = os.path.join(
            self.state.project_directory, self.state.project_name, page_url)

        try:
            # Write HTML content to the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_content)
        except FileNotFoundError:
            pass
        except IOError as error:
            logger.info(f"An error occurred while writing the content of: {page_url}")
            logger.error(str(error))

    def fetch_pages(self, page_url: str, proxies: Optional[ConfigProxies], thread_name: str) -> Tuple[Optional[str], Optional[List[str]]]:
        """
        Fetch a web page, extract .onion links from it, and return the HTML content and the extracted links.

        :param page_url: The URL of the page to be fetched.
        :param proxies: Dictionary of proxies to be used for the request.
        :param thread_name: The name of the thread performing the request.
        :return: A tuple containing the HTML content and a list of .onion links. If any error occurs, both will be None.
        """

        try:
            response = requests.get(page_url, headers=self.headers, timeout=self.timeout, proxies=proxies)
        
            if response.status_code == 200:
                logger.info(f"Request from {thread_name} went through successfully")

                # Set default encoding to "utf-8" if encoding is None
                html_content = response.text

                page_scrapper = PageScrapper(html_content)
                domains = page_scrapper.find_onion_links()
                logger.info(f"{thread_name} found {len(domains)} links on {page_url}")

                return html_content, [f"http://{address}" for address in domains]

        except requests.exceptions.ConnectionError as error:
            # Extract the error message from the exception
            # Log only the error message
            logger.error(f"Connection Error for domain: {page_url}. ERROR: {str(error)}")
            pass

        except requests.exceptions.ReadTimeout as error:
            logger.error(f"Read timeout for domain: {page_url}. ERROR: {str(error)}")
            pass

        except requests.exceptions.Timeout:
            logger.error(f"Timeout for domain: {page_url}. ERROR: {str(error)}")
            pass
        
        return None, None

