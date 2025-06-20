from fastapi import FastAPI
from datetime import datetime
import logging

from agent.extract_content import run_linkedin_extraction_agent
from agent.relevance_rag_agent import run_okr_relevance_agent
from agent.depth_originality_agent import run_depth_originality_agent
from agent.social_impact_agent import run_social_impact_agent
from agent.feedback_agent import run_feedback_aggregator_agent

from db.mongo import collection
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import re


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VerifyRequest(BaseModel):
    url: str
    article_title: str
    user_id: str

class VerifyResponse(BaseModel):
    result: str
    valid: bool
    feedback: str

@app.post("/verify", response_model=VerifyResponse)
async def verify(payload: VerifyRequest):
    try:
        if "linkedin.com" not in payload.url.lower():
            return {
                "result": "Invalid URL",
                "valid": False,
                "feedback": "Only LinkedIn URLs are allowed."
            }

        # Step 1: LinkedIn Extraction Agent
        extraction_result = (await run_linkedin_extraction_agent(payload.url)).get("extracted", {})
        if "error" in extraction_result:
            return {
                "result": extraction_result["error"],
                "valid": False,
                "feedback": "Extraction failed."
            }

        article_text = extraction_result.get("summary", "")

        # Step 2: OKR Relevance Agent
        relevance_output = run_okr_relevance_agent(article_text, payload.article_title)
        relevance_result = relevance_output.get("relevance", "")

        # Step 3: Depth & Originality Agent
        depth_output = run_depth_originality_agent(article_text)
        depth_eval = depth_output.get("evaluation", "")

        # Step 4: Social Impact Agent
        social_output = run_social_impact_agent(article_text)
        engagement_output = social_output.get("engagement", {}).get("output", "")
        match = re.search(r"(\d+)\s+out of\s+100", engagement_output)
        social_score = int(match.group(1)) if match else 0

        # Step 5: Feedback Aggregator Agent
        full_result = f"""
🧠 Relevance: {relevance_result}

📚 Depth Evaluation:
{depth_eval}

📢 Social Impact Score: {social_score}/100
"""

        feedback_output = run_feedback_aggregator_agent(full_result)
        feedback_summary = feedback_output.get("feedback", "")

        # Step 6: Validity Check
        relevance_output_text = relevance_result.get("output", "").lower()
        depth_eval_text = depth_eval.get("evaluation", "") if isinstance(depth_eval, dict) else str(depth_eval)

        is_valid = (
            "relevant" in relevance_output_text
            or "aligned" in relevance_output_text
        ) and "summary:" in depth_eval_text.lower() and social_score >= 50

        # Step 7: Store in MongoDB
        doc = {
            "user_id": payload.user_id,
            "url": payload.url,
            "article_title": payload.article_title,
            "relevance_result": relevance_result,
            "depth_eval": depth_eval,
            "social_score": social_score,
            "feedback": feedback_summary,
            "is_valid": is_valid,
            "created_at": datetime.utcnow(),
        }
        await collection.insert_one(doc)
        # Step 8: Return response
        return {
            "result": full_result.strip(),
            "feedback": (
                feedback_summary.get("feedback", "") 
                if isinstance(feedback_summary, dict) 
                else str(feedback_summary)
            ).strip(),
            "valid": is_valid
        }
    except Exception as e:
        logger.error(f"Error in /verify endpoint: {e}", exc_info=True)
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
