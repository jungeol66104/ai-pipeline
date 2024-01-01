import json
from openai import OpenAI
# refactoring: clear


def gpt(model, prompt, input_data, temperature, max_tokens):
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_data}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    content = json.loads(response.choices[0].message.content)
    return content
