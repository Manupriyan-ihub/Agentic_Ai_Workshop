import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

from agents.relevance_agent import check_relevance
from agents.message_agent import check_messages
from agents.interaction_agent import check_interaction
from agents.submission_intake import validate_csv  # 🔄 Imported submission validator

load_dotenv()

# Init LLM, embeddings, retriever
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma(persist_directory="./vs_store_gemini", embedding_function=embeddings)
retriever = vectorstore.as_retriever()
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# UI
st.set_page_config(page_title="LinkedIn Connection Verifier")
st.title("🔍 LinkedIn Tech & Interaction Verifier")

uploaded = st.file_uploader("Upload LinkedIn Connections CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)

    if not validate_csv(df):  # ✅ Use submission agent for validation
        st.error("❌ CSV must contain columns: Name, Title, Messages, Endorsements, Events")
    else:
        verified_data = []
        tech_count = 0

        with st.spinner("🤖 AI agents verifying..."):
            for _, row in df.iterrows():
                name = row["Name"]
                title = row["Title"]
                messages = row["Messages"]
                endorsements = row["Endorsements"]
                events = row["Events"]

                relevance_output = check_relevance(rag_chain, title)
                messages_output = check_messages(rag_chain, messages)
                interaction_output = check_interaction(rag_chain, endorsements, events)

                is_tech = "yes" in relevance_output.lower()
                if is_tech:
                    tech_count += 1

                verified_data.append({
                    "Name": name,
                    "Title": title,
                    "Messages": messages,
                    "Endorsements": endorsements,
                    "Events": events,
                    "Relevance Verdict": relevance_output.strip(),
                    "Message Verdict": messages_output.strip(),
                    "Interaction Verdict": interaction_output.strip()
                })

        st.success(f"✅ {tech_count} tech-related connections found.")
        result_df = pd.DataFrame(verified_data)
        result_df.index = result_df.index + 1
        st.dataframe(result_df, use_container_width=True)
