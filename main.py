from PageCrawler import Pagecrawler
from PageScrapper import PageScrapper
from OnionCrawler import OnionCrawler
from html_manager import *
import os
import requests

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def main():
    url = 'https://thehiddenwiki.org/'
    #url = 'https://duckduckgo.com/'
    #url = 'https://ahmia.fi/'
    request = Pagecrawler(url)
    page_contentent = request.page_content
    
    scraper = PageScrapper(page_contentent)
    onion_addresses = scraper.find_onion_links()
    print(f'Found unique onion addresses: {onion_addresses}')
    scraper.save_onion_addresses(onion_addresses)

    with open('onion_link_websites.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f] 

        for line in lines:

            try:
                tor_search = OnionCrawler(line, proxies=proxies)
                onion_page_content = tor_search.search()

                if onion_page_content is not None:
                    filename = rename_file(line)
                    #print(f'filename: {filename}')
                    write_html_file(onion_page_content, filename)
                else:
                    continue

            except requests.exceptions.RequestException as e:
                print(f"Error occurred for {line}: {e}")
                continue


if __name__ == '__main__':
    main()