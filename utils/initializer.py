import os
import sys

from typing import List
from queue import Queue

from utils.log_config import logger


class Initializer:
    def __init__(
        self, 
        project_directory: str, 
        project_name: str,
        urls: List[str],
    ) -> None:
        if not os.path.exists(project_directory):
            logger.info('Invalid project directory: %s.', project_directory)
            sys.exit("Terminating the program.")
        
        self.project_path = os.path.join(project_directory, project_name)
        if os.path.exists(self.project_path):
            logger.info('Project directory already exists: %s.', self.project_path)
            sys.exit("Terminating the program.")

        os.makedirs(self.project_path)
        logger.info('Created project directory: %s.', self.project_path)

        self.crawl_queue = Queue()
        
        for url in urls:
            self.crawl_queue.put(url)
