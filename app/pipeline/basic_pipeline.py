from app.ai.simaqian import simaqian
from app.ai.url_extractor import url_extractor
from app.crawler.subject_crawler import subject_crawler
from app.crawler.url_crawler import url_crawler
from app.db.uploader import url_uploader
from app.processor.utils import get_url_existence


def basic_pipeline(subject):
    subject_crawler(subject)
    url_extractor()
    url_uploader()
    while get_url_existence(subject):
        url_crawler()
        simaqian()

    return
