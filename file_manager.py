import os


class FileManager:
    def __init__(self, project_name, base_url):
        self.project_name = project_name
        self.base_url = base_url

    def create_data_files(self):
        """Create queue and crawled files if they don't exist."""
        queue_file = os.path.join(self.project_name, 'queue.txt')
        crawled_file = os.path.join(self.project_name, 'crawled.txt')

        if not os.path.isfile(queue_file):
            self.write_file(queue_file, self.base_url)

        if not os.path.isfile(crawled_file):
            self.write_file(crawled_file, '')

    @staticmethod
    def write_file(path, data):
        """Create a new file and write data into it."""
        with open(path, 'w') as file:
            file.write(data)
