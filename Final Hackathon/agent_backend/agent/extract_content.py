from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from bs4 import BeautifulSoup
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ✅ Async function to fetch and extract content
async def extract_from_linkedin_async(url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True, timeout=10)
            response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch the URL: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")
    article_text = " ".join([p.text for p in soup.find_all("p")])[:4000]

    metadata = {
        "title": soup.title.string if soup.title else "Unknown",
        "meta_description": soup.find("meta", attrs={"name": "description"})["content"]
        if soup.find("meta", attrs={"name": "description"}) else "None"
    }

    prompt = f"""Given this article text from LinkedIn:

{article_text}

Extract and return the following:
- Article Content
- Author (if mentioned)
- Publish date (if mentioned)
- Number of likes
- Comments
"""

    result = llm.invoke([HumanMessage(content=prompt)])

    return {
        "summary": result.content,
        "metadata": metadata
    }

# ✅ Synchronous wrapper for agent (used only by LangChain Tool if needed)
def extract_from_linkedin_sync(url: str) -> str:
    # ONLY call this in non-async (CLI or test script)
    return "This sync function is not used in FastAPI context."

# ✅ Register tool for CLI use only (not used by FastAPI right now)
tools = [
    Tool(
        name="LinkedInExtractorTool",
        func=extract_from_linkedin_sync,
        description="Extracts article content and metadata from a LinkedIn URL"
    )
]

# ✅ Create agent (optional if you don't use LangChain agent flow)
linkedin_extraction_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ✅ This is what your FastAPI endpoint should call
async def run_linkedin_extraction_agent(url: str):
    extracted = await extract_from_linkedin_async(url)
    return {"extracted": extracted}
