from app.util.utils import logger
from app.crawler.serp_crawler import serp_crawler


@logger
def subject_serp_crawler(subject, query):
    if query is None or query == "":
        query = f'{subject} timeline'
        # query = f'{subject} chronology'
        # query = f'{subject} history'

    serp_crawler(subject, query)
    return



