import requests
import random
import string

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
        result = session.get(self.url, timeout=30).text
        file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        with open(f'{file_name}.txt', 'w+', encoding='utf-8') as new_thing:
            new_thing.write(result)
