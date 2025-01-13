# NewsAskAI

🚧 **Work in Progress**:  
NewsAskAI scrapes the latest news and generates a list of the most relevant articles. The project leverages Retrieval-Augmented Generation (RAG) to allow users to ask questions about the news and receive context-rich, real-time answers. It is powered by open-source Hugging Face embeddings and Chroma DB for efficient storage and retrieval.

## Future Steps

- **Download Full Articles**: Implement functionality to download the entire article found based on the specified topic.
- **Multiple Topics**: Enable ingestion of multiple topics or allow users to explore top news across categories (e.g., sports, technology, politics) without requiring a fresh ingestion process.
- **Topic Modeling / Named Entity Recognition**: Add advanced features, such as a second processing stage to label or tag articles for more efficient query filtering (e.g., “Filter by entity: ‘Elon Musk’”).

## How to Use It

This project includes a `Makefile` to automate common tasks like linting, type checking, and running the application. Below are the available commands:

### Install Dependencies and Create a Virtual Environment

For general systems:

```console
$ make install
```

For systems with CUDA support:

```console
$ make install-cuda
```

### Run the application after performing linting and type checking:

```console
$ make run
```
