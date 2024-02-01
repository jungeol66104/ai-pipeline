from app.util.utils import logger
from app.crawler.serp_crawler import serp_crawler


@logger
def subject_crawler(subject):
    serp_crawler(subject, 'timeline')
    serp_crawler(subject, 'chronology')
    return



