import torch
from sentence_transformers import SentenceTransformer

from news_ask_ai.utils.logger import setup_logger

logger = setup_logger()


class EmbeddingService:
    """
    A service class for creating and handle embedding models.
    """

    def __init__(self, model_name: str = "Alibaba-NLP/gte-modernbert-base") -> None:
        logger.info(f"Initializing the embedding model: {model_name}")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = SentenceTransformer(model_name, device=self.device)

    def get_embeddings(self, text_to_embed: list[str]) -> list[list[float]]:
        """
        Generate embeddings for the given list of text inputs.

        Args:
            text_to_embed (List[str]): A list of strings to embed.

        Returns:
            torch.Tensor: The embeddings as a PyTorch tensor.
        """
        embeddings = self.model.encode(text_to_embed, convert_to_tensor=True, device=self.device)
        return embeddings.tolist()
