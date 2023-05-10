import requests
import random
import string
import re

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

#url = 'https://onionlandsearchengine.com/search?q=comic+book'
url = 'https://hidden.wiki/?s=comic+book'


def tor_searcher(url):

    def get_tor_session():
        session = requests.session()

        session.proxies = proxies

        return session
    
    session = get_tor_session()

    print('Getting url: ', url)

    try:
        result = session.get(url, timeout=30).text
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error for {url}: {e}")
        return None
    
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))

    with open(f'{file_name}.txt', 'w+', encoding='utf-8') as new_thing:
        new_thing.write(result)

    return result
