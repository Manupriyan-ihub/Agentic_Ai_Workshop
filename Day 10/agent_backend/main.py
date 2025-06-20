from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Optional: Create a request schema (if needed)
class VerifyRequest(BaseModel):
    data: str

# Optional: Create a response schema (if needed)
class VerifyResponse(BaseModel):
    result: str
    valid: bool

@app.post("/verify", response_model=VerifyResponse)
async def verify(payload: VerifyRequest):
    # Dummy logic for verification
    if "ok" in payload.data.lower():
        return {"result": "Verified", "valid": True}
    else:
        return {"result": "Not Verified", "valid": False}
