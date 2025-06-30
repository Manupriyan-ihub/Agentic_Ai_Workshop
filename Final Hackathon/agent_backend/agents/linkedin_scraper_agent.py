from bs4 import BeautifulSoup
import httpx
import re
from datetime import datetime
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# ✅ Clean boilerplate
def clean_article_text(text: str) -> str:
    patterns_to_remove = [
        r"(?i)Agree\s*&?\s*Join LinkedIn.*?(?=Whether|If you're|get started)",
        r"(?i)By clicking Continue.*?Cookie Policy\.",
        r"(?i)Create your free account.*?search",
        r"(?i)New to LinkedIn\?Join now",
        r"(?i)To view or add a comment,sign in",
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text)
    return text.strip()

# ✅ Main scraping function
async def extract_linkedin_content(url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True, timeout=10)
            response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch URL: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Article content
    article_content = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
    article_content = clean_article_text(article_content)

    # Likes
    likes_btn = soup.find("button", attrs={"aria-label": re.compile(r"\d+\s+reactions")})
    likes = re.search(r"(\d+)\s+reactions", likes_btn["aria-label"]).group(1) if likes_btn else "0"

    # Comments
    comments_btn = soup.find("button", attrs={"aria-label": re.compile(r"\d+\s+comments?")})
    comments = re.search(r"(\d+)\s+comments?", comments_btn["aria-label"]).group(1) if comments_btn else "0"

    # Publish date
    time_tag = soup.find("time", class_="text-body-small-open t-black--light")
    if time_tag:
        try:
            publish_date = datetime.strptime(time_tag.get_text(strip=True), "%B %d, %Y").date().isoformat()
        except ValueError:
            publish_date = time_tag.get_text(strip=True)
    else:
        publish_date = "Not found"

    # Author name
    author_tag = soup.find("h2", class_="text-heading-medium")
    author = author_tag.get_text(strip=True) if author_tag else "Not found"

    # Author bio
    bio_tag = soup.find("div", class_="lt-line-clamp lt-line-clamp--multi-line text-body-small t-black--light break-words")
    author_bio = bio_tag.get_text(strip=True) if bio_tag else "Not found"

    return {
        "article_content": article_content[:4000].strip(),
        "likes": likes,
        "comments": comments,
        "publish_date": publish_date,
        "author": author,
        "author_bio": author_bio,
    }

# ✅ LangChain-compatible wrapper (sync for tool)
def extract_linkedin_tool_wrapper(url: str) -> str:
    import asyncio
    result = asyncio.run(extract_linkedin_content(url))
    return str(result)

# ✅ Tool definition
linkedin_scrape_tool = Tool(
    name="LinkedInScraper",
    func=extract_linkedin_tool_wrapper,
    description="Extracts content, stats, and metadata from a LinkedIn article URL."
)

# ✅ Initialize agent (if needed in other files)
linkedin_scrape_agent_executor: AgentExecutor = initialize_agent(
    tools=[linkedin_scrape_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
