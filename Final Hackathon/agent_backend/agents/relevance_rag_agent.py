from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
import os
import re

load_dotenv()

# ✅ 1. LLM Initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
)

# ✅ 2. Search Tool
search_tool = TavilySearchResults(k=5, api_key=os.getenv("TAVILY_API_KEY"))

# ✅ 3. Prompt Template
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

# ✅ 4. LangChain Tool Function
def relevance_eval_tool_func(input: dict) -> str:
    article = input.get("article", "")
    title = input.get("title", "")
    snippets = input.get("snippets", "")
    chain = relevance_prompt | llm
    result = chain.invoke({"article": article, "title": title, "snippets": snippets})
    return result.content if hasattr(result, "content") else str(result)

# ✅ 5. Tool Definition
relevance_tool = Tool(
    name="RelevanceEvaluator",
    func=relevance_eval_tool_func,
    description="Evaluates how relevant an article is to its title using search snippets."
)

# ✅ 6. Agent Executor
relevance_agent = initialize_agent(
    tools=[relevance_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ✅ 7. Final Agent Wrapper
def run_okr_relevance_agent(article: str, title: str):
    results = search_tool.run(title)
    snippets = "\n".join(res["content"] for res in results)

    # Run the chain manually instead of agent
    chain = relevance_prompt | llm
    output = chain.invoke({
        "article": article,
        "title": title,
        "snippets": snippets
    })

    output_text = output.content if hasattr(output, "content") else str(output)

    match = re.search(r"Score:\s*(\d+)", output_text)
    score = int(match.group(1)) if match else 0

    return {
        "relevance_score": score,
        "justification": output_text.strip()
    }

