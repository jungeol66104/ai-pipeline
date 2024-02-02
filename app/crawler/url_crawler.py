import os
import requests
from dotenv import load_dotenv
from app.db.session import query_serp_urls_by_subject, complete_serp_urls_by_id
from app.util.utils import get_token_limit, read_storage_file, write_storage_file, logger, split_by_newline


load_dotenv()
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")


@logger
def url_crawler(subject):
    serp_urls = query_serp_urls_by_subject(subject)
    raw_data = read_storage_file('raw_data.json')

    for serp_url in serp_urls:
        proxies = {
            "https": f"scraperapi.country_code=us.device_type=desktop:{SCRAPER_API_KEY}@proxy-server.scraperapi.com:8001"
        }
        response = requests.get(serp_url, proxies=proxies, verify=False)
        text = response.text
        texts = split_by_newline(text)
        raw_data.append({"subject": subject, "token_limit": get_token_limit(texts), "texts": texts})

    write_storage_file(raw_data, 'raw_data.json')
    complete_serp_urls_by_id([serp_url["id"] for serp_url in serp_urls])
    return
