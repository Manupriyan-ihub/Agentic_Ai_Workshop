from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

# Load the retriever (RAG memory)
def load_reference_okr():
    loader = TextLoader("data/okr_reference.txt")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    vectordb = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory="./chroma_okr"
    )
    vectordb.persist()

    return vectordb.as_retriever()

# Tool function: returns relevance score (0–100)
def check_relevance_tool_fn(input_text: str) -> str:
    try:
        article_text, project_title = input_text.split("||")
    except ValueError:
        return "Input must be in the format: <article_text>||<project_title>"

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

Evaluate relevance based on Learning objectives, Project theme match, Semantic & keyword overlap.
Just return a single score from 0–100.
"""

    result = rag_chain.run(prompt)
    return f"Relevance Score: {result.strip()}"

# Tool wrapper
tools = [
    Tool(
        name="OKRRelevanceTool",
        func=check_relevance_tool_fn,
        description="Checks how relevant an article is to a given OKR/project using RAG. Input format: <article_text>||<project_title>"
    )
]

# Agent setup
okr_relevance_agent = initialize_agent(
    tools,
    ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY")),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Runner
def run_okr_relevance_agent(article_text: str, project_title: str):
    combined = f"{article_text}||{project_title}"
    return {"relevance": okr_relevance_agent.invoke(combined)}
