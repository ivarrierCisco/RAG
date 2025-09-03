import streamlit as st
import json
from sentence_transformers import SentenceTransformer
import chromadb
from vector_search import search_documents
from services.product_query_service import ProductQueryService
from sparql_generator import getSPARQLQuery
import requests
from graph_connection import get_schema_info, query_data

st.title("Cisco Knowledge Hub")

# Cache schema info for efficiency
@st.cache_resource
def load_schema():
    return get_schema_info()

schema_info = load_schema()

@st.cache_resource
def get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def get_client():
    return chromadb.PersistentClient(path="./chroma_db")

model = get_model()
client = get_client()
product_service = ProductQueryService()

question = st.text_input("Ask a question about Cisco products:")
def generate_final_answer(question, sparql_result, vector_context):
    prompt = f"""
    You are an expert on Cisco products.
    User question: {question}
    SPARQL result: {sparql_result}
    Context from documents: {vector_context}
    Provide a concise, helpful answer for the user.
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt}
    )
    # Print raw response for debugging
    print("Raw response text:", response.text)
    # If multiple JSON objects, take the first one
    answer_chunks = []
    for line in response.text.split('\n'):
        if line.strip():
            try:
                obj = json.loads(line)
                if "response" in obj:
                    answer_chunks.append(obj["response"])
            except Exception as e:
                print(f"Error parsing line: {line}\n{e}")
    return "".join(answer_chunks)

if question:
    query_embedding = model.encode([question])
    sparql_query = getSPARQLQuery(question, schema_info)  
    print(sparql_query)
    sparql_result = product_service.execute_query(sparql_query)
    vector_context = "providing dummy context for now"
    final_answer = generate_final_answer(question, sparql_result, vector_context)
    st.subheader("Answer")
    st.write(final_answer)

def search_chromadb(client, query_embedding, top_k=3):
    collection = client.get_collection("your_collection_name")
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )
    return results['documents']

