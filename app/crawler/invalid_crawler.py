from app.util.utils import logger
from app.db.session import query_invalid_events_by_subject
from app.crawler.serp_crawler import serp_crawler


@logger
def invalid_crawler(subject):
    invalid_events = query_invalid_events_by_subject(subject)

    for invalid_event in invalid_events:
        serp_crawler(subject, f'{invalid_event["name"]} exact date')
        serp_crawler(subject, f'{invalid_event["name"]} timeline')
        serp_crawler(subject, f'{invalid_event["name"]} chronology')
    return



