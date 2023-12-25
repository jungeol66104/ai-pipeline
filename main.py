from app.utils import read_storage_file
from app.crawler.crawler import crawler
from app.ai.simaqian import simaqian
from app.ai.translator_kr import translator_kr
from app.processor.layer0_processor import layer0_processor
from app.processor.layer1_processor import layer1_processor
from app.processor.layer2_processor import layer2_processor
from app.processor.layer3_processor import layer3_processor
# refactoring:


def run_pipeline():
    while read_storage_file('status.json')["source"] == "exist":
        print('\nCYCLE START')
        # phase 1: crawler
        crawling_model, crawling_target = layer0_processor()
        crawler(crawling_model, crawling_target)
        # phase 2: ai
        text_packet = layer1_processor()
        events_packet = simaqian(text_packet)
        timelines_for_translator, events_for_translator = layer2_processor(events_packet)
        timelines_kr, events_kr = translator_kr(timelines_for_translator, events_for_translator)
        layer3_processor(timelines_kr, events_kr)
        print('CYCLE END')
    return


if __name__ == "__main__":
    run_pipeline()
