from langchain.chains import RetrievalQA

def check_messages(rag_chain: RetrievalQA, messages: str) -> str:
    prompt = f"""
    These are the messages exchanged with a LinkedIn connection: "{messages}".
    Is this a meaningful exchange that indicates a professional connection?
    Answer with "Yes" or "No", and explain briefly.
    """
    return rag_chain.run(prompt)
