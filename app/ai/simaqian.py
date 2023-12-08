import json
from openai import OpenAI
# refactoring: needed


# get json events from raw data
def simaqian(text_packet):
    client = OpenAI()

    title = text_packet["title"]
    prompt = f"You are a fact based politics researcher. Your job is to extract events from user input and compensate it with your own knowledge.\n\nFollow the steps below and only return JSON format made in Step-3.\n\nStep-1. List all events that are mentioned inside the user input.\n\nStep-2. With every events from Step-1, make a JSON just like the format below.\n\nDesired JSON format:\n{{\"1\": {{\"date\": [Strictly keep \"YYYY-MM-DD\" format. First ask yourself when it happened. If you know it, fill in with your own knowledge as specific as possible. If you do not know, just leave it as what is mentioned in the user input alternating MM or DD that you do not know to XX.], \"name\": [Put name of the event.], \"description\": [Made out of 3 sentences. If mentioned in the user input, paraphrase it. If not mentioned and you know what it is about, fill in with your own knowledge.] ,\"importance\": [Add importance ranging 1 to 1000 considering its importance in terms of the title {title} in your subjective manner.]}}, \"2\": {{Same as key \"1\"}}, ... , \"N\": {{Same as key \"1\"}}}}\n\nStep-3. Before returning the JSON you made, take a deep breath. Check if you made all events listed in Step-1 to JSON. Check if you fully used your knowledge to fill in the \"date\" and \"description\". Check if you only filled in facts that you are confident of. If you found some mistakes while checking, fix all and return the final result."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text_packet["text"]}
        ],
        temperature=0.6,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # there were no errors in JSON format of AI generated output until now
    content = json.loads(response.choices[0].message.content)
    events = list(content.values())
    events_packet = {"title": title, "events": events}

    print('\tsimaqian complete')
    return events_packet
