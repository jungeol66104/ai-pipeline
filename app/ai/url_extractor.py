from app.ai.gpt import gpt
from app.utils import modify_storage_file_list, read_storage_file, logger, write_storage_file
from app.processor.utils import get_text_packet, get_text_batches
# refactoring: clear


@logger
def url_extractor():
    raw_data = read_storage_file('raw_data.json')
    serp_raw_data = [raw_datum for raw_datum in raw_data if raw_datum.get("type") == "serp"]

    extracted_urls = []
    for serp_raw_datum in serp_raw_data:
        subject = serp_raw_datum["subject"]
        prompt = "Your job is to extract URLs from user input.\n\nWith all URLs mentioned in the user input, make a JSON object just like the format below and return the result.\n\nDesired JSON format:\n{\"1\": {\"name\": [title of the url] \"url\": [url]}, \"2\": {Same as key \"1\"}, ... , \"N\": {Same as key \"1\"}}"
        input_data = get_text_batches(serp_raw_datum)[0]
        output_data = gpt("gpt-3.5-turbo-1106", prompt, input_data, 0.2, 4095)
        modify_storage_file_list('db/fine_tuning_training_set', {"model": "url_extractor", "input": input_data, "output": output_data}, 'temporary.json')

        for key in output_data.keys():
            output_data[key]["subject"] = subject
        extracted_urls.append(list(output_data.values()))

    modify_storage_file_list('db/url', extracted_urls, 'temporary.json')
    return
