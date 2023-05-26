import requests
from fake_useragent import UserAgent
import chardet

class Crawler:
    def __init__(self, url: str):
        self.url = url
        self.headers = self.get_random_headers()

    @staticmethod
    def get_random_headers():
        user_agents_list = UserAgent()
        user_agent = user_agents_list.random
        return {'User-Agent': user_agent}

    def fetch_pages(self):
        raise NotImplementedError("This method should be overridden.")


class PageCrawler(Crawler):
    def fetch_pages(self):
        request = requests.get(self.url, headers=self.headers)
        if request.status_code == 200:
            print('Request went through. \n')
            return request.content.decode('utf-8')
        return None


class OnionCrawler(Crawler):
    def __init__(self, url: str, proxies: dict):
        super().__init__(url)
        self.proxies = proxies

    def get_tor_session(self):
        session = requests.session()
        session.proxies = self.proxies
        return session

    def fetch_pages(self):
        session = self.get_tor_session()
        print('Getting url:', self.url)

        try:
            response = session.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()  # Raise exception if request was not successful
            print('Request went through.\n')

            # Detect character encoding using chardet
            #encoding = chardet.detect(response.content)['encoding']
            #result = response.content.decode(encoding)

            # Detect character encoding using chardet
            encoding = chardet.detect(response.content)['encoding']
            # solved issue: TypeError: decode() argument 'encoding' must be str, not None
            encoding = encoding or 'utf-8'  # Set default encoding to 'utf-8' if encoding is None
            result = response.content.decode(encoding)


            return result

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error for {self.url}: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
