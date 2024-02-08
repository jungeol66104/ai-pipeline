import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from app.crawler.wikipedia_crawler import wikipedia_crawler
from app.db.session import query_serp_urls_by_subject, complete_serp_urls_by_id
from app.util.utils import get_token_limit, read_storage_file, write_storage_file, logger, split_by_newline, \
    is_wikipedia_url, get_wikipedia_title_from_url, is_black_listed_url, is_pdf_url

load_dotenv()
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")


@logger
def url_crawler(subject):
    serp_urls = query_serp_urls_by_subject(subject)
    serp_urls_not_completed = [serp_url for serp_url in serp_urls if serp_url.is_completed == 0]
    raw_data = read_storage_file('raw_data.json')

    for serp_url in serp_urls_not_completed:
        # skip black listed urls
        if is_black_listed_url(serp_url.url):
            continue

        # skip pdf for now
        if is_pdf_url(serp_url.url):
            continue

        # treat wikipedia with different logic
        if is_wikipedia_url(serp_url.url):
            title = get_wikipedia_title_from_url(serp_url.url)
            wikipedia_crawler(title)
            continue

        proxies = {
            "https": f"http://scraperapi.country_code=us.device_type=desktop:{SCRAPER_API_KEY}@proxy-server.scraperapi.com:8001"
        }
        response = requests.get(serp_url.url, proxies=proxies, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.body

        if body is not None:
            text = body.get_text()
        else:
            text = soup.get_text()

        texts = split_by_newline(text)
        raw_data.append({"subject": subject, "token_limit": get_token_limit(texts), "texts": texts})

    write_storage_file(raw_data, 'raw_data.json')
    complete_serp_urls_by_id([serp_url.id for serp_url in serp_urls_not_completed])
    return
