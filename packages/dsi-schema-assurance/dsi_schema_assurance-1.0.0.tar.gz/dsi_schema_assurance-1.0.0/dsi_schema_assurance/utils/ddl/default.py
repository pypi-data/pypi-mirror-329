# sparql queries that will be used by default

default_primitive_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?datatype ?label ?comment
WHERE {
    # Capture datatypes from rdfs:range, filtered for xsd datatypes
    ?property rdfs:range ?datatype .
    FILTER(STRSTARTS(STR(?datatype), "http://www.w3.org/2001/XMLSchema#"))
    OPTIONAL { ?datatype rdfs:label ?label . }
    OPTIONAL { ?datatype rdfs:comment ?comment . }
}
"""

default_dtypes_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?datatype ?stereotype
WHERE {
    ?property rdfs:range ?datatype .
}
"""

default_shacl_query = """
PREFIX sh: <http://www.w3.org/ns/shacl#>

SELECT DISTINCT ?property ?datatype
WHERE {
  {
    # Case 1: Nested under a shape
    ?shape sh:property ?propertyShape .
    ?propertyShape sh:path ?property ;
                   sh:datatype ?datatype .
  }
  UNION
  {
    # Case 2: Standalone PropertyShape
    ?propertyShape rdf:type sh:PropertyShape ;
                   sh:path ?property ;
                   sh:datatype ?datatype .
  }
}
"""
