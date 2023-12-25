from gpt import gpt
# refactoring: clear


def translator_kr(timelines_for_translator, events_for_translator):

    prompt_for_timelines = ""
    input_timelines = f"{timelines_for_translator}"
    while True:
        output_timelines = gpt("gpt-3.5-turbo-1106", prompt_for_timelines, input_timelines, 0.2, 4095)
        timelines_kr = list(output_timelines.values())
        if len(timelines_for_translator) == len(timelines_kr):
            for index, timeline in enumerate(timelines_kr):
                timeline["timeline_id"] = timelines_for_translator[index]["id"]
            break

    prompt_for_events = "You are the best translator who converts some part of user input into Korean.\n\nFollow the conditions below and only return JSON format.\n\nCondition-1. Only translate values of \"ko_name\" and \"ko_description\".\n\nCondition-2. For \"ko_name\", translated Korean must be a nominalized format.\n\nCondition-3. For \"ko_description\", translated Korean must be '이다'체, not '입니다'체.\n\nCondition-4. Make user input list to JSON just like the format below.\n\nDesired JSON Format:\n{\"1\": first dictionary of the user input list that is translated., ..., \"N\": Nth dictionary of the user input list that is translated.}"
    input_events = f"{events_for_translator}"
    while True:
        output_events = gpt("gpt-3.5-turbo-1106", prompt_for_events, input_events, 0.2, 4095)
        events_kr = list(output_events.values())
        if len(events_for_translator) == len(events_kr):
            for index, timeline in enumerate(events_kr):
                timeline["event_id"] = events_for_translator[index]["id"]
            break

    return timelines_kr, events_kr
