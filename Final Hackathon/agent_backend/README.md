# Agent Backend

## Folder Structure

- `main.py`: Entry point for the backend API server.
- `agent/`: Contains AI agent modules responsible for various functionalities such as content extraction, feedback, relevance, and social impact analysis.
- `chroma_okr/`: Vector store data directory used for storing embeddings and related data.
- `Data/`: Contains reference data files used by the backend.
- `db/`: Database related modules, including MongoDB connection and operations.
- `utils/`: Utility scripts for various helper functions.
- `.env`: Environment configuration file for sensitive settings.
- `requirements.txt`: Python dependencies required for the backend.
- `.gitignore`: Git ignore file.

## Tools Used

- **FastAPI**: Web framework for building the API server.
- **Uvicorn**: ASGI server for running FastAPI applications.
- **Langchain**: Framework for building language model applications.
- **Google Generative AI**: Integration with Google's generative AI services.
- **HTTPX**: HTTP client for making asynchronous requests.
- **python-dotenv**: For loading environment variables from `.env` files.
- **BeautifulSoup4**: For parsing and extracting content from HTML.
- **Motor**: Asynchronous MongoDB driver for database operations.

## Overview

This backend serves as the API layer for the hackathon project, hosting multiple AI agents that perform tasks such as content extraction, relevance scoring, feedback generation, and social impact analysis. It also manages vector stores for efficient retrieval and integrates with external AI services.
