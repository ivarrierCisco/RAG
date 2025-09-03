from graph_connection import query_data

class ProductQueryService:
    def __init__(self):
        self.endpoint = "https://d06b233f791b24458934.sandbox.graphwise.ai/repositories/Products_Isha"

    def query_basic_info(self):
        query = "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 5"
        return self.execute_query(query)

    def query_skos_concepts(self):
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
          ?c a skos:Concept ; skos:prefLabel ?label .
        }
        LIMIT 5
        """
        return self.execute_query(query)

    def execute_query(self, query):
        try:
            result = query_data(query)
            return result.get("results", {}).get("bindings", [])
        except Exception as e:
            print(f"Query execution failed: {e}")
            return []