from fake_useragent import UserAgent
import requests
import random
import re


def Scrapper():


    query = 'comic book'

    if ' ' in query:
        query = query.replace(' ','+')

    url = 'https://ahmia.fi/search/q={}'.format(query) 

    ua_list = UserAgent()

    ua = ua_list.random

    headers = {'User-Agent': ua}
    print(headers)

    request = requests.get(url, headers=headers)
    print('request: {}'.format(request))
    html = request.content.decode('utf-8')

    def find_links(content):

        pattern = r'[a-zA-Z0-9]{16,56}\.onion'
        onion_addresses = re.findall(pattern, html)

        # Remove duplicates by converting the list to a set and then back to a list
        onion_addresses = list(set(onion_addresses))

        print('Found unique onion addresses: {}'.format(onion_addresses))

        if onion_addresses:
            n = random.randint(1, 9999)

            file_name = 'sites{}.txt'.format(str(n))
            print('Saving to ...', file_name)

            with open(file_name, 'w') as f:
                for onion_address in onion_addresses:
                    f.write(f'http://{onion_address}' + '\n')

            print('All the unique onion addresses are written to the file ', file_name)

        else:
            print("No .onion links found in this website")

    if request.status_code == 200:
        print('Request went through. \n')
        find_links(html)


Scrapper()

