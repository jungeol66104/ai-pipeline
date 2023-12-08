import json
from openai import OpenAI
# refactoring: clear


def translator_kr(events_for_translator):
    client = OpenAI()

    prompt = "You are the best translator who converts some part of user input into Korean.\n\nFollow the conditions below and only return JSON format.\n\nCondition-1. Only translate values of \"ko_name\" and \"ko_description\".\n\nCondition-2. For \"ko_name\", translated Korean must be a nominalized format.\n\nCondition-3. For \"ko_description\", translated Korean must be '이다'체, not '입니다'체.\n\nCondition-4. Make user input list to JSON just like the format below.\n\nDesired JSON Format:\n{\"1\": first dictionary of the user input list that is translated., ..., \"N\": Nth dictionary of the user input list that is translated.} "

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{events_for_translator}"}
        ],
        temperature=0.2,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    content = json.loads(response.choices[0].message.content)
    events_kr = list(content.values())
    if len(events_for_translator) == len(events_kr):
        for index, event in enumerate(events_kr):
            event["id"] = events_for_translator[index]["id"]
    else:
        message = f"\t\tInvalid translated output came out.\n\t\tlist length: {len(events_for_translator)}/{len(events_kr)}\n\t\trepeating round."
        print("output: ", content)
        print(message)
        events_kr = translator_kr(events_for_translator)
    print("\ttranslator_kr complete")
    return events_kr
