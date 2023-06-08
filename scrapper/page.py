import re
from typing import List


class PageScrapper:
    """
    PageScrapper is a class for extracting onion links from HTML content.
    """
    def __init__(self, html: str) -> None:
        """
        Initializes PageScrapper with HTML content to be scrapped.
        
        :param html: A string containing the HTML content.
        """
        self.html = html

    def find_onion_links(self) -> List[str]:
        """
        Finds and returns a list of unique .onion links from the HTML content.
        
        :return: A list of unique .onion links.
        """
        if not self.html:
            return []

        onion_pattern = r"[a-zA-Z0-9]{16,56}\.onion"
        onion_addresses = re.findall(onion_pattern, self.html)
        return list(set(onion_addresses))
