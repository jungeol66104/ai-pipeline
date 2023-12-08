import os
import json

dir_processor = os.path.dirname(os.path.realpath(__file__))
dir_pipeline = os.path.join(dir_processor, '../../')
events_kr_storage_path = os.path.join(dir_pipeline, 'storage', 'events_kr_storage.json')


def layer2_processor(events_kr):
    with open(events_kr_storage_path, 'r', encoding='utf-8') as file:
        original_events_kr = json.load(file)

    new_events_kr = original_events_kr + events_kr

    with open(events_kr_storage_path, 'w', encoding='utf-8') as file:
        json.dump(new_events_kr, file, ensure_ascii=False, indent=2)
