from app.ai.simaqian import simaqian
from app.ai.url_extractor import url_extractor
from app.crawler.subject_serp_crawler import subject_serp_crawler
from app.crawler.subject_url_crawler import subject_url_crawler
from app.db.uploaders import simaqian_uploader, url_uploader
from app.util.utils import read_storage_file, modify_storage_file_value, write_storage_file, logger


@logger
def search_pipeline():
    count = 0
    while True:
        queue = read_storage_file('queue.json')
        if bool(queue) is False or count >= 1:
            break
        subject = queue[0]["subject"]
        query = queue[0]["query"]
        modify_storage_file_value('main_subject', subject, 'temporary.json')
        print(f'\tSUBJECT: {subject}')

        subject_serp_crawler(subject, query)
        url_extractor()
        url_uploader()
        subject_url_crawler(subject)
        simaqian()
        simaqian_uploader()
        # count += 1
        write_storage_file(queue[1:], 'queue.json')
    return
