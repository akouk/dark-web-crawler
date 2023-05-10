from PageCrawler import Pagecrawler
from PageScrapper import PageScrapper
#from OnionCrawler import OnionCrawler

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def main():
    url = 'my-link/'
    request = Pagecrawler(url)
    page_contentent = request.page_content
    scraper = PageScrapper(page_contentent)
    onion_addresses = scraper.find_onion_links()
    print(f'Found unique onion addresses: {onion_addresses}')
    scraper.save_onion_addresses(onion_addresses)

    #tor_search = OnionCrawler(url, proxies=proxies)



if __name__ == '__main__':
    main()