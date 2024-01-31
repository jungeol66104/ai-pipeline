from app.db.session import query_timeline_by_name, query_highest_timeline_id, query_highest_event_id, query_highest_event_timeline_id
from app.processor.utils import logger, get_is_date_valid, read_storage_file, get_ephemeris_time


@logger
def simaqian_processor(events, timelines):
    events_valid = []
    events_invalid = []

    for event in events:
        is_date_valid = get_is_date_valid(event["date"])
        if is_date_valid:
            events_valid.append(event)
        else:
            events_invalid.append(event)




    return