from app.utils import logger
from app.crawler.serp_crawler import serp_crawler


@logger
def subject_crawler(subject):
    serp_crawler(subject, 'exact date')
    serp_crawler(subject, 'timeline')
    serp_crawler(subject, 'chronology')
    return



