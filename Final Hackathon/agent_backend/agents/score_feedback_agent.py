# agents/feedback_generator.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from dotenv import load_dotenv
import os
import json
load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5
)

# Prompt
feedback_prompt = PromptTemplate.from_template("""
You are a helpful assistant that returns only valid JSON output.
A LinkedIn article was evaluated on:
- Relevance Score: {relevance}
- Insight Score: {insight}
- Engagement Score: {engagement}
Here is the article content:
--------------------------
{article}
--------------------------
Now, generate feedback in this format:
{{
  "final_score": <int>,  // average of the three scores
  "breakdown": {{
    "relevance": {relevance},
    "insight": {insight},
    "engagement": {engagement}
  }},
  "summary_feedback": "<2-3 line human-friendly summary>",
  "improvement_suggestions": [
    "<specific improvement 1>",
    "<specific improvement 2>",
    "<specific improvement 3>"
  ],
  "reflection_prompt": "<a thoughtful question to guide future writing>"
}}
Important rules:
- Return ONLY the raw JSON (no markdown, no commentary).
- Do not wrap the result in triple backticks or tags.
- Use double quotes around all keys and string values.
""")

# Core Function
def generate_feedback(relevance: int, insight: int, engagement: int, article: str) -> str:
    chain = feedback_prompt | llm
    result = chain.invoke({
        "relevance": relevance,
        "insight": insight,
        "engagement": engagement,
        "article": article[:4000]
    })
    return result.content if hasattr(result, "content") else str(result)

# Tool Definition
feedback_tool = Tool(
    name="FeedbackGenerator",
    func=lambda input: generate_feedback(
        input["relevance"], input["insight"], input["engagement"], input["article"]
    ),
    description="Generates constructive feedback on a LinkedIn article based on relevance, insight, and engagement scores"
)

# Agent Initialization
agent = initialize_agent(
    tools=[feedback_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False
)

# Public Function
def run_feedback_generator(relevance: int, insight: int, engagement: int, article: str):
    avg_score = int(round((relevance + insight + engagement) / 3))
    raw_output = generate_feedback(relevance, insight, engagement, article)
    try:
        json_start = raw_output.find("{")
        json_end = raw_output.rfind("}") + 1
        json_data = raw_output[json_start:json_end]
        return json.loads(json_data)
    except Exception:
        print(":warning: Failed to parse feedback:\n", raw_output)
        return {
            "final_score": avg_score,
            "breakdown": {
                "relevance": relevance,
                "insight": insight,
                "engagement": engagement
            },
            "summary_feedback": "Unable to parse feedback output.",
            "improvement_suggestions": [],
            "reflection_prompt": ""
        }
