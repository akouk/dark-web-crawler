import threading
from queue import Queue
from crawlers import PageCrawler, OnionCrawler
from CrawlerState import CrawlerState
from file_manager import *
from config_reader import *
from config_parser import *
from log_config import logger

config_file_path = 'config.yaml'
config = read_config_file(config_file_path)
(
    project_directory,
    project_name,
    results_name,
    base_urls,
    urls_to_crawl_file,
    crawled_urls_file,
    num_worker_threads,
    proxies
) = get_config_values(config)

#check_project_directory(project_directory, project_name, urls_to_crawl_file, crawled_urls_file, base_urls)
project_path = create_project_directory(project_directory, project_name)
if project_path:
    create_results_data_directory(project_path, results_name)
    create_txt_files(project_path, urls_to_crawl_file, crawled_urls_file)
    write_urls_to_file(base_urls, os.path.join(project_path, urls_to_crawl_file))


# Convert base_urls to a queue
url_queue = convert_urls_to_queue_from_config(base_urls)
logger.info('Base urls: %s', url_queue.queue)



state = CrawlerState(project_name, base_urls)
PageCrawler(state)


# Create worker threads (will die when main exits)
def create_crawler_threads():
    logger.debug("CREATING CRAWLER THREADS")
    for _ in range(num_worker_threads):
        t = threading.Thread(target=crawl_worker)
        t.daemon = True
        t.start()
    logger.debug("CRAWLER THREADS CREATED")


def crawl_worker():
    while True:
        url = url_queue.get()
        logger.info("Processing URL %s:", url)

        if ".onion" in url:
            logger.debug("ONION LINK FOUND")
            logger.info("Creating OnionCrawler")
            crawler = OnionCrawler(state, proxies=proxies)
        else:
            logger.debug("REGULAR LINK FOUND")
            logger.info("Creating PageCrawler")
            crawler = PageCrawler(state)

        crawler.crawl_page(threading.current_thread().name, url)
        url_queue.task_done()

        # Check if the file is empty and remove if necessary
        remove_empty_urls_file(os.path.join(project_path, urls_to_crawl_file))

   
def assign_jobs():
    for link in file_to_queue(urls_to_crawl_file).queue:
        url_queue.put(link)
    url_queue.join()
    start_crawling()


def start_crawling():
    logger.debug("CRAWLING STARTED")

    queued_links = file_to_queue(urls_to_crawl_file).queue

    if queued_links:
        logger.debug("QUEUED LINKS FOUND")
        logger.info(f"{len(queued_links)} links in the queue")
        assign_jobs()


create_crawler_threads()
start_crawling()
