from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import re
import requests
from bs4 import BeautifulSoup

from agents.linkedin_scraper_agent import extract_linkedin_content
from agents.relevance_rag_agent import run_okr_relevance_agent
from agents.depth_originality_agent import run_depth_originality_agent
from agents.engagement_analyzer_agent import run_engagement_agent
from agents.score_feedback_agent import run_feedback_generator


load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VerifyRequest(BaseModel):
    url: str
    article_title: str
    user_id: str

@app.post("/verify")
async def verify(payload: VerifyRequest):
    try:
        if "linkedin.com" not in payload.url.lower():
            return {
                "result": "Invalid URL",
                "valid": False,
                "feedback": "Only LinkedIn URLs are allowed."
            }

        # ✅ Step 1: Extract content
        extracted = await extract_linkedin_content(payload.url)
        no_of_likes = extracted.get("likes", "")
        no_of_comments = extracted.get("comments", "")

        if "error" in extracted:
            return {
                "result": "Extraction failed",
                "valid": False,
                "feedback": extracted["error"]
            }

        article_content = extracted.get("article_content", "")
        hashtags = re.findall(r"#\w+", article_content)
        if not article_content.strip():
            return {
                "result": "No meaningful content extracted",
                "valid": False,
                "feedback": "Article seems empty or inaccessible."
            }

        # ✅ Step 2: Run Relevance Agent
        relevance_result = run_okr_relevance_agent(article_content, payload.article_title)
        # use this later
        relevance_score = relevance_result.get("relevance_score", 0)
        relevance_justification = relevance_result.get("justification", "")

        # ✅ Step 3: Run Depth & Originality Agent
        depth_result = run_depth_originality_agent(article_content, payload.article_title)
        idea_density_score = depth_result["idea_density"]
        sentiment_score = depth_result["sentiment_score"]
        application_score = depth_result["application"]
        avg_insights = round((idea_density_score +sentiment_score + application_score)/15 * 100); 

        # ✅ Step 4: Run Engagement Agent
        engagement_result = run_engagement_agent(
        likes=int(no_of_likes or 0),
        comments=extracted.get("raw_comments", []),  # assuming comments are scraped
        hashtags=hashtags
        )
        engagement_score = engagement_result["engagement_score"]

        # ✅ Step 4: Score and Feedback Agent
        feedback = run_feedback_generator(
            relevance=relevance_score,
            insight=avg_insights,
            engagement=engagement_score,
            article=article_content
        )


        return {
            "result": "Extraction and relevance analysis successful",
            "valid": True,
            # "article_content": article_content,
            # "likes": extracted.get("likes", ""),
            # "comments": extracted.get("comments", ""),
            # "hashtags":hashtags,
            # "publish_date": extracted.get("publish_date", ""),
            # "relevance_justification": relevance_justification,
            # "depth": {
            # "idea_density": depth_result["idea_density"],
            # "sentiment": {
            #     "type": depth_result["sentiment_type"],
            #     "score": depth_result["sentiment_score"]
            # },
            # "application": depth_result["application"],
            # "summary": depth_result["summary"]
            # },
            # "engagement_analysis": engagement_result,
            # "engagement_score":engagement_score,
            # "avg_insights": avg_insights,
            # "relevance_score": relevance_score,
            "score_feedback": feedback
        }

    except Exception as e:
        return {
            "result": "Internal server error",
            "valid": False,
            "feedback": str(e)
        }

class LinkRequest(BaseModel):
    url: str

@app.post("/get-title")
def verify_metadata(link: LinkRequest):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link.url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("meta", property="og:title")
        description = soup.find("meta", property="og:description")

        return {
            "title": title.get("content") if title else "No title found",
            "description": description.get("content") if description else "No description found"
        }
    else:
        return {"error": "Could not fetch URL", "status_code": response.status_code}