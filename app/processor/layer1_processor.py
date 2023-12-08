import os
import json
import re
import spiceypy as spice
from app.db.session import insert_event, insert_timeline, insert_association, query_event_highest_id, \
    query_timeline_highest_id, insert_test, query_test_highest_id, query_timeline_by_name

dir_processor = os.path.dirname(os.path.realpath(__file__))
dir_pipeline = os.path.join(dir_processor, '../../')
events_packet_storage_json_path = os.path.join(dir_pipeline, 'storage', 'events_packet_storage.json')
naif0012_tls_path = os.path.join(dir_pipeline, 'data', 'naif0012.tls')


def layer1_processor(events_packet):
    events_valid = []
    events_invalid = []

    # check for validity
    for event in events_packet["events"]:
        is_date_valid = get_is_date_valid(event["date"])
        if is_date_valid:
            events_valid.append(event)
        else:
            events_invalid.append(event)

    # timelines, events, associations for db
    timeline_from_db = query_timeline_by_name(events_packet["title"])
    timeline_next_id = timeline_from_db.id if timeline_from_db else query_timeline_highest_id() + 1
    event_next_id = query_event_highest_id() + 1

    timelines_for_db = [{"name": events_packet["title"]}]
    events_for_db = events_valid[:]
    associations_for_db = []

    for event in events_for_db:
        event["julian_date"] = get_julian_date(event["date"])
        event["id"] = event_next_id
        association = {"timeline_id": timeline_next_id, "event_id": event_next_id, "importance": event.pop("importance")}
        associations_for_db.append(association)
        event_next_id += 1

    insert_timeline(timelines_for_db)
    insert_event(events_for_db)
    insert_association(associations_for_db)
    print('Inserted timelines, events, associations to the DB.')

    # make events for translator
    events_for_translator = events_for_db[:]
    for event in events_for_translator:
        del event["date"]
        del event["julian_date"]
        event["ko_name"] = event.pop("name")
        event["ko_description"] = event.pop("description")

    events_for_storage = events_invalid
    with open(events_packet_storage_json_path, 'r', encoding='utf-8') as file:
        original_events_packet = json.load(file)
    new_events_packet = original_events_packet[:]
    new_events_packet.append({"title": events_packet["title"], "events": events_for_storage})
    with open(events_packet_storage_json_path, 'w', encoding='utf-8') as file:
        json.dump(new_events_packet, file, indent=2)

    # (later)
    events_for_crawler = events_invalid

    return [events_for_translator, events_for_crawler]


def get_is_date_valid(input_string):
    pattern = re.compile(r'^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$')
    return bool(pattern.match(input_string))


def get_julian_date(date):
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
