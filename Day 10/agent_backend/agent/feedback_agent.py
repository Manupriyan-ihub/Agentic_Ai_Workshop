from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.7)

def generate_feedback(final_result: str) -> dict:
    prompt = f"""
You are an educational assistant AI that evaluates student-posted LinkedIn articles for learning outcome alignment.

Given the following combined output from multiple assessment agents:

--- BEGIN AGENT RESULT ---
{final_result}
--- END AGENT RESULT ---

Please do the following:

1. Extract and display a **score breakdown**:
   - Relevance (0–100)
   - Insight (0–100) — based on depth/originality evaluation
   - Engagement (0–100) — based on the social impact score

2. Compute and display the **average score** across the 3.

3. Generate a **reflection prompt** like:  
   > “How could this post better showcase your capstone project?”

4. Provide **2-3 specific improvement suggestions** to increase the post’s value.

Respond in this format:

Score Breakdown:
- Relevance: <x>/100
- Insight: <y>/100
- Engagement: <z>/100
- Average: <avg>/100

Reflection Prompt:
"<prompt>"

Improvement Suggestions:
1. <suggestion>
2. <suggestion>
3. <optional suggestion>
"""

    response = llm.invoke(prompt)
    return {"feedback": response.content}
