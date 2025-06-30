from bs4 import BeautifulSoup
import httpx
import re
from datetime import datetime
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Utility: Clean LinkedIn login boilerplate
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

# Prompt Template for article extraction (could be extended for summary if needed)
linkedin_extraction_prompt = PromptTemplate.from_template("""
You are an HTML content extractor.
From the raw HTML of a LinkedIn article, extract the full article content as clean text (no HTML tags), avoiding LinkedIn boilerplate login prompts.

RAW HTML:
---------------------
{html}
---------------------

Return only the clean article text.
""")

# Function to extract article + metadata from LinkedIn page
async def extract_linkedin_content(url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True, timeout=10)
            response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch URL: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract and clean article content
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

# # (Optional) Wrap as LangChain Tool — if you ever want to integrate it into an agent:
# linkedin_scrape_tool = Tool(
#     name="LinkedInScraper",
#     func=lambda url: extract_linkedin_content(url),
#     description="Extracts article content, metadata, and stats from a LinkedIn article URL"
# )
