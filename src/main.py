from sentence_transformers import SentenceTransformer
import chromadb
from graph_connection import get_schema_info, query_data
from sparql_generator import getSPARQLQuery
from graph_connection import run_sparql
# from vector_search import search_chromadb
from answer_generator import generate_answer


def main():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.PersistentClient(path="./chroma_db")
    schema_info = get_schema_info()

    while True:
        question = input("\n🔎 Ask a question (or type 'exit' to quit): ").strip()
        if question.lower() in {"exit", "quit"}:
            print("👋 Exiting. Goodbye!")
            break

        query_embedding = model.encode([question])
        sparql_query = get_sparql_query(question, schema_info)
        sparql_result = run_sparql(sparql_query)
        vector_context = search_chromadb(client, query_embedding)
        answer = generate_answer(question, sparql_result, vector_context)
        print("\n💬 Answer:")
        print(answer)

# if __name__ == "__main__":
#     main()

def test_schema():
    print("Testing schema info retrieval...")
    schema_info = get_schema_info()
    print(schema_info)
    return schema_info

def test_sparql_generation(question, schema_info):
    print(f"Testing SPARQL query generation for: '{question}'")
    sparql_query = getSPARQLQuery(question, schema_info)  # Pass schema_info here
    print("Generated SPARQL query:")
    print(sparql_query)
    print("Testing query execution...")
    result = query_data(sparql_query)
    print("SPARQL query result:")
    print(result)

if __name__ == "__main__":
    schema_info = test_schema()
    test_question = "List all Cisco product concepts"
    test_sparql_generation(test_question, schema_info)