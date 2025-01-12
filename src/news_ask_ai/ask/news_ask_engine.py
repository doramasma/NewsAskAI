import json
from news_ask_ai.services.chroma_service import ChromaDBService
from news_ask_ai.services.embedding_service import EmbeddingService
from news_ask_ai.services.llm_completion_service import LLMCompletionService
from news_ask_ai.utils.logger import setup_logger

logger = setup_logger()


class NewsAskEngine:
    """
    A service class for interacting with the LLM model.
    """

    def __init__(
        self,
        collection_name: str,
        embedding_model_name: str = "BAAI/bge-large-en-v1.5",
        llm_model_name: str = "microsoft/Phi-3.5-mini-instruct",
    ) -> None:
        self.chroma_service = ChromaDBService(collection_name)
        self.embedding_service = EmbeddingService(embedding_model_name)
        self.llm_service = LLMCompletionService(llm_model_name)

    # TODO: Create a search engine for finding the news related to the topic
    def ingest_data(self, news_topic: str) -> None:
        logger.info("Ingesting data...")
        print(news_topic)

        # Example of ingestion
        with open("src/news_ask_ai/datasets/news_articles_dataset_example.json", "r", encoding="utf-8") as file:
            news_articles = json.load(file)

        for ids, articles in enumerate(news_articles):
            document = f"Title: {articles['title']}\n content: {articles['content']}"
            document_embedding = self.embedding_service.get_embeddings([document])
            metadata = [{"date": articles["date"], "tags": ", ".join(articles["tags"])}]
            self.chroma_service.add_documents([document], document_embedding, metadata=metadata, ids=[str(ids)])

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
