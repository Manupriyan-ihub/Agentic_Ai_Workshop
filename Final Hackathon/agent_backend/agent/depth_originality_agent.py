from langchain.agents import Tool, initialize_agent, AgentType
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

# Prompt Template
depth_prompt = PromptTemplate.from_template("""
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

# Tool function
def depth_eval_tool_fn(article):
    chain = depth_prompt | llm
    return chain.invoke({"article": article})

# Wrap as LangChain Tool
tools = [
    Tool(
        name="DepthOriginalityTool",
        func=depth_eval_tool_fn,
        description="Evaluates article depth, originality, sentiment, and application"
    )
]

# Initialize Agent
depth_originality_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Runner
def run_depth_originality_agent(article: str):
    return {"evaluation": depth_originality_agent.invoke(article)}
