# Dark-Web-Crawler
## Description

Dark-Web-Crawler is a Python-based project that crawls and scrapes .onion websites. This project consists of various modules which are used to efficiently manage the crawling process, while maintaining the state and ensuring that links are visited only once.


## Requirements
Ensure you have installed the followings on your system:
- Python 3.7 or newer
- pip
- venv


## Getting Started

Clone this repository to your local machine.

```git clone https://github.com/akouk/dark-web-crawler.git```

Navigate to the cloned repository.

```cd <project_directory>```

## Configuration

Before you can run the project, you need to configure it according to your needs.

You can modify the config.yaml file for your configuration. This YAML file is structured as follows:

- `project` : This section includes name and directory that specifies the project's name and the directory where the project will be located.
- `base_urls` : Specify the list of URLs from where you want to start the crawling process.
- `num_worker_threads` : Specify the number of threads that you want to run for crawling.
- `request` : This section includes timeout in seconds for the requests.
- `proxies`: Specify the proxies to be used for requests when crawling onion websites.

## Setup and Running

After updating the config.yaml file, set up the virtual environment, install the required dependencies and run the project using the Makefile:


```make setup```

This will initiate the crawler, and you will see the crawled pages and other information on the console.

To run the project, you can use the following command.
```make run```


## Disclaimer

This project is meant for educational purposes only. Do not use it for illegal activities. Be aware of the potential legal and ethical implications when using a web crawler.