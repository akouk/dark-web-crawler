import requests

class Pagecrawler:
    def __init__(self, base_url: str):
        self.url = base_url

        self.headers = self.get_random_headers()
        self.page_content = self.get_pages_html()

    @staticmethod
    def get_random_headers():
        from fake_useragent import UserAgent
        user_agents_list = UserAgent()
        user_agent = user_agents_list.random
        return {'User-Agent': user_agent}
    
    def get_pages_html(self):
        request = requests.get(self.url, headers=self.headers)
        if request.status_code == 200:
            print('Request went through. \n')
            return request.content.decode('utf-8')
        return None