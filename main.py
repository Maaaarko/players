import os
import sys

from scrapy.crawler import CrawlerProcess

from players.spiders.wikipedia import WikipediaPlayerInfoSpider


def load_start_urls(file_path):
    with open(file_path, "r") as f:
        return [url.strip() for url in f.readlines()]


def start_process(file_path, output_file_path):
    start_urls = load_start_urls(file_path)

    db_connection_string = "host=localhost dbname=players user=postgres password=postgres"  # hardcoded for simplicity
    settings = {
        "OUTPUT_FILE": output_file_path,
        "DB_CONNECTION_STRING": db_connection_string,
        "ITEM_PIPELINES": {"players.pipelines.PlayersPipeline": 300},
    }

    process = CrawlerProcess(settings=settings)
    process.crawl(WikipediaPlayerInfoSpider, start_urls=start_urls)
    process.start()


if __name__ == "__main__":
    file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    start_process(file_path, output_file_path)
