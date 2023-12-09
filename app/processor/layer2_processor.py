import os
import json
from app.db.session import query_timeline_by_name
# refactoring: clear

dir_processor = os.path.dirname(os.path.realpath(__file__))
dir_pipeline = os.path.join(dir_processor, '../../')
events_kr_storage_path = os.path.join(dir_pipeline, 'storage', 'events_kr_storage.json')
timelines_kr_storage_path = os.path.join(dir_pipeline, 'storage', 'timelines_kr_storage.json')


def layer2_processor(timelines_kr, events_kr):
    # events_kr
    with open(events_kr_storage_path, 'r', encoding='utf-8') as file:
        original_events_kr = json.load(file)

    new_events_kr = original_events_kr + events_kr

    with open(events_kr_storage_path, 'w', encoding='utf-8') as file:
        json.dump(new_events_kr, file, ensure_ascii=False, indent=2)

    # timelines_kr
    with open(timelines_kr_storage_path, 'r', encoding='utf-8') as file:
        original_timelines_kr = json.load(file)

    new_timelines_kr = original_timelines_kr[:]
    timeline_from_db = query_timeline_by_name(timelines_kr[0]["ko_name"])
    timeline_from_json = timelines_kr[0]["ko_name"] in [timeline["ko_name"] for timeline in original_timelines_kr]
    if not timeline_from_db and not timeline_from_json:
        new_timelines_kr.extend(timelines_kr[0])

    with open(timelines_kr_storage_path, 'w', encoding='utf-8') as file:
        json.dump(new_timelines_kr, file, ensure_ascii=False, indent=2)

    print('\tlayer2_processor complete')
