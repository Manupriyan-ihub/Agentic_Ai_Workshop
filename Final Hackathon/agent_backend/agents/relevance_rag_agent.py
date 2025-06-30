from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os
import re

load_dotenv()

# 1. LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
)

# 2. Search Tool
search_tool = TavilySearchResults(k=5, api_key=os.getenv("TAVILY_API_KEY"))

# 3. Updated Prompt Template
relevance_prompt = PromptTemplate.from_template("""
You're a relevance evaluator. A user has written an article titled:

"{title}"

We fetched the top web search snippets for this topic. Compare them with the article content below:

ARTICLE:
-------------------
{article}
-------------------

SEARCH SNIPPETS:
-------------------
{snippets}
-------------------

Your task:
1. Evaluate how well the article aligns with its title and the search snippets.
2. Assign a relevance score on a scale of 0–100.
   - 90–100: Highly relevant and informative
   - 60–89: Moderately relevant with some depth
   - 30–59: Partially relevant or off-topic
   - 0–29: Poorly aligned or irrelevant

Respond in **this format only**:

Score: <number out of 100>  
Justification: <brief explanation>
""")


# 4. Agent Function
def run_okr_relevance_agent(article: str, title: str):
    # Step 1: Get Web Search Results
    results = search_tool.run(title)
    snippets = "\n".join(res["content"] for res in results)

    # Step 2: Send to LLM
    chain = relevance_prompt | llm
    output = chain.invoke({"article": article, "title": title, "snippets": snippets})
    output_text = output.content if hasattr(output, "content") else str(output)

    # Step 3: Extract score
    match = re.search(r"Score:\s*(\d+)", output_text)
    score = int(match.group(1)) if match else 0

    return {
        "relevance_score": score,
        "justification": output_text.strip()
    }

