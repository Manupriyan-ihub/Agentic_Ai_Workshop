from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5
)

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

def run_feedback_generator(relevance: int, insight: int, engagement: int, article: str):
    avg_score = int(round((relevance + insight + engagement) / 3))

    chain = feedback_prompt | llm
    output = chain.invoke({
        "relevance": relevance,
        "insight": insight,
        "engagement": engagement,
        "article": article[:4000]  # Truncate if article is too long
    })

    raw_output = output.content if hasattr(output, "content") else str(output)

    try:
        # Try to extract the first JSON object from the output
        json_start = raw_output.find("{")
        json_end = raw_output.rfind("}") + 1
        json_data = raw_output[json_start:json_end]
        return json.loads(json_data)
    except Exception as e:
        print("⚠️ Failed to parse feedback:\n", raw_output)
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
