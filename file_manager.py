from typing import List
from queue import Queue
from log_config import logger
import os
import sys

# NEW ---------------------------------------------------
def create_project_directory(project_directory, project_name):
    if project_directory and project_name:
        if os.path.exists(project_directory):
            project_path = os.path.join(project_directory, project_name)
            if not os.path.exists(project_path):
                os.makedirs(project_path)
                logger.info('Created project directory: %s.', project_path)
                return project_path
            else:
                logger.info('Project directory already exists: %s.', project_path)
                sys.exit("Terminating the program.")
        else:
            logger.info('Invalid project directory: %s.', project_directory)
            sys.exit("Terminating the program.")
    else:
        logger.info("Invalid project configuration")
        sys.exit("Terminating the program.")

# NEW --------------------------------------------------------------------
def create_txt_files(project_path, urls_to_crawl_file, crawled_urls_file):
    create_file_in_project(project_path, urls_to_crawl_file)
    create_file_in_project(project_path, crawled_urls_file)



# NEW ----------------------------------------------
def create_file_in_project(project_path, file_name):
    file_path = os.path.join(project_path, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass

# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        logger.info('Creating directory ' + directory)
        os.makedirs(directory)

# NEW -----------------------------------
def create_file_in_project(project_path, file_name):
    file_path = os.path.join(project_path, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass

# NEW -----------------------------------------------
def create_results_data_directory(project_directory, results_data_name):
    if project_directory and results_data_name:
        results_data_path = os.path.join(project_directory, results_data_name)
        os.makedirs(results_data_path)
        print('Created results data directory:', results_data_path)
    else:
        logger.info('Invalid results data configuration')
        sys.exit("Terminating program.")


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    links_to_crawl = os.path.join(project_name , 'links_to_crawl.txt')
    crawled_links = os.path.join(project_name,'crawled_links.txt')
    if not os.path.isfile(links_to_crawl):
        write_file(links_to_crawl, base_url)
    if not os.path.isfile(crawled_links):
        write_file(crawled_links, '')




# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()



def read_from_file(filename: str) -> List[str]:
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        logger.error('The file %s does not exists.', filename)
        return []
    except IOError as e:
        logger.error('An error occurred while reading the file %s. Error: %s', filename, str(e))
        return []

# NEW --------------
def write_urls_to_file(urls: List[str], filename: str):
    try:
        with open(filename, 'w') as f:
            for url in urls:
                f.write(url + '\n')
    except IOError as e:
        logger.error('An error occurred while writing to the file %s. Error: %s', filename, str(e))

def write_html_file(result: str, filename: str):
    try:
        with open(filename, 'w+', encoding='utf-8') as onion_html:
            onion_html.write(result)
            logger.info(f'{filename} wrote successfully!')
    except IOError as e:
        logger.error('An error occurred while writing to the file %s. Error: %s', filename, str(e))

# Convert a file to a queue
def file_to_queue(file_name):
    results = Queue()

    try:
        with open(file_name, 'rt') as f:
            for line in f:
                results.put(line.replace('\n', ''))
    except IOError as e:
        logger.error('An error occurred while reading the file %s. Error: %s', file_name, str(e))
    except Exception as e:
        logger.exception('An unexpected error occurred while converting from file to queue: %s.', str(e))
    return results

# Convert a queue to a file
def queue_to_file(links, file_name):
    try:
        with open(file_name, "w") as f:
            while not links.empty():
                f.write(links.get() + "\n")
    except IOError as e:
        logger.error('An error occurred while reading the file %s. Error: %s', file_name, str(e))
    except Exception as e:
        logger.exception('An unexpected error occurred while converting from queue to file: %s.', str(e))

# NEW ----------------------------------------------------------------
def remove_empty_urls_file(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        os.remove(file_path)
        logger.info('Deleted empty file: %s', file_path)