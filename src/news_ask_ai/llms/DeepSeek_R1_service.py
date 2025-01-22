import torch
import logging
from typing import cast
from transformers import Qwen2ForCausalLM, AutoTokenizer, pipeline  # type: ignore

from news_ask_ai.llms.base import BaseLLM
from news_ask_ai.llms.prompts.news_rag_prompts import get_system_prompt, get_user_prompt

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)


class DeepSeekR1(BaseLLM):
    """
    A service class for interacting with the DeepSeek models.
    """

    def __init__(
        self,
        model_name: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        temperature: float = 0.5,
        max_new_tokens: int = 500,
    ) -> None:
        super().__init__(model_name, temperature, max_new_tokens)

        torch.random.manual_seed(0)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Using device: {self.device}")

        self.initialize_model()

    def initialize_model(self) -> None:

        self.model = Qwen2ForCausalLM.from_pretrained(
            self.model_name,
            load_in_8bit=True,
        ).eval()

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        with torch.no_grad():
            self.completion_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
            )

    def get_completions(self, documents: list[str], question: str) -> str:
        """
        Generate completions based on the provided messages.
        """
        self.logger.info(f"Creating response for the question: {question}")

        formatted_documents = "\n".join(f"document {i + 1}: {s}" for i, s in enumerate(documents))
        messages = [
            {"role": "system", "content": get_system_prompt()},
            {
                "role": "user",
                "content": get_user_prompt(formatted_documents, question),
            },
        ]

        generation_args = {
            "max_new_tokens": self.max_new_tokens,
            "return_full_text": False,
            "temperature": self.temperature,
            "do_sample": False,
        }

        with torch.no_grad():
            output = self.completion_pipeline(messages, **generation_args)

        return cast(str, output[0]["generated_text"])
