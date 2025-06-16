import streamlit as st
import json
import pandas as pd
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

load_dotenv()

# Load LLM & Vectorstore
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma(persist_directory="./vs_store_gemini", embedding_function=embeddings)
retriever = vectorstore.as_retriever()
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Logic
def is_genuine_engagement(messages: list) -> bool:
    return len(messages) >= 2 and any("thank" in m.lower() or "discuss" in m.lower() for m in messages)

def is_domain_relevant_rag(profile_bio: str, domain: str = "AI in Education") -> bool:
    prompt = f"Is this person relevant to {domain}?\n\nBio: {profile_bio}\n\nAnswer only yes or no with a reason."
    result = rag_chain.run(prompt)
    return "yes" in result.lower()

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

# Streamlit UI
st.set_page_config(page_title="🔍 Network Verifier", layout="centered")
st.title("🔍 Professional Network Verifier Agent")
st.caption("Check if your LinkedIn/email connections are genuine and domain-relevant (e.g., AI in EdTech).")

uploaded_file = st.file_uploader("Upload Connection JSON", type=["json"])

if uploaded_file is not None:
    data = json.load(uploaded_file)
    student_id = data.get("student_id", "unknown")
    connections = data.get("connections", [])

    st.subheader(f"👤 Student ID: `{student_id}`")
    st.write(f"🔄 Verifying {len(connections)} connections...")

    verified = []
    with st.spinner("Running Gemini agent..."):
        for conn in connections:
            result = verify_connection(conn)
            verified.append(result)

    df = pd.DataFrame(verified)
    st.success("✅ Verification Complete!")
    st.dataframe(df, use_container_width=True)

    output_json = {
        "student_id": student_id,
        "verified_connections": verified
    }

    st.download_button(
        label="📥 Download Results",
        data=json.dumps(output_json, indent=2),
        file_name=f"{student_id}_verified_results.json",
        mime="application/json"
    )
