import os
from sentence_transformers import SentenceTransformer
import chromadb

def load_documents(folder_path):
    docs = []
    doc_ids = []
    for fname in os.listdir(folder_path):
        if fname.endswith(".txt"):
            with open(os.path.join(folder_path, fname), "r") as f:
                docs.append(f.read())
                doc_ids.append(fname)
    return docs, doc_ids

def build_chroma_collection(docs, doc_ids, collection_name="my_collection"):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(collection_name)
    # Only vectorize and add if collection is empty
    if len(collection.get(ids=doc_ids)['ids']) == 0:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(docs)
        collection.add(
            documents=docs,
            embeddings=embeddings.tolist(),
            ids=doc_ids
        )
    return collection

def search_documents(collection, query, top_k=3):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query])
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )
    return results['documents']

if __name__ == "__main__":
    folder = "path/to/your/text_files"
    docs, doc_ids = load_documents(folder)
    collection = build_chroma_collection(docs, doc_ids)
    query = input("Enter your search query: ")
    results = search_documents(collection, query)
    print("Top results:")
    for doc in results:
        print(doc)