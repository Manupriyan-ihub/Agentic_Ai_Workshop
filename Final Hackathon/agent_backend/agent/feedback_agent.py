from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Tool logic
def generate_feedback_tool_fn(final_result: str) -> str:
    prompt = f"""
You are an educational assistant AI that evaluates student-posted LinkedIn articles for learning outcome alignment.

Given the following combined output from multiple assessment agents:

--- BEGIN AGENT RESULT ---
{final_result}
--- END AGENT RESULT ---

Please do the following:

1. Extract and display a **score breakdown**:
   - Relevance (0–100)
   - Insight (0–100) — based on depth/originality evaluation
   - Engagement (0–100) — based on the social impact score

2. Compute and display the **average score** across the 3.

3. Generate a **reflection prompt** like:  
   > “How could this post better showcase your capstone project?”

4. Provide **2-3 specific improvement suggestions** to increase the post’s value.

Respond in this format:

Score Breakdown:
- Relevance: <x>/100
- Insight: <y>/100
- Engagement: <z>/100
- Average: <avg>/100

Reflection Prompt:
"<prompt>"

Improvement Suggestions:
1. <suggestion>
2. <suggestion>
3. <optional suggestion>
"""
    result = llm.invoke(prompt)
    return result.content

# Tool wrapper
tools = [
    Tool(
        name="FeedbackAggregatorTool",
        func=generate_feedback_tool_fn,
        description="Aggregates agent results and generates educational feedback with scoring and improvement suggestions"
    )
]

# Agent setup
feedback_aggregator_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Runner function
def run_feedback_aggregator_agent(final_result: str):
    return {"feedback": feedback_aggregator_agent.invoke(final_result)}
