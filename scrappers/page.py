import re
from typing import List


class PageScrapper:
    def __init__(self, html: str) -> None:
        self.html = html

    def find_onion_links(self) -> List[str]:
        if not self.html:
            return []

        onion_pattern = r"[a-zA-Z0-9]{16,56}\.onion"
        onion_addresses = re.findall(onion_pattern, self.html)
        return list(set(onion_addresses))
