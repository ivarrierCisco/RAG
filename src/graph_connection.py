#src/graph_connection.py
#This script tests the connection to a SPARQL endpoint and performs various queries to validate functionality.
 
import os
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.error
import socket

import requests, json
import os, certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from SPARQLWrapper import SPARQLWrapper, JSON
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.getenv("GRAPHDB_USERNAME")
PASSWORD = os.getenv("GRAPHDB_PASSWORD")

HOST = "https://g6831df228af54262ad4.sandbox.graphwise.ai"
REPO = "Cisco_Products"
ENDPOINT = f"{HOST}/repositories/{REPO}"

def obtain_token(host: str, username: str, password: str) -> str:
    r = requests.post(f"{host}/rest/login",
                      json={"username": username, "password": password},
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
    # Returns value like "Bearer eyJ..."
    return r.headers["Authorization"]

TOKEN = obtain_token(HOST,USERNAME, PASSWORD)

def get_schema_info():
    print("Retrieving schema info...")
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setMethod("POST")
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?scheme ?schemeLabel ?topConcept ?topLabel ?concept ?conceptLabel WHERE {
        ?scheme a skos:ConceptScheme .
        OPTIONAL { ?scheme skos:prefLabel ?schemeLabel }
        OPTIONAL {
            ?scheme skos:hasTopConcept ?topConcept .
            OPTIONAL { ?topConcept skos:prefLabel ?topLabel }
            OPTIONAL {
                ?topConcept skos:narrower* ?concept .
                ?concept skos:prefLabel ?conceptLabel
            }
        }
    }
    """)
    sparql.addCustomHttpHeader("Authorization", TOKEN)
    result = sparql.query().convert()
    print("Raw schema info:", result)  # For debugging
    return result  # Return the schema info to main.py

def test_connection():
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setMethod("POST")
    sparql.setReturnFormat(JSON)
    sparql.setQuery("SELECT (1 AS ?ok) WHERE {} LIMIT 1")
    # IMPORTANT: TOKEN already includes "Bearer ..."
    sparql.addCustomHttpHeader("Authorization", TOKEN)
    results = sparql.query().convert()
    print("these r the results", json.dumps(results, indent=2))
    return results

def query_data(query: str):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setMethod("POST")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    sparql.addCustomHttpHeader("Authorization", TOKEN)
    return sparql.query().convert()


def run_sparql(query: str, timeout_s: int = 15):
    s = SPARQLWrapper(ENDPOINT)
    s.setReturnFormat(JSON)
    s.setMethod("POST")
    s.setQuery(query)
    
    s.setTimeout(timeout_s)
    
    if TOKEN:
        s.addCustomHttpHeader("Authorization", f"Bearer {TOKEN}")
    
    try:
        return s.queryAndConvert()
    except urllib.error.HTTPError as e:
        print(f"[HTTP {e.code}] {e.reason}", file=sys.stderr)
        if e.code == 401:
            print("This might indicate authentication is required. Check if you need a token.", file=sys.stderr)
        elif e.code == 404:
            print("Repository not found. Check your endpoint URL.", file=sys.stderr)
        raise
    except socket.timeout:
        print(f"[Timeout] Query timed out after {timeout_s} seconds", file=sys.stderr)
        raise
    except Exception as e:
        print(f"[Error] {e}", file=sys.stderr)
        raise

def test_basic_connection():
    print(f"Endpoint: {ENDPOINT}")
    print("Testing basic connection...")
    
    try:
        result = run_sparql("ASK WHERE { ?s ?p ?o }")
        print("✓ Basic connection successful")
        return True
    except Exception as e:
        print(f"✗ Basic connection failed: {e}")
        return False

def test_simple_select():
    print("\nTesting simple SELECT query...")
    try:
        result = run_sparql("SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 5")
        bindings = result.get("results", {}).get("bindings", [])
        if bindings:
            print(f"✓ Found {len(bindings)} triples")
            for binding in bindings[:3]:
                s = binding.get("s", {}).get("value", "")
                p = binding.get("p", {}).get("value", "")
                o = binding.get("o", {}).get("value", "")
                print(f"  {s} -> {p} -> {o}")
        else:
            print("✓ Query executed but no results returned")
        return True
    except Exception as e:
        print(f"✗ Simple SELECT failed: {e}")
        return False

def test_skos_concepts():
    print("\nTesting SKOS concepts...")
    q = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?c ?label
    WHERE {
      ?c a skos:Concept ; skos:prefLabel ?label .
    }
    LIMIT 5
    """
    try:
        res = run_sparql(q)
        bindings = res.get("results", {}).get("bindings", [])
        if bindings:
            print(f"✓ Found {len(bindings)} SKOS concepts:")
            for b in bindings:
                concept = b.get("c", {}).get("value", "")
                label = b.get("label", {}).get("value", "")
                print(f"  {concept} — {label}")
        else:
            print("No SKOS concepts found (might not be SKOS data)")
        return True
    except Exception as e:
        print(f"✗ SKOS query failed: {e}")
        return False

def test_repository_info():
    print("\nTesting repository information...")
    
    try:
        result = run_sparql("SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }")
        count = result.get("results", {}).get("bindings", [{}])[0].get("count", {}).get("value", "0")
        print(f"✓ Total triples in repository: {count}")
    except Exception as e:
        print(f"✗ Could not count triples: {e}")
    
    try:
        q = """
        SELECT DISTINCT ?class (COUNT(?instance) AS ?count)
        WHERE {
          ?instance a ?class .
        }
        GROUP BY ?class
        ORDER BY DESC(?count)
        LIMIT 10
        """
        result = run_sparql(q)
        bindings = result.get("results", {}).get("bindings", [])
        if bindings:
            print("✓ Top classes in your data:")
            for b in bindings:
                cls = b.get("class", {}).get("value", "")
                count = b.get("count", {}).get("value", "0")
                print(f"  {cls}: {count} instances")
        else:
            print("No typed instances found")
    except Exception as e:
        print(f"✗ Could not get class info: {e}")