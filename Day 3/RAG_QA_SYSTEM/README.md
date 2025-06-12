# RAG QA System - AI Research Papers

## Project Description
This project is a Retrieval-Augmented Generation (RAG) Question Answering system designed to answer questions about AI research papers. It leverages a vectorstore built from chunked PDF documents and uses a Google Gemini language model to generate answers based on retrieved relevant document sections.

## Features
- Interactive Streamlit web interface for querying AI research papers.
- Retrieval of relevant document chunks using FAISS vectorstore.
- Answer generation using Google Gemini 2.0 Flash model via Langchain.
- Source document references with page metadata and content snippets.
- Automated document loading and chunking from PDF files.

## Installation and Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd Day 3/RAG_QA_SYSTEM
   ```

2. Create and activate a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

- Enter your question about AI research papers in the input box.
- The system will return an answer along with source document snippets and page numbers.

## Data Preparation

- PDF documents should be placed in the `data` folder.
- The system automatically loads all PDFs, splits them into chunks (1000 characters with 200 overlap), and creates embeddings using the `sentence-transformers/all-MiniLM-L6-v2` model.
- A FAISS vectorstore index is created and saved locally for efficient retrieval.

## Architecture Overview

- **Streamlit UI (`app.py`)**: Provides a simple web interface for user queries.
- **RAG Pipeline (`src/rag_pipeline.py`)**: Combines retrieval from vectorstore and generation using Google Gemini LLM.
- **Retriever (`src/retriever.py`)**: Loads or creates the FAISS vectorstore index from embedded document chunks.
- **Preprocessing (`src/preprocess.py`)**: Loads PDFs, splits into chunks, and generates embeddings.

## Requirements

- Python 3.8+
- Streamlit
- Langchain
- langchain-google-genai
- langchain-community
- FAISS
- sentence-transformers
- python-dotenv

(See `requirements.txt` for full list)

## License

This project is licensed under the MIT License. See the LICENSE file for details.
