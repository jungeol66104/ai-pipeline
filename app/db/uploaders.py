import json
from app.db.session import insert_timeline, insert_event, insert_event_timeline, insert_invalid_events, \
    insert_training_set, query_highest_invalid_events_id, query_highest_training_set_id, query_serp_urls_by_url, \
    insert_serp_url
from app.util.utils import read_storage_file, logger


@logger
def url_uploader():
    temporary_db = read_storage_file('temporary.json')["db"]
    serp_urls_from_temporary = temporary_db["serp_url"]
    serp_urls_for_db = []

    for serp_url_from_temporary in serp_urls_from_temporary:
        serp_urls_from_db = query_serp_urls_by_url(serp_url_from_temporary["url"])
        serp_url_subjects_from_db = [serp_url_from_db["subject"] for serp_url_from_db in serp_urls_from_db]
        if serp_url_from_temporary["subject"] not in serp_url_subjects_from_db:
            serp_urls_for_db.append(serp_url_from_temporary)

    insert_serp_url(serp_urls_for_db)
    return


@logger
def simaqian_uploader():
    temporary_db = read_storage_file('temporary.json')["db"]

    # timeline, event, event_timeline (id previously assigned)
    insert_timeline(temporary_db["timeline"])
    insert_event(temporary_db["event"])
    insert_event_timeline(temporary_db["event_timeline"])

    # invalid_events, fine_tuning_training_set (id should be assigned here)
    id_missing_lists = [temporary_db["invalid_events"], temporary_db["fine_tuning_training_set"]]
    highest_ids = [query_highest_invalid_events_id, query_highest_training_set_id]
    for i_list, l in enumerate(id_missing_lists):
        highest_id = 0 if highest_ids[i_list] is None else highest_ids[i_list]
        for i_id, element in enumerate(l):
            element["id"] = highest_id + 1 + i_id
    insert_invalid_events(id_missing_lists[0])

    # fine_tuning_training_set (assign model_id, make output json as str)
    for s in id_missing_lists[1]:
        s["pipeline_model_id"] = 1 if s["model"] == "simaqian" else 3
        s["output"] = json.dumps(s["output"])
        del s["model"]
    insert_training_set(id_missing_lists[1])
    return
