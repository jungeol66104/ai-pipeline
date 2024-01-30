from app.db.session import query_invalid_event_by_id
from app.utils import logger
from app.crawler.serp_crawler import serp_crawler


@logger
def invalid_crawler():
    invalid_event = query_invalid_event_by_id(1)
    serp_crawler(invalid_event.subject, 'exact date')
    serp_crawler(invalid_event.subject, 'timeline')
    serp_crawler(invalid_event.subject, 'chronology')
    return



