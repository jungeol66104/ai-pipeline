import os
import json
import requests
from dotenv import load_dotenv
from app.util.utils import get_token_limit, read_storage_file, write_storage_file, logger, modify_storage_file_list

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


@logger
def serp_crawler(subject, query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query,
        "num": 10
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    response_text = response.text
    keys = response_json.keys()
    texts = [response_text]

    serp_keys = read_storage_file('serp_keys.json')
    serp_keys.extend(list(keys))
    serp_keys = list(set(serp_keys))
    write_storage_file(serp_keys, 'serp_keys.json')

    modify_storage_file_list('', {"type": "serp", "token_limit": get_token_limit(texts), "subject": subject, "texts": texts}, 'raw_data.json')
    return
