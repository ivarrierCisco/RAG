import requests
import json

def getSPARQLQuery(query, schema_info):
    prompt = f"""You are a SPARQL query generator for a SKOS-based ontology where most data uses prefLabel.
        Convert natural language questions to SPARQL queries.

        SCHEMA INFORMATION:
        {schema_info}

        IMPORTANT: This ontology uses skos:prefLabel for most displayable text.

        COMMON PATTERNS FOR PREFLABEL-BASED ONTOLOGY:
        - For "all concepts": SELECT ?concept ?label WHERE {{ ?concept a skos:Concept . ?concept skos:prefLabel ?label }}
        - For "concepts containing X": Use FILTER(CONTAINS(LCASE(?label), "x"))
        - For hierarchical relationships: Use skos:broader, skos:narrower
        - For schemes: Use skos:ConceptScheme and skos:hasTopConcept

        EXAMPLES FOR PREFLABEL-BASED ONTOLOGY:
        Question: "What are all the concepts?"
        SPARQL: PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?concept ?label WHERE {{
        ?concept a skos:Concept .
        ?concept skos:prefLabel ?label
        }}

        Question: "Show me concepts with 'switch' in the name"
        SPARQL: PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?concept ?label WHERE {{
        ?concept a skos:Concept .
        ?concept skos:prefLabel ?label .
        FILTER(CONTAINS(LCASE(?label), "switch"))
        }}

        Question: "Find concepts related to electronics"
        SPARQL: PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?concept ?label WHERE {{
        ?concept a skos:Concept .
        ?concept skos:prefLabel ?label .
        FILTER(CONTAINS(LCASE(?label), "electronic"))
        }}

        Question: "What concepts are broader than X?"
        SPARQL: PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?broader ?broaderLabel WHERE {{
        ?concept skos:prefLabel "X" .
        ?concept skos:broader ?broader .
        ?broader skos:prefLabel ?broaderLabel
        }}

        Question: "Show me all top-level concepts"
        SPARQL: PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?concept ?label WHERE {{
        ?concept a skos:Concept .
        ?concept skos:prefLabel ?label .
        ?scheme skos:hasTopConcept ?concept
        }}

        NOW CONVERT THIS QUESTION:
        Question: {query}

        REQUIREMENTS:
        1. Include necessary PREFIX declarations
        2. Use OPTIONAL for labels that might not exist
        3. Use FILTER for text matching when needed
        4. Return only valid SPARQL syntax
        5. No explanations, just the query

        SPARQL:"""

    full_response = ""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt},
            stream=True
        )
        for chunk in response.iter_lines():
            if chunk:
                data = json.loads(chunk.decode())
                if 'response' in data:
                    full_response += data['response']
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during generation: {e}")
        

    print("\n💬 Answer:")
    print(full_response.strip())
    return full_response