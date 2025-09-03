import requests

def generate_answer(question, sparql_result, vector_context):
    prompt = f"""
    You are an expert on Cisco products.
    User question: {question}
    SPARQL result: {sparql_result}
    Context from documents: {vector_context}
    Provide a concise, helpful answer.
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt}
    )
    return response.json().get("response", "")