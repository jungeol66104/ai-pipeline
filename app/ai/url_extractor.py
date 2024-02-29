from app.ai.gpt import gpt
from app.util.utils import modify_storage_file_list, read_storage_file, logger, get_text_batches
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
        modify_storage_file_list('db/training_set', {"model": "url_extractor", "input": input_data, "output": output_data}, 'temporary.json')

        for key in output_data.keys():
            output_data[key]["subject"] = subject
            output_data[key]["is_completed"] = 0

        new_extracted_urls = list(output_data.values())
        extracted_url_urls = [extracted_url["url"] for extracted_url in extracted_urls]
        for new_extracted_url in new_extracted_urls:
            if new_extracted_url["url"] not in extracted_url_urls:
                extracted_urls.append(new_extracted_url)

    temporary_db = read_storage_file('temporary.json')["db"]
    serp_urls_for_temporary = []

    for extracted_url in extracted_urls:
        serp_url_subjects_from_temporary = [serp_url["subject"] for serp_url in temporary_db["serp_url"] if serp_url.get("url") == extracted_url["url"]]
        if extracted_url["subject"] not in serp_url_subjects_from_temporary:
            serp_urls_for_temporary.append(extracted_url)

    modify_storage_file_list('db/serp_url', serp_urls_for_temporary, 'temporary.json')
    return
