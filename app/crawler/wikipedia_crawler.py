import wikipediaapi
from app.db.session import query_serp_urls_by_url
from app.util.utils import read_storage_file, write_storage_file, logger, split_by_newline, get_token_limit, modify_storage_file_list
# refactoring: clear


@logger
def wikipedia_crawler(subject, query=None):
    if query is None:
        query = subject

    wiki = wikipediaapi.Wikipedia('testBot/0.0', 'en')
    page = wiki.page(query)
    canonical_url = page.canonicalurl

    # check for the same url that has the same subject from db
    serp_urls_from_db = query_serp_urls_by_url(canonical_url)
    serp_url_subjects_from_db = [serp_url_from_db.subject for serp_url_from_db in serp_urls_from_db if serp_url_from_db.is_completed == 1]
    if subject in serp_url_subjects_from_db:
        return

    text = page.text
    texts = split_by_newline(text)

    modify_storage_file_list('', {"token_limit": get_token_limit(texts), "subject": subject, "texts": texts}, 'raw_data.json')
    modify_storage_file_list('db/serp_url', {"subject": subject, "name": f"{subject} - Wikipedia", "url": canonical_url, "is_completed": 1}, 'temporary.json')
    return
