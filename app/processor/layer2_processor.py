from app.db.session import query_highest_event_id, query_highest_timeline_id, query_highest_event_timeline_id, query_timeline_by_name
from app.utils import get_is_date_valid, get_ephemeris_time, modify_storage_file_list, logger, read_storage_file
# refactoring: clear


@logger
def layer2_processor(events_packet):
    events_valid = []
    events_invalid = []

    # check for validity
    for event in events_packet["events"]:
        is_date_valid = get_is_date_valid(event["date"])
        if is_date_valid:
            events_valid.append(event)
        else:
            events_invalid.append(event)

    # can be more abstract
    timelines_from_temporary = read_storage_file('temporary.json')["db"]["timeline"]
    events_from_temporary = read_storage_file('temporary.json')["db"]["event"]
    event_timelines_from_temporary = read_storage_file('temporary.json')["db"]["event_timeline"]
    timeline_next_id = max(timelines_from_temporary, key=lambda x: x['id'])['id'] + 1 if len(timelines_from_temporary) > 0 else query_highest_timeline_id + 1
    event_next_id = max(events_from_temporary, key=lambda x: x['id'])['id'] + 1 if len(events_from_temporary) > 0 else query_highest_event_id + 1
    event_timeline_next_id = max(event_timelines_from_temporary, key=lambda x: x['id'])['id'] + 1 if len(event_timelines_from_temporary) > 0 else query_highest_event_timeline_id + 1

    timelines_for_db = []
    events_for_db = events_valid[:]
    event_timelines_for_db = []

    for event in events_for_db:
        # deal with timeline
        timeline_from_db = query_timeline_by_name(event["subject"])
        timeline_from_temporary = next((timeline for timeline in read_storage_file('temporary.json')["db"]["timeline"] if timeline.get("name") == event["subject"]), None)
        timeline_for_db = next((timeline for timeline in timelines_for_db if timeline.get("name") == event["subject"]), None)
        if timeline_from_db is not None:
            timeline_id = timeline_from_db.id
        elif timeline_from_temporary is not None:
            timeline_id = timeline_from_temporary["id"]
        elif timeline_for_db is not None:
            timeline_id = timeline_for_db["id"]
        else:
            timeline_id = timeline_next_id
            timelines_for_db.append({"id": timeline_id, "name": event["subject"]})
            timeline_next_id += 1
        del event["subject"]
        # deal with event
        event_id = event_next_id
        event["id"] = event_id
        event["ephemeris_time"] = get_ephemeris_time(event["date"])
        event_next_id += 1
        # deal with association
        event_timeline_id = event_timeline_next_id
        event_timelines_for_db.append({"id": event_timeline_id, "timeline_id": timeline_id, "event_id": event_id, "importance": event.pop("importance")})
        event_timeline_next_id += 1
    events_invalid_for_db = events_invalid[:]

    modify_storage_file_list('db/timeline', timelines_for_db, 'temporary.json')
    modify_storage_file_list('db/event', events_for_db, 'temporary.json')
    modify_storage_file_list('db/event_timeline', event_timelines_for_db, 'temporary.json')
    modify_storage_file_list('db/invalid_events', events_invalid_for_db, 'temporary.json')
    
    # make timelines and events for translator
    timelines_for_translator_kr = timelines_for_db[:]
    for timeline in timelines_for_translator_kr:
        timeline["language_code_id"] = 2
        timeline["timeline_id"] = timeline.pop("id")

    events_for_translator_kr = events_for_db[:]
    for event in events_for_translator_kr:
        event["language_code_id"] = 2
        event["event_id"] = event.pop("id")
        del event["date"]
        del event["ephemeris_time"]

    return [timelines_for_translator_kr, events_for_translator_kr]
