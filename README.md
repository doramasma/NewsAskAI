# NewsAskAI

🔨 WIP: NewsAskAI scrapes the latest news and generates a list of the most relevant articles. The project uses Retrieval-Augmented Generation (RAG) to allow users to ask questions about the news and get context-rich, real-time answers, powered by open-source Hugging Face embeddings and Chroma DB for efficient storage.

**Future steps:** be able to specify topics of interest and define the desired date range for the news.

## How to use it?

This project includes a Makefile to automate common tasks like linting, type checking, and running the application. You can execute the following commands with make:

### Install dependencies and create a virtual environment:

```console
$ make install
```
### Run the application after performing linting and type checking:

```console
$ make run
```
