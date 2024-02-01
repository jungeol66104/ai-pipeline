from app.ai.gpt import gpt
from app.db.session import query_timeline_by_name
from app.util.utils import read_storage_file, write_storage_file, modify_storage_file_list, logger, get_text_batches, separate_events_by_validity
from app.util.processors import simaqian_processor, simaqian_temporary_uploader
# refactoring: clear


@logger
def simaqian():
    # get raw data
    raw_data = read_storage_file('raw_data.json')
    new_raw_data = raw_data[:]

    # get events from ai
    raw_events = []
    for raw_datum in raw_data:
        subject = raw_datum["subject"]
        text_batches = get_text_batches(raw_datum)
        for text_batch in text_batches:
            prompt = f"You are a fact based history researcher. Your job is to extract events from user input and compensate it with your own knowledge.\n\nPlease follow the steps below, and provide the JSON format generated from Step-2. DO NOT provide result generated from Step-1.\n\nStep-1. List all events that are mentioned inside the user input. EVENTS SHOULD NOT BE COMPREHENSIVE, IT MUST BE VERY SPECIFIC.\n\nStep-2. With every events from Step-1, make a JSON object just like the format below.\n\nDesired JSON format:\n{{\"1\": {{\"date\": [If year, month and day are all mentioned, stictly keep 'YYYY-MM-DD' format like '2017-11-06'. If only year and month are mentioned, strictly keep 'YYYY-MM' format like '1998-06'. Make sure if the MM is refering to month not two first digits of year. If only year is mentioned, strictly keep 'YYYY' format like '1398'. NO OTHER FORMATS ARE ALLOWED FOR date. All months should be represented as numbers not strings like 'May'.], \"name\": [Assign the name of the event. It should be concise but specific and attractive.], \"description\": [Less than three sentences, you MUST paraphrase what is mentioned in the user input IN YOUR OWN WORDS. If nothing is mentioned and you know about the event, describe what it is about.], \"subject\": [First check the subject name {{subject}}. If it fits the event, use this. If not, assign new subject name that is general, and simple such as the {subject}.], \"importance\": [Assign a number in your subjective manner ranging 1 to 1000 considering its importance in terms of the subject you gave to this event and its cultural, economical and political impact.]}}, \"2\": {{Same as key \"1\"}}, ... , \"N\": {{Same as key \"1\"}}}}"
            input_data = text_batch
            output_data = gpt("gpt-3.5-turbo-1106", prompt, input_data, 0.2, 4095)
            modify_storage_file_list('db/fine_tuning_training_set', {"model": "simaqian", "input": input_data, "output": output_data}, 'temporary.json')
            output_events = list(output_data.values())
            raw_events.extend(output_events)
        new_raw_data.remove(raw_datum)

    # get valid and invalid events
    seperated_events = separate_events_by_validity(raw_events)
    valid_raw_events, invalid_events = seperated_events["valid_raw_events"], seperated_events["invalid_events"]

    # check for existing timelines
    subjects = list(set([valid_raw_event["subject"] for valid_raw_event in valid_raw_events]))
    timelines_from_temporary = read_storage_file('temporary.json')["db"]["timeline"]
    timeline_names = []
    for subject in subjects:
        timeline_from_db = query_timeline_by_name(subject)
        timeline_from_temporary = next((timeline for timeline in timelines_from_temporary if timeline.get("name") == subject), None)
        if timeline_from_db is not None or timeline_from_temporary is not None:
            continue
        else:
            timeline_names.append(subject)

    # get timelines from ai
    prompt = "Your job is to describe what each subject of user input is.\n\nWith all subjects in the user input, make a JSON object just like the format below and return the result.\n\nDesired JSON format:\n{\"1\": {\"name\": [each given subject] \"description\": [what is it? be specific with meta data in less than 7 words of plain text]}, \"2\": {Same as key \"1\"}, ... , \"N\": {Same as key \"1\"}}"
    input_data = f'{timeline_names}'
    output_data = gpt("gpt-3.5-turbo-1106", prompt, input_data, 0.2, 4095)
    modify_storage_file_list('db/fine_tuning_training_set', {"model": "simaqian", "input": input_data, "output": output_data}, 'temporary.json')
    raw_timelines = list(output_data.values())

    # refine and upload to temporary.json
    items_for_db = simaqian_processor(valid_raw_events, raw_timelines)
    timelines_for_db, events_for_db, event_timelines_for_db, invalid_events_for_db = items_for_db["timelines_for_db"], items_for_db["events_for_db"], items_for_db["event_timelines_for_db"], invalid_events
    simaqian_temporary_uploader(timelines_for_db, events_for_db, event_timelines_for_db, invalid_events_for_db)
    write_storage_file(new_raw_data, 'raw_data.json')
    return
