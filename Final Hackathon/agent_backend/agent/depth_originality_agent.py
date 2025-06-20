from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

prompt_template = PromptTemplate.from_template("""
You are an academic writing evaluator. Assess the following article content for depth and originality.

ARTICLE:
--------------------
{article}
--------------------

Evaluate the article based on:
1. Idea Density: Does it introduce multiple unique or insightful ideas?
2. Sentiment: Is the tone reflective, promotional, analytical, or emotional?
3. Application: Are there real-world examples or actionable insights?

Give a brief evaluation summary in 3–4 lines and rate each criterion on a scale of 1 to 5.

Output format:
Summary: <your analysis>
Idea Density: <1-5>
Sentiment: <type>, <1-5>
Application: <1-5>
""")

def evaluate_depth_and_originality(article: str) -> str:
    chain = prompt_template | llm
    return chain.invoke({"article": article})
