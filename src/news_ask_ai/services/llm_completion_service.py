import torch
from typing import cast
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline # type: ignore

from news_ask_ai.utils.logger import setup_logger

logger = setup_logger()

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


class LLMCompletionService:
    """
    A service class for interacting with the LLM model.
    """

    def __init__(self, model_name: str = "microsoft/Phi-3.5-mini-instruct") -> None:
        logger.info(f"Initializing the LLM model: {model_name}")

        torch.random.manual_seed(0)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            device_map="cuda", 
            torch_dtype="auto", 
            trust_remote_code=True, 
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    

    def get_completions(
        self, 
        messages: list[dict[str, str]], 
        max_new_tokens: int = 500
    ) -> str:
        """
        Generate completions based on the provided messages.

        Args:
            messages (list[dict]): A list of dictionaries with 'role' and 'content' keys.
            max_new_tokens (int): The maximum number of tokens to generate.

        Returns:
            str: The generated completion text.
        """

        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )

        generation_args = {
            "max_new_tokens": max_new_tokens,
            "return_full_text": False,
            "temperature": 0.1,
            "do_sample": False,
        }

        output = pipe(messages, **generation_args)
        return cast(str, output[0]['generated_text'])

