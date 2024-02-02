import os
import json
import requests
from dotenv import load_dotenv
from app.util.utils import get_token_limit, read_storage_file, write_storage_file, logger, modify_storage_file_list

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


@logger
def serp_crawler(subject=None, query=None):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    modify_storage_file_list()
    # raw_data = read_storage_file('raw_data.json')
    # raw_data.append({"type": "serp", "token_limit": get_token_limit(texts), "subject": subject, "texts": texts})
    # write_storage_file(raw_data, 'raw_data.json')
    return
