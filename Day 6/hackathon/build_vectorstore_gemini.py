# build_vectorstore_gemini.py
import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

def create_vectorstore(bios):
    documents = [Document(page_content=bio) for bio in bios]
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    split_docs = splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))
    vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory="./vs_store_gemini")
    vectorstore.persist()
    print("✅ Vectorstore created with Gemini embeddings")

# Example bios
if __name__ == "__main__":
    bios = [
        "Ravi is a machine learning engineer working in education technology at ABC Corp.",
        "John is a freelance marketer working with small businesses.",
        "Meera is a professor in AI and leads workshops on education policy."
    ]
    create_vectorstore(bios)
