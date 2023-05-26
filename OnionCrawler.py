import requests
from PageCrawler import Pagecrawler


class OnionCrawler:
    def __init__(self, url, proxies):
        self.url = url
        self.proxies = proxies

    def get_tor_session(self):
        session = requests.session()
        session.proxies = self.proxies
        return session
        
    def search(self):
        session = self.get_tor_session()
        print('Getting url:', self.url)
        pagecrawler = Pagecrawler(self.url)  # Create an instance of Pagecrawler
        headers = pagecrawler.headers  # Get random headers

        try:
            response = session.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception if request was not successful
            print('Request went through.\n')
            result = response.text
            return result
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error for {self.url}: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
