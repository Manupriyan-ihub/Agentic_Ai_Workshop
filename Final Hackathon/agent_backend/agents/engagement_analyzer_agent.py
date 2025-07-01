# agents/engagement_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
import os
import re
from dotenv import load_dotenv
load_dotenv()

# Load the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.4
)
# Prompt Template
engagement_prompt = PromptTemplate.from_template("""
You are a social engagement analyst.
Evaluate the engagement level of this LinkedIn article using the following data:
Likes: {likes}
Comments Count: {comment_count}
Sample Comments: {comments}
Hashtags Used: {hashtags}
Judging Criteria:
- Are the comments meaningful (not just “Great post!”)?
- Do the hashtags and engagement suggest reach beyond immediate network?
- Is there diversity in interaction?
Output in this format:
Engagement Score: <score>/100
Likes Weight (out of 30): <score>
Comments Weight (out of 40): <score>
Comment Quality (out of 20): <score>
Hashtag/Network Signal (out of 10): <score>
Summary: <2-line explanation>
""")

# Result Parser
def parse_engagement_response(response: str) -> dict:
    return {
        "engagement_score": int(re.search(r"Engagement Score:\s*(\d+)", response).group(1)) if re.search(r"Engagement Score:\s*(\d+)", response) else 0,
        "likes_weight": int(re.search(r"Likes Weight.*?:\s*(\d+)", response).group(1)) if re.search(r"Likes Weight.*?:\s*(\d+)", response) else 0,
        "comments_weight": int(re.search(r"Comments Weight.*?:\s*(\d+)", response).group(1)) if re.search(r"Comments Weight.*?:\s*(\d+)", response) else 0,
        "comment_quality": int(re.search(r"Comment Quality.*?:\s*(\d+)", response).group(1)) if re.search(r"Comment Quality.*?:\s*(\d+)", response) else 0,
        "hashtag_signal": int(re.search(r"Hashtag/Network Signal.*?:\s*(\d+)", response).group(1)) if re.search(r"Hashtag/Network Signal.*?:\s*(\d+)", response) else 0,
        "summary": re.search(r"Summary:\s*(.*)", response, re.DOTALL).group(1).strip() if re.search(r"Summary:\s*(.*)", response, re.DOTALL) else ""
    }

# Core Tool Function
def evaluate_engagement(likes: int, comments: list, hashtags: list) -> str:
    comment_count = len(comments)
    sample_comments = "\n".join(comments[:5]) if comments else "No comments available"
    chain = engagement_prompt | llm
    result = chain.invoke({
        "likes": likes,
        "comment_count": comment_count,
        "comments": sample_comments,
        "hashtags": ", ".join(hashtags)
    })
    return result.content if hasattr(result, "content") else str(result)

# Tool Definition
engagement_tool = Tool(
    name="EngagementEvaluator",
    func=lambda input: evaluate_engagement(input["likes"], input["comments"], input["hashtags"]),
    description="Evaluates social engagement on a LinkedIn article"
)

# Agent Initialization
agent = initialize_agent(
    tools=[engagement_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False
)

# Agent Runner
def run_engagement_agent(likes: int, comments: list, hashtags: list):
    raw_output = evaluate_engagement(likes, comments, hashtags)
    return parse_engagement_response(raw_output.strip())