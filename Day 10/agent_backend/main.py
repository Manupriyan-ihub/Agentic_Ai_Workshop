from fastapi import FastAPI
from pydantic import BaseModel
from agent.extract_content import extract_from_linkedin
from agent.relevance_rag_agent import check_relevance

app = FastAPI()

class VerifyRequest(BaseModel):
    url: str
    article_title: str

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
    
    print(extraction_result)

    article_text = extraction_result.get("summary", "")

    # Step 2: OKR Relevance Agent
    relevance_result = check_relevance(article_text, payload.article_title)

    return {
        "result": relevance_result,
        "valid": "relevant" in relevance_result.lower() or "aligned" in relevance_result.lower()
    }
