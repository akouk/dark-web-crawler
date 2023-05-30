import threading
from queue import Empty
from typing import Dict, List


from configs import reader
from utils.log_config import logger
from crawlers import state, page, onion


def main():
    config_file_path = './configs/config.yaml'
    config = reader.read_config_file(config_file_path)
    (
        project_directory,
        project_name,
        base_urls,
        num_worker_threads,
        proxies
    ) = reader.get_config_values(config)

    # Yaml links
    state_crawlers = state.CrawlerState(
        project_name, project_directory, base_urls)
    logger.info('Base urls: %s', state_crawlers.crawl_queue.queue)

    create_crawler_threads(num_worker_threads, state_crawlers, proxies)
    #start_crawling(state_crawlers)


def create_crawler_threads(num_worker_threads, state, proxies):
    logger.debug("CREATING CRAWLER THREADS")
    active_threads: List[threading.Thread] = []
    for _ in range(num_worker_threads):
        thread = threading.Thread(target=crawl_worker, args=(state, proxies))
        thread.start()
        active_threads.append(thread)
    for thread in active_threads:
        thread.join()
    logger.debug("CRAWLER THREADS CREATED")



def crawl_worker(state: state.CrawlerState, proxies: Dict[str, str]):
    logger.info('STRATING CRAWL WORKER')

    while True:
        logger.info('INSIDE WHILE TRUE')
        url = state.crawl_queue.get(block=False)

        logger.info(f'URL GET FROM QUEUE {url}')
        logger.info(f'Active entries in queue: {state.crawl_queue.queue}')

        # Check if the URL has been crawled
        if url not in state.crawled_domains:
            logger.info(f'URL {url} NOT IN CRAWLED')

            if ".onion" in url:
                logger.debug("ONION LINK FOUND")
                logger.info("Creating OnionCrawler")
                crawler = onion.OnionCrawler(state, proxies=proxies)

            else:
                logger.debug("REGULAR LINK FOUND")
                logger.info("Creating PageCrawler")
                crawler = page.PageCrawler(state)

            crawler.crawl_page(threading.current_thread().name, url)

        else:
            logger.info(f"URL {url} has already been crawled.")

        state.crawl_queue.task_done()




#def assign_jobs(state: state.CrawlerState):
    for link in state.crawl_queue.queue:
        logger.info('Assigning job for link: %s', link)
        state.crawl_queue.put(link)
    state.crawl_queue.join()
    start_crawling()


#def start_crawling(state: state.CrawlerState):
    logger.debug("CRAWLING STARTED")

    if state.crawl_queue.qsize():
        logger.debug("QUEUED LINKS FOUND")
        #logger.info(f"{len(state.crawl_queue.qsize())} links in the queue")
        assign_jobs(state)


if __name__ == "__main__":
    main()
