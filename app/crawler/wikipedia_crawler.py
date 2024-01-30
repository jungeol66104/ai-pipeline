import wikipediaapi
from app.utils import read_storage_file, write_storage_file, logger, split_by_newline
# refactoring: clear


@logger
def wikipedia_crawler(subject):
    wiki = wikipediaapi.Wikipedia('testBot/0.0', 'en')
    text = wiki.page(subject).text
    texts = split_by_newline(text)

    raw_data = read_storage_file('raw_data.json')
    raw_data.append({"subject": subject, "texts": texts})

    write_storage_file(raw_data, 'raw_data.json')
    return
