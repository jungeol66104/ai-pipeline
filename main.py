from app.pipeline.search_pipeline import search_pipeline
from app.pipeline.wikipedia_pipeline import wikipedia_pipeline
# refactoring: clear


def run_main():
    # pipelines
    # wikipedia_pipeline()
    # invalid_pipeline('')
    search_pipeline()

    # individuals
    # wikipedia_crawler("")
    return


if __name__ == "__main__":
    run_main()
