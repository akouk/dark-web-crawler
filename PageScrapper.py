import re
from html_manager import add_http_prefix_in_the_onion_address

class PageScrapper:
    def __init__(self, html):
        self.html = html

    def find_onion_links(self):
        if not self.html:
            return []

        onion_pattern = r'[a-zA-Z0-9]{16,56}\.onion'
        onion_addresses = re.findall(onion_pattern, self.html)
        return list(set(onion_addresses))

    def save_onion_addresses(self, onion_addresses):
        if onion_addresses:
            file_name = 'onion_link_websites.txt'
            print(f'Saving to ... {file_name}')

            with open(file_name, 'w') as f:
                for onion_address in onion_addresses:
                    address_link = add_http_prefix_in_the_onion_address(onion_address)
                    f.write(address_link + '\n')

            print(f'All the unique onion addresses are written to the file {file_name}')
        else:
            print("No .onion address found on this website")