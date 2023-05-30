import yaml


def read_config_file(config_file_path):
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)

    return config


def get_config_values(config):
    project_directory = config['project_directory']
    project_name = config['project_name']
    base_urls = config['base_urls']
    num_worker_threads = config['num_worker_threads']
    proxies = config['proxies']

    return (
        project_directory,
        project_name,
        base_urls,
        num_worker_threads,
        proxies,
    )
