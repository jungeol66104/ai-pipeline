# get json events only from AI
from openai import OpenAI


def herodotus():
    client = OpenAI()

    title = "Donald Trump"
    prompt = f"You are a fact based history researcher. Your job is to make a timeline of {title}.\n\nFollow the steps below and only return JSON format made in Step-3.\n\nStep-1. List 30 events that you know the exact date down to specific date which is important about {title} in your subjective manner. Events’ date must not pass over September 2021.\n\nStep-2. With every events from Step-1, make a JSON just like the format below.\n\nDesired JSON format:\n{{\"1\": {{\"date\": [Strictly keep \"YYYY-MM-DD\" format.], \"name\": [Put name of the event.], \"description\": [Made out of 3 sentences.] ,\"importance\": [Add importance ranging 1 to 1000 considering its importance in terms of the given title {title} in your subjective manner.]}}, \"2\": {{Same as key \"1\"}}, ... , \"N\": {{Same as key \"1\"}}}}\n\nStep-3. Before returning the JSON you made, take a deep breath. Check if you made all events listed in Step-1 to JSON. Check if you fully used your knowledge to fill in the \"date\" and \"description\". Check if you only filled in facts that you are confident of. If you found some mistakes while checking, fix all and return the final result."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": prompt
            },
        ],
        temperature=0.6,
        max_tokens=3800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content
