import os
import uuid
import threading

from threading import Lock
from utils.log_config import logger
from crawlers.state import CrawlerState

from fake_useragent import UserAgent


file_write_lock = threading.Lock()


class BaseCrawler:
    def __init__(self, state: CrawlerState):
        self.state = state
        self.headers = self.get_random_headers()
        self.lock = Lock()

    @staticmethod
    def get_random_headers():
        user_agents_list = UserAgent()
        user_agent = user_agents_list.random
        return {"User-Agent": user_agent}

    def crawl_page(self, thread_name, page_url):
        print(f'crawling page_url: {page_url}')

        logger.info(thread_name + " is now crawling " + page_url)
        logger.info(
            "Queue "
            + str(self.state.crawl_queue.qsize())
            + " | Crawled  "
            + str(len(self.state.crawled_domains))
        )
        html_content, found_links = self.fetch_pages(page_url)
        #print(f'htmlcontent: {html_content}')
        #print('------------------------------------------------------------------')
        #print('------------------------------------------------------------------')
        #print(f'found list: {found_links}')

        self.state.add_links_to_queue(found_links) # Remove this line
        if html_content is not None:
            filename = f"{uuid.uuid4()}.html"
            #filename = page_url.replace("http://", "").replace(".onion", "") + ".html"
            

            # Save HTML before removing URL from the queue
            self.save_html_content(filename, html_content)

        self.state.add_links_to_queue(found_links)
        # Protect the update with a lock
        with self.lock:  
            self.state.crawled_domains.add(page_url)

    def save_html_content(self, page_url, html_content):
        # Generate a valid file name from the URL
        file_path = os.path.join(
            self.state.project_directory, self.state.project_name, page_url)

        # Write HTML content to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

    def fetch_pages(self):
        raise NotImplementedError()
