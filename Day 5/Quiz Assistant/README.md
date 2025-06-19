# Quiz Assistant using Gemini Flash

## Description
Quiz Assistant is a Streamlit-based application that allows users to upload PDF documents, summarizes the content, and generates multiple-choice quiz questions based on the summary. It leverages AI models and utilities to provide an interactive quiz generation experience.

## Features
- Upload PDF files for content extraction.
- Summarize the uploaded PDF content.
- Generate multiple-choice questions (MCQs) from the summary.
- User-friendly Streamlit interface.

## Installation
1. Clone the repository or download the project files.
2. Navigate to the `Day 5/Quiz Assistant` directory.
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit app:
```bash
streamlit run app.py
```
- Upload a PDF file using the file uploader.
- View the summarized content.
- Specify the number of MCQs to generate.
- View the generated quiz questions.

## Dependencies
- PyPDF2
- langchain
- google-generativeai
- streamlit

## License
This project is licensed under the MIT License.
