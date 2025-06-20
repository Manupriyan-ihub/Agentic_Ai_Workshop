import httpx
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

async def extract_from_linkedin(url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True, timeout=10)
            response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch the URL: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Try to get text content from LinkedIn article
    article_text = " ".join([p.text for p in soup.find_all("p")])[:4000]

    metadata = {
        "title": soup.title.string if soup.title else "Unknown",
        "meta_description": soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "None"
    }

    # Ask Gemini to summarize and analyze
    prompt = f"""Given this article text from LinkedIn:
    
    {article_text}

    Extract and return the following:
    - Article Content
    - Author (if mentioned)
    - Publish date (if mentioned)
    - Number of likes
    - Comments
    """

#    data['summary']

    result = llm.invoke([HumanMessage(content=prompt)])
    # resul = result.json()["Article Content:"]
    return {
        "summary": result.content,
        "metadata": metadata
    }
