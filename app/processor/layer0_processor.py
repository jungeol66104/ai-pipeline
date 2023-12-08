import json
import os
import tiktoken
# refactoring: clear

dir_processor = os.path.dirname(os.path.realpath(__file__))
dir_pipeline = os.path.join(dir_processor, '../../')
raw_data_storage_json_path = os.path.join(dir_pipeline, 'storage', 'raw_data_storage.json')
temp_storage_json_path = os.path.join(dir_pipeline, 'storage', 'temp_storage.json')


def layer0_processor():
    with open(raw_data_storage_json_path, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)

    raw_datum = raw_data[0]
    # raw_data for iteration, new_raw_data for mutation
    new_raw_data = raw_data[:]
    new_raw_datum = new_raw_data[0]
    used_raw_datum_texts = []
    text_packet = {"title": raw_datum["title"], "text": ""}

    # limit number of tokens to 2500
    count_tokens = 0
    for index, text in enumerate(raw_datum["texts"]):
        count_tokens += num_tokens_from_string(text, "cl100k_base")
        if count_tokens <= 2500:
            target_text = new_raw_datum["texts"].pop(0)
            text_packet["text"] += target_text
            used_raw_datum_texts.append(target_text)
        else:
            break

    end = True if len(new_raw_datum["texts"]) == 0 else False

    # commit changes to storages
    with open(raw_data_storage_json_path, 'w', encoding='utf-8') as file:
        json.dump(new_raw_data, file, indent=2)
    with open(temp_storage_json_path, 'w', encoding='utf-8') as file:
        json.dump(used_raw_datum_texts, file, indent=2)

    return [end, text_packet]


def num_tokens_from_string(string, encoding_name):
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
