import streamlit as st
from utils.pdf_loader import load_pdf
from utils.summarizer import summarize_text
from utils.question_generator import generate_mcqs

def run():
    st.title("📚 Quiz Assistant using Gemini Flash")
    st.write("Upload a PDF to summarize and generate quiz questions from it.")

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("🔍 Extracting content from PDF..."):
            text = load_pdf(uploaded_file)

        st.subheader("📌 Summary")
        with st.spinner("🧠 Summarizing the content..."):
            summary = summarize_text(text)
        st.text_area("Summary Output", summary, height=200)

        st.subheader("📝 Generate Quiz Questions")
        num_questions = st.number_input("How many MCQs do you want to generate?", min_value=1, max_value=10, step=1)

        with st.spinner("🧠 Generating quiz questions..."):
            questions = generate_mcqs(summary, num_questions)
        st.text_area("Quiz Questions", questions, height=300)

if __name__ == "__main__":
    run()
