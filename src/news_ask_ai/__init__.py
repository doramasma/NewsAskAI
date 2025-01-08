from news_ask_ai.services.chroma_service import ChromaDBService


def main() -> None:
    service = ChromaDBService("news-collection")
    print(service)