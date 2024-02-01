import requests
from bs4 import BeautifulSoup
from app.util.utils import get_token_limit, read_storage_file, write_storage_file, logger, split_by_newline


@logger
def url_crawler():
    urls = read_storage_file('url.json')
    target_url = urls[0]
    response = requests.get(target_url["url"])

    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('body')
    text = body.get_text()
    texts = split_by_newline(text)

    raw_data = read_storage_file('raw_data.json')
    raw_data.append({"subject": target_url["subject"], "token_limit": get_token_limit(texts), "texts": texts})

    write_storage_file(raw_data, 'raw_data.json')
    target_url["is_completed"] = True
    write_storage_file(urls, 'url.json')
    return
