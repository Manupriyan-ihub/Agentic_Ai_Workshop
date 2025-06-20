from fastapi import FastAPI
from pydantic import BaseModel
from agent.extract_content import extract_from_linkedin
from agent.relevance_rag_agent import check_relevance
from agent.depth_originality_agent import evaluate_depth_and_originality
from agent.social_impact_agent import assess_social_impact
from agent.feedback_agent import generate_feedback



app = FastAPI()

class VerifyRequest(BaseModel):
    url: str
    article_title: str
    user_id:str

class VerifyResponse(BaseModel):
    result: str
    valid: bool

@app.post("/verify", response_model=VerifyResponse)
async def verify(payload: VerifyRequest):
    if "linkedin.com" not in payload.url.lower():
        return {"result": "Invalid URL", "valid": False}

    # Step 1: Extract article
    extraction_result = await extract_from_linkedin(payload.url)
    if "error" in extraction_result:
        return {"result": extraction_result["error"], "valid": False}

    article_text = extraction_result.get("summary", "")

    # Step 2: OKR Relevance Agent
    relevance_result = check_relevance(article_text, payload.article_title)

    # Step 3: Depth & Originality Agent
    depth_eval = evaluate_depth_and_originality(article_text)

    # Step 4: Social Impact Agent
    social_score = assess_social_impact(article_text)

    # Final Result Compilation
    full_result = f"""
🧠 Relevance: {relevance_result}

📚 Depth Evaluation:
{depth_eval}

📢 Social Impact Score: {social_score}/100
"""

    # Step 5: Final Feedback Agent
    feedback_summary = generate_feedback(full_result)

    # Validity Conditions
    is_valid = (
        "relevant" in relevance_result.lower()
        or "aligned" in relevance_result.lower()
    ) and "Summary:" in depth_eval and social_score >= 50

    return {
        "result": full_result.strip(),
        "feedback": feedback_summary["feedback"].strip(),
        "valid": is_valid
    }


