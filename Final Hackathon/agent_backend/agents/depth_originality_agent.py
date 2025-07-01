# agents/depth_originality_agent.py
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import re
load_dotenv()

# Load LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.4
)

# Prompt
depth_prompt = PromptTemplate.from_template("""
You're a writing evaluator.
Evaluate the following article titled:
"{title}"
ARTICLE:
-------------------
{article}
-------------------
Analyze it across these 3 criteria:
1. **Idea Density (1–5)** – Does it introduce unique concepts or deep insight?
2. **Sentiment (type + score)** – What's the tone? Reflective, promotional, analytical, etc. Rate on a 1–5 scale.
3. **Application (1–5)** – Are there practical examples, actionable insights, or relevance to real-world scenarios?
Format:
Summary: <brief summary>
Idea Density: <1–5>
Sentiment: <type>, <1–5>
Application: <1–5>
""")

# Define a tool for evaluating article depth
def evaluate_article_depth(article: str, title: str) -> str:
    chain = depth_prompt | llm
    output = chain.invoke({"article": article, "title": title})
    return output.content if hasattr(output, "content") else str(output)
depth_tool = Tool(
    name="DepthEvaluator",
    func=lambda input: evaluate_article_depth(input["article"], input["title"]),
    description="Evaluates the depth, sentiment, and application of a given article"
)

# Initialize the agent with the tool
agent = initialize_agent(
    tools=[depth_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False
)

# Agent function
def run_depth_originality_agent(article: str, title: str):
    # Use the tool directly via function to preserve output structure
    text = evaluate_article_depth(article, title)
    # Extract scores
    idea = re.search(r"Idea Density:\s*(\d+)", text)
    sentiment = re.search(r"Sentiment:\s*([^,]+),\s*(\d+)", text)
    application = re.search(r"Application:\s*(\d+)", text)
    return {
        "summary": text.strip(),
        "idea_density": int(idea.group(1)) if idea else 0,
        "sentiment_type": sentiment.group(1).strip() if sentiment else "Unknown",
        "sentiment_score": int(sentiment.group(2)) if sentiment else 0,
        "application": int(application.group(1)) if application else 0
    }