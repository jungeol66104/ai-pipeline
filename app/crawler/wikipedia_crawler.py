import wikipediaapi
from app.utils import read_storage_file, write_storage_file, logger, split_by_newline


# refactoring: clear


@logger
def wikipedia_crawler(crawling_target):
    wiki = wikipediaapi.Wikipedia('testBot/0.0', 'en')
    text = wiki.page(crawling_target).text
    new_texts = split_by_newline(text)

    original_raw_data = read_storage_file('raw_data.json')
    new_raw_data = original_raw_data[:]
    index, raw_datum = next(((index, item) for index, item in enumerate(new_raw_data) if item.get("subject") == crawling_target), (None, None))
    if raw_datum:
        new_raw_data[index]["texts"].extend(new_texts)
    else:
        new_raw_data.append({"subject": crawling_target, "texts": new_texts})
    write_storage_file(new_raw_data, 'raw_data.json')
    return
