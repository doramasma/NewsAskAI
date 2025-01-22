import logging
from typing import Any, cast

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # type: ignore

from news_ask_ai.llms.base import BaseLLM
from news_ask_ai.llms.prompts.news_rag_prompts import (
    get_system_prompt,
    get_user_prompt,
)

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)

# Input Format:
# The phi-4 model is best suited for prompts formatted as a chat, using special tokens.
# Each message should follow this structure:
#
# <|im_start|><role><|im_sep|>
# <content><|im_end|>
#
# Example:
# <|im_start|>system<|im_sep|>
# You are a medieval knight and must provide explanations to modern people.<|im_end|>
# <|im_start|>user<|im_sep|>
# How should I explain the Internet?<|im_end|>
# <|im_start|>assistant<|im_sep|>


class Phi35LLM(BaseLLM):
    """
    A service class for interacting with the PHI 3.5 model.
    """

    def __init__(
        self, model_name: str = "microsoft/Phi-3.5-mini-instruct", temperature: float = 0.1, max_new_tokens: int = 500
    ) -> None:
        super().__init__(model_name, temperature, max_new_tokens)

        torch.random.manual_seed(0)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Using device: {self.device}")

        self.initialize_model()

    def initialize_model(self) -> None:

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            **self.get_model_kwargs(),
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

    def get_model_kwargs(self) -> dict[str, Any]:
        """
        Return default kwargs for huggingface model loading.
        """
        model_kwargs = {
            "device_map": "cuda" if self.device.type == "cuda" else "cpu",
            "torch_dtype": "auto",
            "trust_remote_code": True,
        }
        if self.device.type == "cuda":
            model_kwargs["attn_implementation"] = "flash_attention_2"

        return model_kwargs
