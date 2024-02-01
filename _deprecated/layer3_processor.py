from app.db.uploaders import uploader
from app.utils import modify_storage_file_list, read_storage_file, modify_storage_file_value, logger, write_storage_file
# refactoring: clear


@logger
def layer3_processor(timelines_kr, events_kr):
    if timelines_kr is not None:
        modify_storage_file_list('db/timeline_translation', timelines_kr, 'temporary.json')
    if events_kr is not None:
        modify_storage_file_list('db/event_translation', events_kr, 'temporary.json')

    # uploader()

    # temporary = {
    #     "crawling_target": read_storage_file('temporary.json')["crawling_target"],
    #     "used_raw_datum_texts": [],
    #     "db": {
    #         "timeline": [],
    #         "event": [],
    #         "event_timeline": [],
    #         "timeline_translation": [],
    #         "event_translation": [],
    #         "invalid_events": [],
    #         "fine_tuning_training_set": []
    #     }
    # }
    # write_storage_file(temporary, 'temporary.json')

    raw_data = read_storage_file('raw_data.json')
    queue = read_storage_file('queue.json')
    if len(raw_data) == 0 and len(queue) == 0:
        modify_storage_file_value('run', False, 'status.json')
    return
