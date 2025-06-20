from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import re

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5
)

# Tool logic
def assess_social_impact_tool_fn(summary: str) -> str:
    prompt = f"""
You are a social media analysis agent.

Given the content of a LinkedIn article summary, assess its organic social impact on a scale of 0 to 100 based on:

1. Whether the article is likely to attract Likes, Comments, and Shares.
2. The potential for high-quality (substantive) comments vs. generic ones.
3. Usage of tags, mentions, or indicators of network amplification.

### Article Summary:
\"\"\" 
{summary}
\"\"\"

Give your score as a single integer from 0 to 100, followed by a brief justification.

Format:
Score: <number>
Reason: <short explanation>
"""
    response = llm.invoke(prompt)
    response_text = response.content if hasattr(response, "content") else str(response)
    match = re.search(r"Score:\s*(\d+)", response_text)

    score = int(match.group(1)) if match else 0
    reason = re.search(r"Reason:\s*(.*)", response_text, re.DOTALL)
    return f"Engagement Score: {score}\nReason: {reason.group(1).strip() if reason else 'No reason found'}"

# Tool
tools = [
    Tool(
        name="SocialImpactTool",
        func=assess_social_impact_tool_fn,
        description="Evaluates a LinkedIn summary's potential for organic engagement (likes/comments/shares)"
    )
]

# Agent
social_impact_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Runner function
def run_social_impact_agent(summary: str):
    return {"engagement": social_impact_agent.invoke(summary)}
