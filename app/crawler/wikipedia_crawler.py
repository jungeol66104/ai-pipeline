import os
import json
import re
import wikipediaapi
# refactoring: clear

dir_crawler = os.path.dirname(os.path.realpath(__file__))
dir_pipeline = os.path.join(dir_crawler, '../../')
raw_data_storage_json_path = os.path.join(dir_pipeline, 'storage', 'raw_data.json')


def wikipedia_crawler(title):
    wiki = wikipediaapi.Wikipedia('testBot/0.0', 'en')
    text = wiki.page(title).text
    new_raw_data_texts = split_by_newline(text)

    with open(raw_data_storage_json_path, 'r', encoding='utf-8') as file:
        original_raw_data = json.load(file)

    new_raw_data = original_raw_data[:]
    index, raw_datum = next(((index, item) for index, item in enumerate(new_raw_data) if item.get("title") == title), (None, None))

    if raw_datum is not None:
        new_raw_data[index]["texts"].extend(new_raw_data_texts)
    else:
        new_raw_data.append({"title": title, "texts": new_raw_data_texts})

    with open(raw_data_storage_json_path, 'w', encoding='utf-8') as file:
        json.dump(new_raw_data, file, ensure_ascii=False, indent=2)
    print('\twikipedia_crawler complete')

def split_by_newline(text):
    texts = re.split(r'\r?\n|\r', text)
    filtered_texts = [text.strip() for text in texts if text != ""]
    return filtered_texts