import re
import os
import tiktoken
import PyPDF2
from app.utils import read_storage_file, write_storage_file, split_by_newline

dir_pipeline = os.path.dirname(os.path.realpath(__file__))


def read_data_txt(directory, file):
    file_path = os.path.join(dir_pipeline, 'data', directory, file)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def write_data_txt(directory, file, text):
    file_path = os.path.join(dir_pipeline, 'data', directory, file)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    return


def check_text_tokens(target):
    filtered_texts = target
    if isinstance(target, str):
        filtered_texts = split_by_newline(target)

    num_of_tokens_list = []
    for index, target in enumerate(filtered_texts):
        num_of_tokens = len(tiktoken.get_encoding("cl100k_base").encode(target))
        if num_of_tokens > 2500:
            print(f'Oh no, {num_of_tokens} tokens caught!')
        num_of_tokens_list.append(num_of_tokens)
    print("paragraph length: ", len(num_of_tokens_list))
    print("max number of tokens: ", max(num_of_tokens_list))
    print("recommended number of tokens: ", sum(num_of_tokens_list)/len(num_of_tokens_list)*10)
    return


def txt_space_remover(directory, file):
    text = read_data_txt(directory, file)
    text = text.replace('\n', '')
    write_data_txt(directory, file, text)
    return


def txt_organizer(directory, file, pattern, replace):
    text = read_data_txt(directory, file)
    text = text.replace('\n', '')
    text = re.sub(pattern, replace, text)
    write_data_txt(directory, file, text)
    return

def reset_raw_data():
    # raw_data = read_storage_file('raw_data.json')
    # used_raw_datum_texts = read_storage_file('temporary.json')["used_raw_datum_texts"]
    # raw_data[0]["texts"] = used_raw_datum_texts + raw_data[0]["texts"]
    write_storage_file([], 'raw_data.json')
    return

def check_keys_validity():
    temporary_db = read_storage_file('temporary.json')["db"]
    for timeline in temporary_db["timeline"]:
        if set(timeline.keys()) != {"id", "name"}:
            print("\tinvalid timeline: ", timeline)
    for event in temporary_db["event"]:
        if set(event.keys()) != {"id", "name", "date", "description", "ephemeris_time"}:
            print("\tinvalid event: ", event)
    for event_timeline in temporary_db["event_timeline"]:
        if set(event_timeline.keys()) != {"id", "event_id", "timeline_id", "importance"}:
            print("\tinvalid event_timeline: ", event_timeline)
    for timeline_translation in temporary_db["timeline_translation"]:
        if set(timeline_translation.keys()) != {"timeline_id", "language_code_id", "name"}:
            print("\tinvalid timeline_translation: ", timeline_translation)
    for event_translation in temporary_db["event_translation"]:
        if set(event_translation.keys()) != {"event_id", "language_code_id", "name", "description"}:
            print("\tinvalid event_translation: ", event_translation)
    for invalid_events in temporary_db["invalid_events"]:
        if set(invalid_events.keys()) != {"date", "name", "description", "subject", "importance"}:
            print("\tinvalid invalid_events: ", invalid_events)
    for fine_tuning_training_set in temporary_db["fine_tuning_training_set"]:
        if set(fine_tuning_training_set.keys()) != {"model", "input", "output"}:
            print("\tinvalid fine_tuning_training_set: ", fine_tuning_training_set)
    return


def reset_temporary():
    temporary = {
        "crawling_target": "",
        "used_raw_datum_texts": [],
        "db": {
            "url":[],
            "timeline": [],
            "event": [],
            "event_timeline": [],
            "invalid_events": [],
            "fine_tuning_training_set": []
        }
    }
    write_storage_file(temporary, 'temporary.json')
    return


def check_temporary_db():
    temporary = read_storage_file('temporary.json')
    db_keys = temporary["db"].keys()

    for key in db_keys:
        print(f"\t{key}: ", len(temporary["db"][key]))
    return


