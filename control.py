import os
import json

dir_pipeline = os.path.dirname(os.path.realpath(__file__))
raw_data_storage_json_path = os.path.join(dir_pipeline, 'storage', 'raw_data_storage.json')
events_packet_storage_json_path = os.path.join(dir_pipeline, 'storage', 'events_packet_storage.json')


def reset_raw_data_storage():
    with open(raw_data_storage_json_path, 'w', encoding='utf-8') as file:
        json.dump([], file)


def organize_events_packet_storage():
    with open(events_packet_storage_json_path, 'r', encoding='utf-8') as file:
        original_events_packets = json.load(file)

    titles = list(set([events_packet["title"] for events_packet in original_events_packets]))

    new_events_packets = []
    for title in titles:
        new_events_packet = {"title": title, "events": []}
        for events_packet in original_events_packets:
            if events_packet["title"] == title:
                new_events_packet["events"].extend(events_packet["events"])
        new_events_packets.append(new_events_packet)

    with open(events_packet_storage_json_path, 'w', encoding='utf-8') as file:
        json.dump(new_events_packets, file, indent=2)


organize_events_packet_storage()
