import json
import os
import tiktoken
from functools import wraps
from app.utils import num_tokens_from_string


dir_app = os.path.dirname(os.path.realpath(__file__))
dir_pipeline = os.path.join(dir_app, '../')
naif0012_tls_path = os.path.join(dir_pipeline, 'kernel', 'naif0012.tls')


# decorators
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\t{func.__name__} started.")
        output_data = func(*args, **kwargs)
        print(f"\t{func.__name__} complete.")
        return output_data

    return wrapper


# file interaction
def read_storage_file(file, subdirectory=None):
    file_path = os.path.join(dir_app, '../storage', file) if not subdirectory else os.path.join(dir_app, f'../storage/{subdirectory}', file)
    with open(file_path, 'r', encoding='utf-8') as file:
        result = json.load(file)
    return result


def write_storage_file(data, file, subdirectory=None):
    file_path = os.path.join(dir_app, '../storage', file) if not subdirectory else os.path.join(dir_app, f'../storage/{subdirectory}', file)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return


def modify_storage_file_value(key_path, value, file, subdirectory=None):
    result = read_storage_file(file, subdirectory)
    keys = [prop.strip() for prop in key_path.split('/')]
    target = result

    for key in keys[:-1]:
        if key in target:
            target = target[key]
    target[keys[-1]] = value
    write_storage_file(result, file, subdirectory)
    return


def modify_storage_file_list(key_path, value, file, subdirectory=None):
    result = read_storage_file(file, subdirectory)
    keys = [prop.strip() for prop in key_path.split('/')]
    target = result

    for key in keys[:-1]:
        if key in target:
            target = target[key]
    if isinstance(value, list):
        target[keys[-1]].extend(value)
    else:
        target[keys[-1]].append(value)
    write_storage_file(result, file, subdirectory)
    return


# utils
def get_text_packet(raw_datum):
    text_packet = {"subject": raw_datum["subject"], "text": raw_datum[0]}
    return text_packet


def get_text_batches(raw_datum):
    texts, token_limit = raw_datum["texts"], raw_datum["token_limit"]

    text_batches = []
    while len(texts) > 0:
        text_batch = ""
        count_tokens = 0
        last_index = 0
        for index, text in enumerate(texts):
            count_tokens += num_tokens_from_string(text, "cl100k_base")
            if count_tokens <= token_limit:
                text_batch += f"{text}\n\n"
                last_index = index
            else:
                break
        text_batches.append(text_batch)
        texts = texts[:last_index+1]
    return text_batches


def calculate_token_limit(texts):
    num_of_tokens_list = []
    for text in texts:
        num_of_tokens = len(tiktoken.get_encoding("cl100k_base").encode(text))
        num_of_tokens_list.append(num_of_tokens)
    return max(max(num_of_tokens_list), int(sum(num_of_tokens_list)/len(num_of_tokens_list)*10))


def get_url_existence(subject):
    urls = read_storage_file('url.json')
    target_url = next((url for url in urls if url.get("subject") == subject), None)
    url_existence = False if target_url is None else True
    return url_existence


# processors
def simaqian_processor(events, timelines):

    return
