from utilities.url_manager import rename_file
from utilities.file_manager import read_from_file, write_html_file
from web_utilities.crawler import PageCrawler, OnionCrawler
from web_utilities.scrapper import PageScrapper
import requests


proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def main():
    url = 'link'

    page_crawler = PageCrawler(url)
    page_content = page_crawler.fetch_pages()

    scraper = PageScrapper(page_content)
    onion_addresses = scraper.find_onion_links()
    print(f'Found unique onion addresses: {onion_addresses}')
    scraper.save_onion_addresses(onion_addresses)

    lines = read_from_file('onion_link_websites.txt')

    for line in lines:
        try:
            while True:
                tor_search = OnionCrawler(line, proxies=proxies)
                onion_page_content = tor_search.fetch_pages()

                if onion_page_content is not None:
                    filename = rename_file(line)
                    print(f'filename: {filename}')
                    write_html_file(onion_page_content, filename)
                else:
                    break

        except requests.exceptions.RequestException as e:
            print(f"Error occurred for {line}: {e}")
            continue


if __name__ == '__main__':
    main()