from app.crawler.wikipedia_crawler import wikipedia_crawler
from app.pipeline.basic_pipeline import basic_pipeline
from app.pipeline.wikipedia_pipeline import wikipedia_pipeline


# refactoring: clear


def run_main():
    # pipelines
    # basic_pipeline("Vladimir Putin")
    wikipedia_pipeline()

    # individuals
    # wikipedia_crawler("putin")
    return


if __name__ == "__main__":
    run_main()
