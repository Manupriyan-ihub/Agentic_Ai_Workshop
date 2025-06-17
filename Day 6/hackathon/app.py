import pandas as pd
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma(persist_directory="./vs_store_gemini", embedding_function=embeddings)
retriever = vectorstore.as_retriever()
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def is_tech_connection(title: str, domain: str = "AI or software or EdTech") -> str:
    prompt = f"""
    Is this job title likely related to {domain}?
    Title: {title}

    Answer yes or no with a short reason.
    """
    return rag_chain.run(prompt)

# Streamlit App
st.set_page_config(page_title="LinkedIn Tech Verifier")
st.title("👥 LinkedIn Connection Relevance Checker")

uploaded = st.file_uploader("Upload scraped connections CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)

    if not {"Name", "Title", "Messages", "Endorsements", "Events"}.issubset(df.columns):
        st.error("CSV must contain columns: Name, Title, Messages, Endorsements, Events")
    else:
        verified = []
        tech_count = 0

        with st.spinner("🤖 AI agent is verifying your LinkedIn connections..."):
            for _, row in df.iterrows():
                name = row["Name"]
                title = row["Title"]
                messages = row["Messages"]
                endorsements = row["Endorsements"]
                events = row["Events"]

                result = is_tech_connection(title)
                relevant = "yes" in result.lower()
                if relevant:
                    tech_count += 1

                verified.append({
                    "Name": name,
                    "Title": title,
                    "Messages": messages,
                    "Endorsements": endorsements,
                    "Events": events,
                    "Gemini Output": result.strip()
                })

        st.success(f"{tech_count} tech industry connections found.")
        result_df = pd.DataFrame(verified)
        result_df.index = result_df.index + 1  # Make index start from 1
        st.dataframe(result_df)
        st.dataframe(result_df, use_container_width=True)
