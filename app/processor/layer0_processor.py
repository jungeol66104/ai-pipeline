from app.utils import read_storage_file, write_storage_file, modify_storage_file_value, logger
# refactoring: clear


@logger
def layer0_processor():
    crawling_model, crawling_target = None, None
    if len(read_storage_file('raw_data.json')) != 0:
        crawling_model = "skip"
    elif len(read_storage_file('queue.json')) != 0:
        crawling_model = "wikipedia"
        queue = read_storage_file('queue.json')
        crawling_target = queue.pop(0)
        modify_storage_file_value('crawling_target', crawling_target, 'temporary.json')
        write_storage_file(queue, 'queue.json')
    # elif len(read_storage_file('invalid_events.json')) != 0:
    #     crawling_model = "serp"
    #     events_packets = read_storage_file('invalid_events.json')
    #     crawling_target = {"subject": events_packets[0]["subject"], "event": events_packets[0]["events"].pop(0)}
    #     write_storage_file(events_packets, 'invalid_events.json')
    return crawling_model, crawling_target
