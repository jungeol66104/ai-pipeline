from app.ai.simaqian import simaqian
from app.ai.url_extractor import url_extractor
from app.crawler.invalid_crawler import invalid_crawler
from app.crawler.url_crawler import url_crawler
from app.db.session import query_invalid_event_by_subject, complete_invalid_event_by_id
from app.db.uploaders import url_uploader, simaqian_uploader


def invalid_pipeline(subject):
    count = 0
    while True:
        invalid_event = query_invalid_event_by_subject(subject)
        if invalid_event is None or count == 1:
            break

        # invalid_crawler(invalid_event)
        # url_extractor()
        # url_uploader()
        url_crawler(subject)
        simaqian()
        simaqian_uploader()

        complete_invalid_event_by_id(invalid_event["id"])
        count += 1
    return