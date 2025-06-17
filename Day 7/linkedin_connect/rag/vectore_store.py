# rag/vectorstore.py
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma(persist_directory="./vs_store_gemini", embedding_function=embeddings)
    return vectorstore.as_retriever()
