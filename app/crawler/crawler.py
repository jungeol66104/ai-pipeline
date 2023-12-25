from app.crawler.wikipedia_crawler import wikipedia_crawler
from app.crawler.serp_crawler import serp_crawler


def crawler(crawling_model, crawling_target):
    if crawling_model == "wikipedia":
        wikipedia_crawler(crawling_target)
    elif crawling_model == "serp":
        serp_crawler(crawling_target)
    return
