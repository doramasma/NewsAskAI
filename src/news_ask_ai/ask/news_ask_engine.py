import uuid

from news_ask_ai.llms.DeepSeek_R1_service import DeepSeekR1
from news_ask_ai.services.chroma_service import ChromaDBService
from news_ask_ai.services.embedding_service import EmbeddingService
from news_ask_ai.services.search_news_service import SearchNewsService
from news_ask_ai.utils.logger import setup_logger
from datetime import date

logger = setup_logger()


class NewsAskEngine:
    """
    A service class for interacting with the LLM model.
    """

    def __init__(
        self,
        collection_name: str,
        embedding_model_name: str = "Alibaba-NLP/gte-modernbert-base",
        llm_model_name: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    ) -> None:
        self.chroma_service = ChromaDBService(collection_name)
        self.embedding_service = EmbeddingService(embedding_model_name)
        self.llm_service = DeepSeekR1(llm_model_name)

        self.news_service = SearchNewsService(
            language="en",
            country="US",
            max_results=10,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 13),
        )

    # TODO: Create a search engine for finding the news related to the topic
    def ingest_data(self, news_topic: str) -> None:
        logger.info("Ingesting data...")

        news_articles = self.news_service.search_news(news_topic)

        for articles in news_articles:
            document = f"Title: {articles.title}\n content: {articles.description}"
            document_embedding = self.embedding_service.get_embeddings([document])
            metadata = [{"date": articles.published_date, "url": ", ".join(articles.url)}]
            self.chroma_service.add_documents(
                [document], document_embedding, metadata=metadata, ids=[str(uuid.uuid4())]
            )

        logger.info("Data ingestion complete.")

    def get_completions(self, question: str) -> str:
        logger.info("You can now ask questions (type 'exit' to quit).")

        query_embedding = self.embedding_service.get_embeddings([question])
        retrieve_documents = self.chroma_service.retrieve_documents(query_embedding)

        if not retrieve_documents["documents"]:
            print("No documents retrieved for the question.")
            raise ValueError("Documents are required to generate completions.")

        try:
            completion = self.llm_service.get_completions(retrieve_documents["documents"][0], question)
        except Exception as e:
            print(f"An error occurred: {e}")

        return completion
