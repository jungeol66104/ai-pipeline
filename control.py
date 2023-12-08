import os
import json
from dotenv import load_dotenv

dir_pipeline = os.path.dirname(os.path.realpath(__file__))
raw_data_storage_json_path = os.path.join(dir_pipeline, 'storage', 'raw_data_storage.json')


def reset_raw_data_storage():
    with open(raw_data_storage_json_path, 'w', encoding='utf-8') as file:
        json.dump([], file)


def check_dotenv():
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    print(url)

check_dotenv()