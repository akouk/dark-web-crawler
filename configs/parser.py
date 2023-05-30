import queue


def convert_urls_to_queue_from_config(base_urls):
    url_queue = queue.Queue()

    for url in base_urls:
        url_queue.put(url)

    return url_queue
