from fastapi import FastAPI
from datetime import datetime
from agent.extract_content import extract_from_linkedin
from agent.relevance_rag_agent import check_relevance
from agent.depth_originality_agent import evaluate_depth_and_originality
from agent.social_impact_agent import assess_social_impact
from agent.feedback_agent import generate_feedback
from db.mongo import collection
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware


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

class VerifyResponse(BaseModel):
    result: str
    valid: bool
    feedback: str

@app.post("/verify", response_model=VerifyResponse)
async def verify(payload: VerifyRequest):
    if "linkedin.com" not in payload.url.lower():
        return {"result": "Invalid URL", "valid": False, "feedback": "Only LinkedIn URLs are allowed."}

    # Step 1: Extract article
    extraction_result = await extract_from_linkedin(payload.url)
    if "error" in extraction_result:
        return {"result": extraction_result["error"], "valid": False, "feedback": "Extraction failed."}

    article_text = extraction_result.get("summary", "")

    # Step 2: OKR Relevance Agent
    relevance_result = check_relevance(article_text, payload.article_title)

    # Step 3: Depth & Originality Agent
    depth_eval = evaluate_depth_and_originality(article_text)

    # Step 4: Social Impact Agent
    social_score = assess_social_impact(article_text)

    # Step 5: Final Feedback Agent
    full_result = f"""
🧠 Relevance: {relevance_result}

📚 Depth Evaluation:
{depth_eval}

📢 Social Impact Score: {social_score}/100
"""
    feedback_summary = generate_feedback(full_result)

    # Step 6: Validity Check
    is_valid = (
        "relevant" in relevance_result.lower()
        or "aligned" in relevance_result.lower()
    ) and "Summary:" in depth_eval and social_score >= 50

    # Step 7: Store in MongoDB
    doc = {
        "user_id": payload.user_id,
        "url": payload.url,
        "article_title": payload.article_title,
        "relevance_result": relevance_result,
        "depth_eval": str(depth_eval.content if hasattr(depth_eval, "content") else depth_eval),
        "social_score": social_score,
        "feedback": feedback_summary["feedback"],
        "is_valid": is_valid,
        "created_at": datetime.utcnow(),
    }
    await collection.insert_one(doc)

    return {
        "result": full_result.strip(),
        "feedback": feedback_summary["feedback"].strip(),
        "valid": is_valid
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
