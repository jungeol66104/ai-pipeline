import requests
from bs4 import BeautifulSoup

from app.processor.utils import calculate_token_limit
from app.utils import read_storage_file, write_storage_file, logger


@logger
def serp_crawler(subject, additive):
    target_url = f'https://www.google.com/search?q={subject.replace(" ", "+")} {additive}'
    response = requests.get(target_url)

    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('body')
    text = body.get_text()
    texts = [text]

    raw_data = read_storage_file('raw_data.json')
    raw_data.append({"type": "serp", "token_limit": calculate_token_limit(texts), "subject": subject, "texts": texts})

    write_storage_file(raw_data, 'raw_data.json')
    return
