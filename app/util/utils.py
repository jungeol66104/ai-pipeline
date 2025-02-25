import os
import re
import json
import time
import tiktoken
import spiceypy as spice
from urllib.parse import urlparse, unquote
from functools import wraps


dir_util = os.path.dirname(os.path.realpath(__file__))
dir_app = os.path.join(dir_util, '../')
dir_pipeline = os.path.join(dir_app, '../')
naif0012_tls_path = os.path.join(dir_pipeline, 'kernel', 'naif0012.tls')


# decorators
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\t{func.__name__} start.")
        start_time = time.time()
        output_data = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\t{func.__name__} complete. ({elapsed_time})")
        return output_data

    return wrapper


# file interaction
def read_storage_file(file, subdirectory=None):
    file_path = os.path.join(dir_app, '../storage', file) if not subdirectory else os.path.join(dir_util, f'../storage/{subdirectory}', file)
    with open(file_path, 'r', encoding='utf-8') as file:
        result = json.load(file)
    return result


def write_storage_file(data, file, subdirectory=None):
    file_path = os.path.join(dir_app, '../storage', file) if not subdirectory else os.path.join(dir_util, f'../storage/{subdirectory}', file)
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
    if len(key_path) == 0:
        if isinstance(value, list):
            result.extend(value)
        else:
            result.append(value)
    else:
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

add_to_queue = lambda value: modify_storage_file_list('', value, 'queue.json')


def reset():
    temporary = {
        "main_subject": '',
        "db": {
            "serp_url":[],
            "timeline": [],
            "event": [],
            "event_timeline": [],
            "invalid_events": [],
            "training_set": []
        }
    }
    write_storage_file(temporary, 'temporary.json')
    write_storage_file([], 'raw_data.json')
    return


def check_temporary_db():
    print('\n\tTEMPORARY DB')
    temporary = read_storage_file('temporary.json')
    db_keys = temporary["db"].keys()

    for key in db_keys:
        print(f"\t{key}: ", len(temporary["db"][key]))
    print('')
    return


def check_queue():
    print('\n\tQUEUE')
    queue = read_storage_file('queue.json')
    print(f"\tqueue: ", len(queue))
    print('\n')
    return


def check_raw_data():
    print('\n\tRAW DATA')
    raw_data = read_storage_file('raw_data.json')
    print(f"\tsubjects: ", [raw_datum["subject"] for raw_datum in raw_data])
    print('\n')
    return


# utils
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
        texts = texts[last_index+1:]
    return text_batches


def get_token_limit(texts):
    token_limit = 500
    num_of_tokens_list = []
    try:
        for text in texts:
            num_of_tokens = len(tiktoken.get_encoding("cl100k_base").encode(text))
            num_of_tokens_list.append(num_of_tokens)
        token_limit = max(max(num_of_tokens_list), int(sum(num_of_tokens_list)/len(num_of_tokens_list)*10))
        return token_limit
    except Exception as e:
        print(e)
        return token_limit


def num_tokens_from_string(string, encoding_name):
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_url_existence(subject):
    urls = read_storage_file('url.json')
    target_url = next((url for url in urls if url.get("subject") == subject), None)
    url_existence = False if target_url is None else True
    return url_existence


def split_by_newline(text):
    texts = re.split(r'\r?\n|\r', text)
    filtered_texts = [text.strip() for text in texts if text != ""]
    filtered_texts = [filtered_text for filtered_text in filtered_texts if filtered_text != ""]
    return filtered_texts


def get_is_date_valid(input_string):
    try:
        pattern = re.compile(r'^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$')
        return bool(pattern.match(input_string))
    except Exception as e:
        print("Error string: ", input_string)
        print(f"Error occurred: {e}")
        return False


def get_ephemeris_time(date):
    try:
        file_path = naif0012_tls_path
        spice.furnsh(file_path)
        return spice.str2et(convert_date(date))
    except Exception as e:
        print(e)
        return None


def convert_date(date):
    parts = []
    if date.startswith("-"):
        parts.append(date)
    else:
        parts = date.split("-")

    if len(parts) != 3:
        parts.append(1)
        parts.append(1)

    year = parts[0]
    month = parts[1]
    day = parts[2]

    if year.startswith("-"):
        year = year[1:]
        era = "B.C."
    else:
        era = "A.D."

    converted_date = f"{year} {era} {month}-{day} 00:00"

    return converted_date


def separate_events_by_validity(raw_events):
    valid_raw_events = []
    invalid_events = []

    for i, event in enumerate(raw_events):
        # for string events, just dismiss it
        if isinstance(event, str):
            modify_storage_file_list('', {"str_event": event}, 'errors.json')
            continue
        for key, value in event.items():
            if isinstance(value, list):
                if value:
                    event[key] = value[0]
                else:
                    event[key] = 'None'

        if "subject" not in event:
            event["subject"] = "None"
            is_valid = False
        elif "date" in event:
            is_valid = get_is_date_valid(event["date"])
        else:
            event["date"] = "None"
            is_valid = False

        if is_valid:
            valid_raw_events.append(event)
        else:
            invalid_events.append(event)

    return {"valid_raw_events": valid_raw_events, "invalid_events": invalid_events}


def is_wikipedia_url(url):
    wikipedia_patterns = [
        "https://en.wikipedia.org/wiki/",
        "https://www.wikipedia.org/wiki/",
    ]
    return any(pattern in url for pattern in wikipedia_patterns)


def get_wikipedia_title_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_components = path.split("/")
    last_component = path_components[-1]
    title = unquote(last_component).replace('_', ' ')
    return title


def is_black_listed_url(url):
    black_list_patterns = [
        "https://timeline.vg/"
        "https://www.facebook.com/",
        "https://www.instagram.com/",
        "https://twitter.com/",
        "https://x.com/",
        "https://www.linkedin.com/",
        "https://www.snapchat.com/",
        "https://www.pinterest.com/",
        "https://www.tumblr.com/",
        "https://www.youtube.com/",
        "https://www.whatsapp.com/",
        "https://www.amazon.com/",
        "https://www.alibaba.com/",
        # "https://www.timetoast.com/",
        "https://www.shopify.com/",
        "https://www.ebay.com/",
        "https://www.walmart.com/",
        "https://play.google.com/",
        "https://apps.apple.com/",
        "https://www.youtube.com/",
        "https://about.fb.com/",
        "https://transparency.fb.com/",
        "https://www.researchgate.net/",
        "https://support.microsoft.com/",
        "https://www.imdb.com/"
    ]
    return any(pattern in url for pattern in black_list_patterns)


def is_pdf_url(url):
    return url.lower().endswith('.pdf') or '/pdf/' in url.lower()
