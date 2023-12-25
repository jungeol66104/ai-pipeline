from app.utils import read_storage_file, write_storage_file, modify_storage_file


def layer0_processor():
    crawling_model = None
    crawling_target = None
    if read_storage_file('raw_data.json').lenghth != 0:
        crawling_model = "skip"
    elif read_storage_file('queue.json').length != 0:
        crawling_model = "wikipedia"
        crawling_target = read_storage_file('queue.json').pop(0)
    elif read_storage_file('invalid_events.json').length != 0:
        crawling_model = "serp"
        events_packets = read_storage_file('invalid_events.json')
        crawling_target = {"subject": events_packets[0]["subject"], "event": events_packets[0]["events"].pop(0)}
        write_storage_file(events_packets, 'invalid_events.json')

    modify_storage_file('status', "in-progress", 'status.json')

    return crawling_model, crawling_target
