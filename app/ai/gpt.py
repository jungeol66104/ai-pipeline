import json
from openai import OpenAI
from app.util.utils import modify_storage_file_list
# refactoring: clear


def gpt(model, prompt, input_data, temperature, max_tokens):
    try:
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
    except Exception as e:
        modify_storage_file_list('', {"input_data": json.dumps(input_data)}, 'errors.json')
        print(e)




