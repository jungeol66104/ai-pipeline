from app.utils import modify_storage_file_list, logger
from app.ai.gpt import gpt
# refactoring: clear


@logger
def translator_kr(timelines_for_translator_kr, events_for_translator_kr):
    timelines_kr, events_kr, output_timelines, output_events = None, None, None, None

    prompt_for_timelines = "You are the best translator who converts some part of user input into Korean.\n\nFollow the conditions below and only return JSON format.\n\nCondition-1. Only translate the value of 'name'. It must be a nominalized format.\n\nCondition-2. Make user input list to JSON just like the format below.\n\nDesired JSON Format:\n\n{\"1\": first dictionary of the user input list with the value of 'name' translated., ..., \"N\": Nth dictionary of the user input list with the value of 'name' translated.}\n"
    input_timelines = f"{timelines_for_translator_kr}"
    while True:
        if len(timelines_for_translator_kr) == 0:
            break
        output_timelines = gpt("gpt-3.5-turbo-1106", prompt_for_timelines, input_timelines, 0.2, 4095)
        timelines_kr = list(output_timelines.values())
        if len(timelines_for_translator_kr) == len(timelines_kr):
            for index, timeline in enumerate(timelines_kr):
                timeline["timeline_id"] = timelines_for_translator_kr[index]["timeline_id"]
                timeline["language_code_id"] = 2
            break

    prompt_for_events = "You are the best translator who converts some part of user input into Korean.\n\nFollow the conditions below and only return JSON format.\n\nCondition-1. Only translate values of \"name\" and \"description\".\n\nCondition-2. For \"name\", translated Korean must be a nominalized format.\n\nCondition-3. For \"description\", translated Korean must be '이다'체, not '입니다'체.\n\nCondition-4. Make user input list to JSON just like the format below.\n\nDesired JSON Format:\n{\"1\": first dictionary of the user input list that is translated., ..., \"N\": Nth dictionary of the user input list that is translated.}"
    input_events = f"{events_for_translator_kr}"
    while True:
        if len(events_for_translator_kr) == 0:
            break
        output_events = gpt("gpt-3.5-turbo-1106", prompt_for_events, input_events, 0.2, 4095)
        events_kr = list(output_events.values())
        if len(events_for_translator_kr) == len(events_kr):
            for index, timeline in enumerate(events_kr):
                timeline["event_id"] = events_for_translator_kr[index]["event_id"]
                timeline["language_code_id"] = 2
            break

    if timelines_kr is not None:
        modify_storage_file_list('db/fine_tuning_training_set', {"model": "translator_kr", "input": input_timelines, "output": output_timelines}, 'temporary.json')
    if events_kr is not None:
        modify_storage_file_list('db/fine_tuning_training_set', {"model": "translator_kr", "input": input_events, "output": output_events}, 'temporary.json')
    return timelines_kr, events_kr
