from abc import ABC, abstractmethod

from news_ask_ai.utils.logger import setup_logger

class BaseLLM(ABC):
    """Base class to implement a new LLM"""

    def __init__(self, model_name: str, temperature: float, max_new_tokens: int):
        self.logger = setup_logger()
        self.logger.info(f"Initializing the LLM model: {model_name}")
        
        self.model_name = model_name
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens

    @abstractmethod
    def initialize_model(self) -> None:
        pass

    @abstractmethod
    def get_completions(self, documents: list[str], question: str) -> str:
        pass