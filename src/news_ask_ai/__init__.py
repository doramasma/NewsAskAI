from news_ask_ai.ask.news_ask_ui import NewsAskUI
from news_ask_ai.utils.logger import setup_logger

logger = setup_logger()


def main() -> None:
    logger.info("Initializing RAG engine...")
    app = NewsAskUI()
    app.run()
