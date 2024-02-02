from app.ai.url_extractor import url_extractor
from app.crawler.invalid_crawler import invalid_crawler
from app.db.session import query_invalid_event_by_subject, complete_invalid_event_by_id
from app.db.uploaders import url_uploader


def invalid_pipeline(subject):
    while True:
        invalid_event = query_invalid_event_by_subject(subject)
        if invalid_event is None:
            break

        invalid_crawler(invalid_event)
        url_extractor()
        url_uploader()

        complete_invalid_event_by_id(invalid_event["id"])
    return