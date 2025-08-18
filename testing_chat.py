import requests, json
import os, certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from SPARQLWrapper import SPARQLWrapper, JSON

HOST = "https://d06b233f791b24458934.sandbox.graphwise.ai"
REPO = "Products_Isha"
ENDPOINT = f"{HOST}/repositories/{REPO}"

def obtain_token(host: str, username: str, password: str) -> str:
    r = requests.post(f"{host}/rest/login",
                      json={"username": username, "password": password},
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
    # Returns value like "Bearer eyJ..."
    return r.headers["Authorization"]

TOKEN = obtain_token(HOST,"ishavarrier@gmail.com", "xZe}&Nd6T5")

def test_connection():
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setMethod("POST")
    sparql.setReturnFormat(JSON)
    sparql.setQuery("SELECT (1 AS ?ok) WHERE {} LIMIT 1")
    # IMPORTANT: TOKEN already includes "Bearer ..."
    sparql.addCustomHttpHeader("Authorization", TOKEN)
    print(sparql.query().convert())

def query_data(query: str):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setMethod("POST")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    sparql.addCustomHttpHeader("Authorization", TOKEN)
    return sparql.query().convert()

if __name__ == "__main__":
    # Optional: list repos
    print(requests.get(f"{HOST}/repositories",
                       headers={"Authorization": TOKEN,
                                "Accept": "application/json"}).text)

    q = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?concept ?label
    WHERE {
      ?concept a skos:Concept ;
               skos:prefLabel ?label .
    }
    LIMIT 20
    """
    print(query_data(q))
