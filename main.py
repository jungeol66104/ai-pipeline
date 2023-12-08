from app.crawler.wikipedia_crawler import wikipedia_crawler
from app.ai.simaqian import simaqian
from app.ai.translator_kr import translator_kr
from app.processor.layer0_processor import layer0_processor
from app.processor.layer1_processor import layer1_processor
from app.processor.layer2_processor import layer2_processor


def run_pipeline(title=""):
    if title != "":
        wikipedia_crawler(title)
    end, text_packet = layer0_processor()
    events_packet = simaqian(text_packet)
    events_for_translator, events_for_crawler = layer1_processor(events_packet)
    events_kr = translator_kr(events_for_translator)
    layer2_processor(events_kr)
    # if len(events_for_crawler) != 0:
    #     crawler(events_for_crawler)
    #     run_pipeline()
    if not end:
        run_pipeline()


if __name__ == "__main__":
    run_pipeline('Donald Trump')
