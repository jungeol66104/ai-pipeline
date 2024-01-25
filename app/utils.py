import os
import json
import re
import spiceypy as spice
from functools import wraps
# refactoring: needed (make json interactions mor general)


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


# storage interactions
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


# global
def split_by_newline(text):
    texts = re.split(r'\r?\n|\r', text)
    filtered_texts = [text.strip() for text in texts if text != ""]
    return filtered_texts


def get_is_date_valid(input_string):
    pattern = re.compile(r'^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$')
    return bool(pattern.match(input_string))


def get_ephemeris_time(date):
    file_path = naif0012_tls_path
    spice.furnsh(file_path)

    return spice.str2et(convert_date(date))


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
