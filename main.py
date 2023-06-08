import yaml
import time
import threading
import sys
from queue import Empty
from typing import List, Dict


from utils.log_config import logger
from crawler.state import CrawlerState
from crawler.base import BaseCrawler
from config_types import ConfigDict


def main(config_file_path: str) -> None:
    """
    Loads the configuration, initializes the crawler state, and starts the crawler threads.

    :param config_file_path: The path to the YAML configuration file.
    """
    with open(config_file_path, "r") as file:
        config: ConfigDict = yaml.safe_load(file)

    state_crawlers = CrawlerState(
        project_name=config["project"]["name"],
        project_directory=config["project"]["directory"],
        base_urls=config["base_urls"],
    )
    logger.info(f"Base urls: {state_crawlers.crawl_queue.queue}")

    create_crawler_threads(
        num_worker_threads=config["num_worker_threads"],
        state=state_crawlers,
        proxies=config["proxies"],
        timeout=config["request"]["timeout"],
    )


def create_crawler_threads(num_worker_threads: int, state: CrawlerState, proxies: Dict[str, str], timeout: int) -> None:
    """
    Creates and starts a specified number of crawler threads.

    :param num_worker_threads: The number of threads to create.
    :param state: The CrawlerState shared among all threads.
    :param proxies: Dictionary of proxies to be used for requests when crawling onion websites.
    :param timeout: The maximum time to wait for a response to a request.
    """

    active_threads: List[threading.Thread] = []

    for _ in range(num_worker_threads):
        thread = threading.Thread(target=crawl_worker, args=(state, proxies, timeout))
        thread.start()
        active_threads.append(thread)

    for thread in active_threads:
        thread.join()

def crawl_worker(state: CrawlerState, proxies: Dict[str, str], timeout: int) -> None:
    """
    The worker function that will be executed by each crawler thread. It continuously takes URLs from the queue and 
    crawls them until the queue is empty.

    :param state: The CrawlerState shared among all threads.
    :param proxies: Dictionary of proxies to be used for requests when crawling onion websites.
    :param timeout: The maximum time to wait for a response to a request.
    """

    try:
        while True:
            time.sleep(0.5)
            url = state.crawl_queue.get(block=False) #block=True & timeout => multithread | Block=False => 1 thread crawls the pages

            #logger.debug(f"Url get from queue {url}")

            # Check if the URL has been crawled
            if url in state.crawled_domains:
                logger.debug(f"Onion address {url} has already been crawled")
                continue

            #logger.info(f"Starting the crawler(s). \n")

            proxies_conf = (
                proxies
                if ".onion" in url
                else None
            )
            crawler = BaseCrawler(state, timeout, proxies_conf)

            crawler.crawl_page(threading.current_thread().name, url)

            state.crawl_queue.task_done()

    except Empty:
        logger.info(f"List of queue is empty")
        sys.exit("Terminating the program")


if __name__ == "__main__":
    main(config_file_path="./config.yaml")
