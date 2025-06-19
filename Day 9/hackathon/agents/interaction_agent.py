from langchain.chains import RetrievalQA

def check_interaction(rag_chain: RetrievalQA, endorsements: str, events: str) -> str:
    prompt = f"""
    A LinkedIn connection has the following interactions:
    - Endorsements: "{endorsements}"
    - Events Attended Together: "{events}"

    Do these suggest a professional engagement with this person?
    Answer with "Yes" or "No", and justify your answer.
    """
    return rag_chain.run(prompt)
