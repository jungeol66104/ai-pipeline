from app.ai.gpt import gpt
from app.utils import modify_storage_file_list, logger
# refactoring: clear


@logger
def simaqian(text_packet):
    subject = text_packet["subject"]
    prompt = f"You are a fact based history researcher. Your job is to extract events from user input and compensate it with your own knowledge.\n\nFollow the steps below and only return JSON format made from Step-3.\n\nStep-1. List all events that are mentioned inside the user input. EVENTS SHOULD NOT BE COMPREHENSIVE OR BROAD, IT MUST BE VERY SPECIFIC.\n\nStep-2. With every events from Step-1, make a JSON just like the format below.\n\nDesired JSON format:\n{{\"1\": {{\"date\": [Strictly keep \"YYYY-MM-DD\" format. First ask yourself when it happened. If you know it, fill in with your own knowledge as specific as possible. If you do not know, just leave it as what is mentioned in the user input alternating MM or DD that you do not know to XX.], \"name\": [Assign name of the event. It should be compact but specific and attractive.], \"description\": [Made out of 3 sentences. If mentioned in the user input, paraphrase it. If not mentioned and you know what it is about, fill in with your own knowledge.], \"subject\": [First check the subject name {subject}. If it fits the event, use this. If not, assign a new subject name that is broad, general, and simple such as the {subject}.], \"importance\": [Assign a number in your subjective manner ranging 1 to 1000 considering its importance in terms of the subject you gave to this event and its cultural, economical, political impact.]}}, \"2\": {{Same as key \"1\"}}, ... , \"N\": {{Same as key \"1\"}}}}\n\nStep-3. Before returning the JSON you made, take a deep breath. Check if you made all events listed in Step-1 to JSON. Check if you fully used your knowledge to fill in the \"date\" and \"description\". Check if you only filled in facts that you are confident of. If you found some mistakes while checking, fix all and return the final result."
    input_data = text_packet["text"]
    output_data = gpt("gpt-3.5-turbo-1106", prompt, input_data, 0.2, 4095)

    events = list(output_data.values())
    events_packet = {"subject": subject, "events": events}

    modify_storage_file_list('db/fine_tuning_training_set', {"model": "simaqian", "input": input_data, "output": output_data}, 'temporary.json')
    return events_packet
