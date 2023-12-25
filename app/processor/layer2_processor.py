from app.db.session import query_event_highest_id, query_timeline_highest_id, query_timeline_by_name, query_association_highest_id
from app.utils import read_storage_file, write_storage_file, modify_storage_file, get_is_date_valid, get_ephemeris_time
# refactoring:


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

    timeline_next_id = query_timeline_highest_id() + 1
    event_next_id = query_event_highest_id() + 1
    association_next_id = query_association_highest_id() + 1

    timelines_for_db = []
    events_for_db = events_valid[:]
    associations_for_db = []

    for event in events_for_db:
        # deal with timeline
        timeline_from_db = query_timeline_by_name(event["subject"])
        timeline_id = timeline_from_db.id
        if timeline_from_db is None:
            timeline_id = timeline_next_id
            timelines_for_db.append({"id": timeline_id, "name": event["subject"]})
            timeline_next_id += 1
        # deal with event
        event_id = event_next_id
        event["id"] = event_id
        event["ephemeris_time"] = get_ephemeris_time(event["date"])
        event_next_id += 1
        # deal with association
        association_id = association_next_id
        associations_for_db.append({"id": association_id, "timeline_id": timeline_id, "event_id": event_id, "importance": event.pop("importance")})
        association_next_id += 1

    # make timelines and events for translator
    timelines_for_translator = timelines_for_db[:]
    for timeline in timelines_for_translator:
        timeline["country_code"] = 0
        timeline["timeline_id"] = timeline.pop("id")

    events_for_translator = events_for_db[:]
    for event in events_for_translator:
        event["country_code"] = 0
        event["event_id"] = event.pop("id")
        del event["date"]
        del event["ephemeris_time"]

    events_for_storage = events_invalid[:]
    iteration = events_packet["iteration"]
    max_iteration = 5
    target_file = 'invalid_events.json' if iteration >= max_iteration else 'invalid_events_terminated.json'
    invalid_events = read_storage_file(target_file)
    for event in events_for_storage:
        event["iteration"] = iteration + 1
    invalid_events.extend(events_for_storage)
    write_storage_file(invalid_events, target_file)

    modify_storage_file('timelines_for_db', timelines_for_db, 'temporary.json')
    modify_storage_file('events_for_db', events_for_db, 'temporary.json')
    modify_storage_file('associations_for_db', associations_for_db, 'temporary.json')

    return [timelines_for_translator, events_for_translator]
