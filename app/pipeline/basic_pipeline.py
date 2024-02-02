from app.ai.simaqian import simaqian
from app.ai.url_extractor import url_extractor
from app.crawler.invalid_crawler import invalid_crawler
from app.crawler.subject_crawler import subject_crawler
from app.crawler.url_crawler import url_crawler
from app.db.uploaders import url_uploader, simaqian_uploader
from app.util.utils import get_url_existence


def basic_pipeline(subject):
    subject_crawler(subject)
    url_extractor()
    url_uploader()
    while get_url_existence(subject):
        url_crawler(subject)
        simaqian()
        simaqian_uploader()
        # end here for now
        invalid_crawler(subject)
        url_extractor()
        url_uploader()
    return
