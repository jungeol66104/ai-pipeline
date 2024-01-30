from app.utils import read_storage_file
from app.crawler.crawler import crawler
from app.ai.simaqian import simaqian
from app.processor.layer0_processor import layer0_processor
from app.processor.layer1_processor import layer1_processor
from app.processor.layer2_processor import layer2_processor
from app.db.uploader import uploader
# refactoring: clear


def run_pipeline():
    while read_storage_file('status.json')["run"]:
        print('\nCYCLE START')
        # phase 1: crawler
        crawling_model, crawling_target = layer0_processor()
        crawler(crawling_model, crawling_target)
        # phase 2: ai
        text_packet = layer1_processor()
        events_packet = simaqian(text_packet)
        layer2_processor(events_packet)
        print('CYCLE END')
    return


if __name__ == "__main__":
    run_pipeline()
