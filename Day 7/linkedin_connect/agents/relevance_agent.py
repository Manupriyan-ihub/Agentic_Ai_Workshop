from langchain.chains import RetrievalQA

def check_relevance(rag_chain: RetrievalQA, title: str, domain: str = "AI, Software, or EdTech") -> str:
    prompt = f"""
    A LinkedIn connection has the title: "{title}".
    Would you classify this person as being part of the {domain} domain?
    Answer with "Yes" or "No", followed by a brief reason.
    """
    return rag_chain.run(prompt)
