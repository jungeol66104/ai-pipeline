import tiktoken
from app.utils import read_storage_file, write_storage_file, modify_storage_file
# refactoring: clear


def layer1_processor():
    raw_data = read_storage_file('raw_data.json')

    raw_datum = raw_data[0]
    used_raw_datum_texts = []
    text_packet = {"subject": raw_datum["subject"], "text": ""}

    token_limit = 2500
    count_tokens = 0
    last_index = 0
    for index, text in enumerate(raw_datum["texts"]):
        count_tokens += num_tokens_from_string(text, "cl100k_base")
        if count_tokens <= token_limit:
            text_packet["text"] += text
            used_raw_datum_texts.append(text)
            last_index = index
        else:
            break

    raw_datum["texts"] = raw_datum["texts"][last_index + 1:]

    # commit changes to storages
    write_storage_file(raw_data, 'raw_data.json')
    modify_storage_file('used_raw_datum_texts', used_raw_datum_texts, 'temporary.json')

    return text_packet


def num_tokens_from_string(string, encoding_name):
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
