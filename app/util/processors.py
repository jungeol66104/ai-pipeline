from app.db.session import query_timeline_by_name, query_highest_timeline_id, query_highest_event_id, \
    query_highest_event_timeline_id, enable_timeline_by_id
from app.util.utils import logger, read_storage_file, get_ephemeris_time, modify_storage_file_list, check_temporary_db


@logger
def simaqian_processor(valid_raw_events, raw_timelines):
    main_subject_from_temporary = read_storage_file('temporary.json')["main_subject"]
    temporary_db = read_storage_file('temporary.json')["db"]
    timelines_from_temporary = temporary_db["timeline"]
    events_from_temporary = temporary_db["event"]
    event_timelines_from_temporary = temporary_db["event_timeline"]

    timeline_next_id = max(timelines_from_temporary, key=lambda x: x['id'])['id'] + 1 if len(timelines_from_temporary) > 0 else query_highest_timeline_id() + 1
    event_next_id = max(events_from_temporary, key=lambda x: x['id'])['id'] + 1 if len(events_from_temporary) > 0 else query_highest_event_id() + 1
    event_timeline_next_id = max(event_timelines_from_temporary, key=lambda x: x['id'])['id'] + 1 if len(event_timelines_from_temporary) > 0 else query_highest_event_timeline_id() + 1

    timelines_for_db = []
    events_for_db = valid_raw_events[:]
    event_timelines_for_db = []

    for event in events_for_db:
        # deal with timeline
        is_enabled = 1 if event["subject"] == main_subject_from_temporary else 0
        timeline_from_db = query_timeline_by_name(event["subject"])
        timeline_from_temporary = next((timeline for timeline in read_storage_file('temporary.json')["db"]["timeline"] if timeline.get("name") == event["subject"]), None)
        timeline_for_db = next((timeline for timeline in timelines_for_db if timeline.get("name") == event["subject"]), None)
        if timeline_from_db is not None:
            timeline_id = timeline_from_db.id
            if timeline_from_db.name == main_subject_from_temporary:
                enable_timeline_by_id(timeline_id)
        elif timeline_from_temporary is not None:
            timeline_id = timeline_from_temporary["id"]
        elif timeline_for_db is not None:
            timeline_id = timeline_for_db["id"]
        else:
            timeline_id = timeline_next_id
            timelines_for_db.append({"id": timeline_id, "name": event["subject"], "description": next((raw_timeline["description"] for raw_timeline in raw_timelines if raw_timeline.get("name") == event["subject"]), None), "is_enabled": is_enabled})
            timeline_next_id += 1
        del event["subject"]

        # deal with event
        event_id = event_next_id
        event["id"] = event_id
        event["ephemeris_time"] = get_ephemeris_time(event["date"])
        event["is_enabled"] = 1
        event_next_id += 1

        # deal with association
        event_timeline_id = event_timeline_next_id
        event_timelines_for_db.append({"id": event_timeline_id, "timeline_id": timeline_id, "event_id": event_id, "importance": event.pop("importance")})
        event_timeline_next_id += 1
    return {"timelines_for_db": timelines_for_db, "events_for_db": events_for_db, "event_timelines_for_db": event_timelines_for_db}


def simaqian_temporary_uploader(timelines_for_db, events_for_db, event_timelines_for_db, invalid_events_for_db):
    modify_storage_file_list('db/timeline', timelines_for_db, 'temporary.json')
    modify_storage_file_list('db/event', events_for_db, 'temporary.json')
    modify_storage_file_list('db/event_timeline', event_timelines_for_db, 'temporary.json')
    modify_storage_file_list('db/invalid_events', invalid_events_for_db, 'temporary.json')
    check_temporary_db()
    return
