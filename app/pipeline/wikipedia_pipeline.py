from app.ai.simaqian import simaqian
from app.crawler.wikipedia_crawler import wikipedia_crawler
from app.db.uploaders import simaqian_uploader
from app.util.utils import read_storage_file, write_storage_file, logger


@logger
def wikipedia_pipeline():
    count = 0
    while count <= 1:
        queue = read_storage_file('queue.json')
        subject = queue[0]["subject"]
        print(f'SUBJECT: {subject}')

        wikipedia_crawler(subject)
        simaqian()
        simaqian_uploader()

        write_storage_file(queue[1:], 'queue.json')
        count += 1
    return
