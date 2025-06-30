from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
import re
from dotenv import load_dotenv

load_dotenv()

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

# Parser
def parse_engagement_response(response: str) -> dict:
    return {
        "engagement_score": int(re.search(r"Engagement Score:\s*(\d+)", response).group(1)) if re.search(r"Engagement Score:\s*(\d+)", response) else 0,
        "likes_weight": int(re.search(r"Likes Weight.*?:\s*(\d+)", response).group(1)) if re.search(r"Likes Weight.*?:\s*(\d+)", response) else 0,
        "comments_weight": int(re.search(r"Comments Weight.*?:\s*(\d+)", response).group(1)) if re.search(r"Comments Weight.*?:\s*(\d+)", response) else 0,
        "comment_quality": int(re.search(r"Comment Quality.*?:\s*(\d+)", response).group(1)) if re.search(r"Comment Quality.*?:\s*(\d+)", response) else 0,
        "hashtag_signal": int(re.search(r"Hashtag/Network Signal.*?:\s*(\d+)", response).group(1)) if re.search(r"Hashtag/Network Signal.*?:\s*(\d+)", response) else 0,
        "summary": re.search(r"Summary:\s*(.*)", response, re.DOTALL).group(1).strip() if re.search(r"Summary:\s*(.*)", response, re.DOTALL) else ""
    }

# Agent Runner
def run_engagement_agent(likes: int, comments: list, hashtags: list):
    comment_count = len(comments)
    sample_comments = "\n".join(comments[:5]) if comments else "No comments available"

    chain = engagement_prompt | llm
    result = chain.invoke({
        "likes": likes,
        "comment_count": comment_count,
        "comments": sample_comments,
        "hashtags": ", ".join(hashtags)
    })

    raw_output = str(result.content).strip() if hasattr(result, "content") else str(result).strip()
    return parse_engagement_response(raw_output)
