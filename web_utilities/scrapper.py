import re
from typing import List
from utilities.file_manager import write_to_file
from utilities.url_manager import add_http_prefix

class PageScrapper:
    def __init__(self, html: str):
        self.html = html

    def find_onion_links(self) -> List[str]:
        if not self.html:
            return []

        onion_pattern = r'[a-zA-Z0-9]{16,56}\.onion'
        onion_addresses = re.findall(onion_pattern, self.html)
        return list(set(onion_addresses))

    def save_onion_addresses(self, onion_addresses: List[str], file_name: str = 'onion_link_websites.txt'):
        if onion_addresses:
            print(f'Saving to ... {file_name}')

            formatted_addresses = [add_http_prefix(address) + '\n' for address in onion_addresses]
            write_to_file(formatted_addresses, file_name)
            print(f'All the unique onion addresses are written to the file {file_name}')
        else:
            print("No .onion address found on this website")
