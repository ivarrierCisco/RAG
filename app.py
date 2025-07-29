import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import requests 


if __name__ == "__main__":
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.PersistentClient(path="./chroma_db")
    client.delete_collection(name="trial_rag_data")
    collection = client.create_collection(name="trial_rag_data")

    def setup():
    #in this function, we will setup the chromaDB and conduct the text preprocessing
        text = '''Diya Varrier is a girl
        She is turning 17 on September 10. 
        She's good at making chai, and she also can be sassy. 
        Diya is testing out the context/hallucinations of this LLM
        Is Diya able to pass the tests?'''
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)
        embeddings = model.encode(chunks)

        for i, (text,embedding) in enumerate(zip(chunks,embeddings)):
            collection.add(documents=[text], embeddings=[embedding.tolist()], ids=[f"id_{i}"])
    

    if collection.count() == 0:
        setup()
    

    query = input("What is your query?")
    query_embedding = model.encode([query])
    

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=2,
        include=["documents", "distances"]
    )

    # Use a relevance threshold (tune this as needed, e.g., 0.3 to 0.5)
    threshold = 0.9


    # Only use context if it's relevant enough
    relevant_context = ""
    if results['distances'][0][0] < threshold:
        relevant_context = "\n".join(results['documents'][0])

    prompt = f"""
        You are a helpful assistant. Use the context below to answer the question only if it's directly relevant. 
        If the context is not useful, use your own knowledge. 
        Keep the answer concise and factual.

        Context:
        {relevant_context if relevant_context else '[No useful context]'}

        Question: {query}
        Answer:"""


    full_response = ""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model":"llama3", "prompt": prompt}
    )
    for chunk in response.iter_lines():
        if chunk:
            data = json.loads(chunk.decode())
            if 'response' in data:
                full_response += data['response']

    print(full_response.strip())


