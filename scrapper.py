import re
from typing import List
from file_manager import write_urls_to_file
from url_manager import add_http_prefix
from log_config import logger

class PageScrapper:
    def __init__(self, html: str):
        self.html = html

    def find_onion_links(self) -> List[str]:
        if not self.html:
            return []

        onion_pattern = r'[a-zA-Z0-9]{16,56}\.onion'
        onion_addresses = re.findall(onion_pattern, self.html)
        return list(set(onion_addresses))

    def save_onion_addresses(self, onion_addresses: List[str], file_name: str):
        if onion_addresses:
            logger.info(f'Saving to ... {file_name}')

            formatted_addresses = [add_http_prefix(address) + '\n' for address in onion_addresses]
            write_urls_to_file(formatted_addresses, file_name)
            logger.info(f'All the unique onion addresses are written to the file {file_name}')
        else:
            logger.info("No .onion address found on this website")

