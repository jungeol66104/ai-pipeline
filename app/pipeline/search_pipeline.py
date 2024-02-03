from app.ai.simaqian import simaqian
from app.ai.url_extractor import url_extractor
from app.crawler.subject_crawler import subject_crawler
from app.crawler.url_crawler import url_crawler
from app.db.uploaders import simaqian_uploader, url_uploader
from app.util.utils import read_storage_file, write_storage_file


def search_pipeline():
    while True:
        queue = read_storage_file('queue.json')
        if bool(queue) is False:
            break
        subject = queue[0]["subject"]
        print(f'\tSUBJECT: {subject}')

        subject_crawler(subject)
        url_extractor()
        url_uploader()
        url_crawler(subject)
        simaqian()
        simaqian_uploader()

        write_storage_file(queue[1:], 'queue.json')
    return
