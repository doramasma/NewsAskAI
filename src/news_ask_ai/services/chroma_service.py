from typing import Any
import chromadb

from chromadb import GetResult, QueryResult
from datetime import datetime

from news_ask_ai.utils.logger import setup_logger

logger = setup_logger()

class ChromaDBService:
    """
    A service class for managing interactions with Chroma DB.
    """

    def __init__(self, collection_name: str) -> None:
        logger.info(f"Initializing ChromaDBService with collection: {collection_name}")
 
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine",  # Configure ChromaDB to use cosine similarity
                "hnsw:search_ef": 100,
                "description": "This collection will contain representations of news articles.",
                "created": str(datetime.now())
            }
        )
    
    def add_documents(
            self, 
            documents: list[str], 
            embeddings: list[Any], 
            metadata: list[Any], 
            ids: list[str]
        ) -> None:
        logger.info(f"Adding {len(documents)} documents to the collection.")

        try:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadata,
                ids=ids
            )
            logger.info("Documents added successfully to the collection.")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            
    def delete_documents(self,) -> None:
        pass

    def retrieve_documents(self, embeddings: list[Any]) -> QueryResult:
        logger.info("Retrieving top k documents.")

        documents = self.collection.query(
            query_embeddings=embeddings,
            n_results=10,
        )
        
        return documents

    def collection_count(self,) -> int:
        return self.collection.count()
        
    def collection_head(self, n: int = 10) -> GetResult: 
        return self.collection.peek(limit=n) 
        