import wikipediaapi
from app.util.utils import read_storage_file, write_storage_file, logger, split_by_newline, get_token_limit
# refactoring: clear


@logger
def wikipedia_crawler(subject):
    wiki = wikipediaapi.Wikipedia('testBot/0.0', 'en')
    text = wiki.page(subject).text
    texts = split_by_newline(text)

    raw_data = read_storage_file('raw_data.json')
    raw_data.append({"token_limit": get_token_limit(texts), "subject": subject, "texts": texts})
    write_storage_file(raw_data, 'raw_data.json')
    return