def pdf_to_text():
    with open('2008.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file, strict=False)

        text = ''
        for page in reader.pages:
            content = page.extract_text()
            text += content

    with open('2008.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(text)
    return


def txt_2008_organizer():
    # for 2008
    with open('2008.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    text = text.replace('\n', '')
    text = re.sub(
        r'(\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*,?\s*\w{3,9}\s*\d{1,2}?\s*,?\s*\d{1,4}\s*:)',
        r'\n\n\1', text)
    text = re.sub(
        r'(\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*,?\s*\d{1,2}?\s*\w{3,9}\s*,?\s*\d{1,4}\s*:)',
        r'\n\n\1', text)

    with open('2008.txt', 'w', encoding='utf-8') as file:
        file.write(text)

    return


def txt_afc_organizer():
    with open('raw_data_afc.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    text = text.replace('\n', '')

    pattern_section1 = r'(.+?)<another page>'
    matches_section1 = re.findall(pattern_section1, text, re.DOTALL)
    if matches_section1:
        section1_content = matches_section1[0].strip()
        pattern_1997 = r'(.+?)1998'
        matches_1997 = re.findall(pattern_1997, section1_content, re.DOTALL)
        if matches_1997:
            section_1997 = matches_1997[0].strip()
            section_1997 = re.sub(
                r'(\d{1,2}(-\d{1,2})?\s*(January|Feburary|March|April|May|June|July|August|September|October|November|December))',
                r'\n\n1997 \1:', section_1997)

        pattern_1998 = r'1998(.+)'
        matches_1998 = re.findall(pattern_1998, section1_content, re.DOTALL)
        if matches_1998:
            section_1998 = matches_1998[0].strip()
            section_1998 = re.sub(
                r'(\d{1,2}(-\d{1,2})?\s*(January|Feburary|March|April|May|June|July|August|September|October|November|December))',
                r'\n\n1998 \1:', section_1998)

    pattern_section2 = r'<another page>(.+)'
    matches_section2 = re.findall(pattern_section2, text, re.DOTALL)
    if matches_section2:
        section2_content = matches_section2[0].strip()
        section2_content = re.sub(
            r'((Jan(uary)?|Feb(urary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sept(ember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?).?\s*\d{1,2}(-d{1,2})?\s*,\s*(1997|1998|1999))',
            r'\n\n\1:', section2_content)

    final_text = section_1997 + section_1998 + section2_content
    with open('raw_data_afc.txt', 'w', encoding='utf-8') as file:
        file.write(final_text)

    return


def change_property_sequentially():
    temporary = read_storage_file('temporary.json')
    target_list = temporary["db"]["timeline"]

    target_list = target_list[:1]
    temporary["db"]["timeline"] = target_list
    #
    # for i, l in enumerate(target_list):
    #     if l["timeline_id"] != 10:
    #         temporary["db"]["event_timeline"][i]["timeline_id"] = 10
    #         print(l["timeline_id"])
    write_storage_file(temporary, 'temporary.json')
    return


def txt_to_raw_data(directory, file, subject):
    text = read_data_txt(directory, file)
    filtered_texts = split_by_newline(text)

    raw_data = read_storage_file('raw_data.json')
    i, target_raw_datum = next(((i, raw_datum) for i, raw_datum in enumerate(raw_data) if raw_datum.get("subject") == subject), (None, None))
    if target_raw_datum:
        new_texts = raw_data[i]["texts"]
        new_texts.extend(filtered_texts)
        raw_data[i] = {"subject": subject, "texts": new_texts}
    else:
        raw_data.append({"subject": subject, "texts": filtered_texts})
    write_storage_file(raw_data, 'raw_data.json')
    return

def txt_org():
    text = read_data_txt("", 'test.txt')
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace(' ', '')
    write_data_txt("",'test.txt', text)
    return

# reset_raw_data()
# reset_temporary()
# reset_before_translation()
# check_temporary_db()
# check_keys_validity()
# check_text_tokens(read_data_txt('', 'test.txt'))
# uploader()

# pdf_to_text()
# txt_afc_organizer()
# change_property_sequentially()
# txt_to_raw_data('great_depression', 'great_depression_6.txt', 'Great Depression')
# txt_org()