import json
from app.db.session import insert_timeline, insert_event, insert_event_timeline, insert_invalid_events, insert_fine_tuning_training_set, query_highest_timeline_translation_id, query_highest_event_translation_id, query_highest_invalid_events_id, query_highest_fine_tuning_training_set_id
from app.utils import read_storage_file, logger


@logger
def uploader():
    temporary_db = read_storage_file('temporary.json')["db"]
    # timeline, event, event_timeline (id previously assigned)
    insert_timeline(temporary_db["timeline"])
    insert_event(temporary_db["event"])
    insert_event_timeline(temporary_db["event_timeline"])
    # timeline_translation, event_translation, invalid_events, fine_tuning_training_set (id should be assigned here)
    id_missing_lists = [temporary_db["invalid_events"], temporary_db["fine_tuning_training_set"]]
    highest_ids = [query_highest_invalid_events_id, query_highest_fine_tuning_training_set_id]
    for i_list, l in enumerate(id_missing_lists):
        highest_id = 0 if highest_ids[i_list] is None else highest_ids[i_list]
        for i_id, element in enumerate(l):
            element["id"] = highest_id + 1 + i_id
    insert_invalid_events(id_missing_lists[0])
    # fine_tuning_training_set (assign model_id, make output json as str)
    for s in id_missing_lists[1]:
        s["pipeline_model_id"] = 1 if s["model"] == "simaqian" else 2
        s["output"] = json.dumps(s["output"])
        del s["model"]
    insert_fine_tuning_training_set(id_missing_lists[1])
    return


def url_uploader():
    url_from_temporary = read_storage_file('temporary.json')["db"]["url"]
    return
