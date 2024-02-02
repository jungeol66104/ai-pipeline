from app.crawler.serp_crawler import serp_crawler
from app.util.utils import add_to_queue, read_storage_file, get_text_batches, reset, check_temporary_db, check_queue


def run_sub():
    # add_to_queue({'subject': 'Tsai Ing_wen'})
    reset()
    # check_temporary_db()
    # check_queue()
    # serp_crawler()
    return


if __name__ == "__main__":
    run_sub()
