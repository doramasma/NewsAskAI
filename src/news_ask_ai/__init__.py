from news_ask_ai.ask.news_ask_engine import NewsAskEngine

from news_ask_ai.utils.logger import setup_logger

logger = setup_logger()


def main() -> None:
    logger.info("Initializing RAG engine...")
    search_engine = NewsAskEngine(collection_name="news-collection")

    print("Indicate the topic of the news you want to ask about")
    topic_input = input("\nYour topic: ")
    search_engine.ingest_data(topic_input)

    while True:
        print("What do you want to ask about?")
        question_input = input("\nYour question: ")
        if question_input.lower() == "exit":
            break

        completion = search_engine.get_completions(question_input)
        print(completion)

    print("Thank you for using the NewsAskAI system. Goodbye!")
