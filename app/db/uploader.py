import json
from app.db.session import insert_timeline, insert_event, insert_event_timeline, insert_timeline_translation, insert_event_translation, insert_invalid_events, insert_fine_tuning_training_set, query_highest_timeline_translation_id, query_highest_event_translation_id, query_highest_invalid_events_id, query_highest_fine_tuning_training_set_id
from app.utils import read_storage_file, logger


@logger
def uploader():
    temporary_db = read_storage_file('temporary.json')["db"]
    # timeline, event, event_timeline (id previously assigned)
    insert_timeline(temporary_db["timeline"])
    insert_event(temporary_db["event"])
    insert_event_timeline(temporary_db["event_timeline"])
    # timeline_translation, event_translation, invalid_events, fine_tuning_training_set (id should be assigned here)
    id_missing_lists = [temporary_db["timeline_translation"], temporary_db["event_translation"], temporary_db["invalid_events"], temporary_db["fine_tuning_training_set"]]
    highest_ids = [query_highest_timeline_translation_id, query_highest_event_translation_id, query_highest_invalid_events_id, query_highest_fine_tuning_training_set_id]
    for i_list, l in enumerate(id_missing_lists):
        highest_id = 0 if highest_ids[i_list] is None else highest_ids[i_list]
        for i_id, element in enumerate(l):
            element["id"] = highest_id + 1 + i_id
    insert_timeline_translation(id_missing_lists[0])
    insert_event_translation(id_missing_lists[1])
    insert_invalid_events(id_missing_lists[2])
    # fine_tuning_training_set (assign model_id, make output json as str)
    for s in id_missing_lists[3]:
        s["pipeline_model_id"] = 1 if s["model"] == "simaqian" else 2
        s["output"] = json.dumps(s["output"])
        del s["model"]
    insert_fine_tuning_training_set(id_missing_lists[3])
    return
    # print('\ttimeline: ', temporary_db["timeline"][:1])
    # print('\tevent: ', temporary_db["event"][:1])
    # print('\tevent_timeline: ', temporary_db["event_timeline"][:1])
    # print('\ttimeline_translation: ', temporary_db["timeline_translation"][:1])
    # print('\tevent_translation: ', temporary_db["event_translation"][:1])
    # print('\tinvalid_events: ', temporary_db["invalid_events"][:1])
    # print('\tfine_tuning_training_set: ', temporary_db["fine_tuning_training_set"][:1])
