import json
from news_ask_ai.services.chroma_service import ChromaDBService
from news_ask_ai.services.embedding_service import EmbeddingService
from news_ask_ai.services.llm_completion_service import LLMCompletionService


def main() -> None:
    service = ChromaDBService("news-collection")
    embedding_service = EmbeddingService()

    # Reading example news dataset
    with open("src/news_ask_ai/datasets/news_articles_dataset_example.json", "r", encoding="utf-8") as file:
        news_articles = json.load(file)

    # Example of ingestion
    for ids, articles in enumerate(news_articles):
        document = f"Title: {articles['title']}\n content: {articles['content']}"
        document_embedding = embedding_service.get_embeddings([document])
        metadata = [{
            "date": articles["date"],
            "tags": ", ".join(articles["tags"])
        }]
        service.add_documents([document], document_embedding, metadata=metadata, ids=[str(ids)])

    # Example of recovering documents
    query = "I'm interested in rocket science, what are the lastest news"
    query_embedding = embedding_service.get_embeddings([query])
    retrieve_documents = service.retrieve_documents(query_embedding)
    print(retrieve_documents)

    # Example of using the LLM
    service = LLMCompletionService()
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"},
    ]

    try:
        completion = service.get_completions(messages)
        print(completion)
    except Exception as e:
        print(f"An error occurred: {e}")