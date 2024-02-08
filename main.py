# refactoring: clear
from app.pipeline.search_pipeline import search_pipeline
from app.pipeline.wikipedia_pipeline import wikipedia_pipeline


def run_main():
    # pipelines
    # wikipedia_pipeline()
    # invalid_pipeline('')
    search_pipeline()

    # individuals
    # wikipedia_crawler("putin")
    return


if __name__ == "__main__":
    run_main()
