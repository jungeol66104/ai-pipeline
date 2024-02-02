from app.util.utils import logger
from app.db.session import query_invalid_event_by_subject
from app.crawler.serp_crawler import serp_crawler


@logger
def invalid_crawler(invalid_event):
    serp_crawler(invalid_event["subject"], f'{invalid_event["name"]} {invalid_event["date"]} exact date')
    return



