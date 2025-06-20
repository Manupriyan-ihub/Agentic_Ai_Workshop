from langchain_google_genai import ChatGoogleGenerativeAI
import re

llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.5)

def assess_social_impact(summary: str) -> int:
    prompt = f"""
You are a social media analysis agent.

Given the content of a LinkedIn article summary, assess its organic social impact on a scale of 0 to 100 based on:

1. Whether the article is likely to attract Likes, Comments, and Shares.
2. The potential for high-quality (substantive) comments vs. generic ones.
3. Usage of tags, mentions, or indicators of network amplification.

### Article Summary:
\"\"\"
{summary}
\"\"\"

Give your score as a single integer from 0 to 100, followed by a brief justification.
Format:
Score: <number>
Reason: <short explanation>
"""

    response = llm.invoke(prompt)
    response_text = response.content if hasattr(response, "content") else str(response)
    match = re.search(r"Score:\s*(\d+)", response_text)

    
    # # Extract score safely
    # import re
    # match = re.search(r"Score:\s*(\d+)", response)
    score = int(match.group(1)) if match else 0
    return score
