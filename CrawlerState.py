from file_manager import *

class CrawlerState:
    def __init__(self, project_name, base_url):
        self.project_name = project_name
        self.base_url = base_url
        self.links_to_crawl_file = self.project_name + '/links_to_crawl.txt'
        self.crawled_links_file = self.project_name + '/crawled_links.txt'
        self.initialize_crawler()

    def initialize_crawler(self):
        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        self.links_to_crawl = file_to_queue(self.links_to_crawl_file)
        self.crawled_links = file_to_queue(self.crawled_links_file)

    def add_links_to_queue(self, links):
        for url in links:
            if url in self.links_to_crawl.queue or url in self.crawled_links.queue:
                continue
            self.links_to_crawl.put(url)

    def update_files(self):
        queue_to_file(self.links_to_crawl, self.links_to_crawl_file)
        queue_to_file(self.crawled_links, self.crawled_links_file)
