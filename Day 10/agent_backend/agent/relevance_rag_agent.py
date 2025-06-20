from langchain_community.vectorstores import Chroma  # ✅ Fixed
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # ✅ Fixed
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import extract_score
import os
import re

def load_reference_okr():
    loader = TextLoader("data/okr_reference.txt")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory="./chroma_okr")
    vectordb.persist()

    return vectordb.as_retriever()

def check_relevance(article_text: str, project_title: str) -> str:
    retriever = load_reference_okr()

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    prompt = f"""Assess how the following article aligns with the module and project:

    Article Content:
    {article_text[:4000]}

    Project Title: {project_title}

    Evaluate relevance based on Learning objectives, Project theme match, Semantic & keyword overlap:
    - Give just a score out of 100 with respect to the retreiver data
    """

    result = rag_chain.run(prompt)
    return result[:2]
    

