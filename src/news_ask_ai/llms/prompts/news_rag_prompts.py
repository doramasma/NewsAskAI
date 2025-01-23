# System-level prompt defining the assistant's behavior
def get_system_prompt() -> str:
    return """You are NewsAskAI, an AI assistant specialized in providing up-to-date news information. 
    
    Your responses should be based on the latest news articles provided in the context. Always strive for accuracy, objectivity, and conciseness in your answers.
    If the information is not available in the given context, state that you don't have the relevant information. When appropriate, cite the source of information from the context."""


# User-level prompt defining the interaction model
def get_user_prompt(documents: str, question: str) -> str:
    return f"""Context: {documents}

Question: {question}

Please answer the question based on the provided context from recent news articles. If the answer isn't clear from the context, say so."""
