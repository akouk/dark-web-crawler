import yaml
import time
import threading
from queue import Empty
from typing import Dict, List

from utils.log_config import logger
from crawlers import state, page, onion
from config_types import ConfigDict


def main(config_file_path: str) -> None:
    with open(config_file_path, "r") as file:
        config: ConfigDict = yaml.safe_load(file)

    state_crawlers = state.CrawlerState(
        project_name=config["project"]["name"],
        project_directory=config["project"]["directory"],
        base_urls=config["base_urls"],
    )
    logger.info("Base urls: %s", state_crawlers.crawl_queue.queue)

    create_crawler_threads(
        num_worker_threads=config["num_worker_threads"],
        state=state_crawlers,
        proxies=config["proxies"],
        timeout=config["request"]["timeout"],
    )


def create_crawler_threads(num_worker_threads: int, state: state.CrawlerState, proxies: Dict[str, str], timeout: int) -> None:
    logger.debug("CREATING CRAWLER THREADS")
    active_threads: List[threading.Thread] = []

    for _ in range(num_worker_threads):
        thread = threading.Thread(target=crawl_worker, args=(state, proxies, timeout))
        thread.start()
        active_threads.append(thread)

    for thread in active_threads:
        thread.join()

    logger.debug("CRAWLER THREADS CREATED")


def crawl_worker(state: state.CrawlerState, proxies: Dict[str, str], timeout: int) -> None:
    logger.info("STARTING CRAWL WORKER")
    try:
        while True:
            logger.info("INSIDE WHILE TRUE")
            url = state.crawl_queue.get(block=False)

            logger.info(f"URL GET FROM QUEUE {url}")
            #logger.info(f"Active entries in queue: {state.crawl_queue.queue}")

            # Check if the URL has been crawled
            if url in state.crawled_domains:
                logger.info(f"URL {url} has already been crawled.")
                time.sleep(0.1)
                continue

            logger.info(f"Start the crawler for url {url}")

            crawler = (
                onion.OnionCrawler(state=state, proxies=proxies, timeout=timeout)
                if ".onion" in url
                else page.PageCrawler(state=state, timeout=timeout)
            )

            crawler.crawl_page(threading.current_thread().name, url)

            state.crawl_queue.task_done()

    except Empty:
        logger.info(f"List of queue is empty, terminating the program.")


if __name__ == "__main__":
    main(config_file_path="./config.yaml")
