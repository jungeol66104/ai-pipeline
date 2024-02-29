import json
from app.crawler.serp_crawler import serp_crawler
from app.util.utils import add_to_queue, read_storage_file, get_text_batches, reset, check_temporary_db, check_queue, \
    get_wikipedia_title_from_url, check_raw_data, get_ephemeris_time


def run_sub():
    # add_to_queue({'subject': "Tesla", 'query': ""})
    # reset()
    # check_temporary_db()
    # check_queue()
    # check_raw_data()
    # serp_crawler()
    return


if __name__ == "__main__":
    run_sub()
