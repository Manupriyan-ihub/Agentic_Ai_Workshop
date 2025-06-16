# agent_gemini.py
import os
import json
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

load_dotenv()

# Init LLM and Vector Store
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.2)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))
vectorstore = Chroma(persist_directory="./vs_store_gemini", embedding_function=embeddings)
retriever = vectorstore.as_retriever()
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Engagement detection
def is_genuine_engagement(messages: list) -> bool:
    return len(messages) >= 2 and any("thank" in m.lower() or "discuss" in m.lower() for m in messages)

# RAG relevance check
def is_domain_relevant_rag(profile_bio: str, domain: str = "AI in Education") -> bool:
    prompt = f"Based on this bio, is the person relevant to {domain}?\n\nBio:\n{profile_bio}\n\nAnswer only yes or no with a reason."
    result = rag_chain.run(prompt)
    return "yes" in result.lower()

# Verification
def verify_connection(conn: dict, domain: str = "AI in Education") -> dict:
    name = conn.get("name", "Unknown")
    messages = conn.get("messages", [])
    profile_bio = conn.get("profile_bio", "")

    genuine = is_genuine_engagement(messages)
    relevant = is_domain_relevant_rag(profile_bio, domain)
    score = int(genuine) + int(relevant)

    return {
        "name": name,
        "genuine": genuine,
        "relevant": relevant,
        "score": score
    }

# Run on JSON
def run_verification(input_json_path):
    with open(input_json_path, "r") as f:
        data = json.load(f)

    connections = data.get("connections", [])
    student_id = data.get("student_id", "unknown")

    results = [verify_connection(c) for c in connections]

    final_output = {
        "student_id": student_id,
        "verified_connections": results
    }

    with open(f"{student_id}_verified_results.json", "w") as f:
        json.dump(final_output, f, indent=2)

    print(f"✅ Verification complete: saved to {student_id}_verified_results.json")
