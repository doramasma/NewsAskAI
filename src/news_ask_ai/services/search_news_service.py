from gnews import GNews  # type: ignore
from dataclasses import dataclass
from datetime import date
from typing import Optional

from news_ask_ai.utils.logger import setup_logger


@dataclass
class Article:
    title: str
    description: str
    published_date: Optional[str]
    url: str


logger = setup_logger()


class SearchNewsService:
    """
    A service class for interacting with GNews (unofficial Google News).
    """

    def __init__(
        self,
        language: str = "en",
        country: str = "US",
        max_results: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        """
        :param language: Language of the news (e.g., "en", "es", "fr", etc.).
        :param country: Country for Google News region (e.g., "US", "GB", etc.).
        :param max_results: Maximum number of results to retrieve.
        :param start_date: Optional start date (datetime.date) for filtering.
        :param end_date: Optional end date (datetime.date) for filtering.
        """

        self.max_results = max_results
        self.language = language
        self.country = country
        self.start_date = start_date
        self.end_date = end_date

        logger.info(
            "Initializing SearchNewsService with "
            f"language={language}, country={country}, max_results={max_results}, "
            f"start_date={start_date}, end_date={end_date}"
        )

        self.client = GNews(language=self.language, country=self.country, max_results=self.max_results)

        if self.start_date:
            logger.debug(f"Setting GNews start_date: {self.start_date}")
            self.client.start_date = self.start_date

        if self.end_date:
            logger.debug(f"Setting GNews end_date: {self.end_date}")
            self.client.end_date = self.end_date

    def search_news(self, topic: str, top_news: Optional[bool] = False) -> list[Article]:
        """
        Search for news articles on Google News matching the given topic.
        """
        logger.info(f"Searching news for topic='{topic}' (top_news={top_news})")

        try:
            if top_news:
                articles = self.client.get_top_news(topic)
            else:
                articles = self.client.get_news(topic)

            parsed_articles = [
                Article(
                    title=article.get("title", "").strip(),
                    description=article.get("description", "").strip(),
                    published_date=article.get("published date", None),
                    url=article.get("url", "").strip(),
                )
                for article in articles
                if isinstance(article, dict)
            ]

            if not parsed_articles:
                logger.warning(f"No valid articles found for topic '{topic}'.")
                return []

            logger.info(f"Found {len(parsed_articles)} valid articles for topic='{topic}'")
            return parsed_articles
        except Exception as e:
            logger.error(f"Error occurred while fetching news for topic='{topic}': {e}", exc_info=True)
            return []
