# sparql queries that will be used on diagram layout

dl_primitive_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dl: <http://iec.ch/TC57/ns/CIM/DiagramLayout-EU#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?datatype ?label ?comment ?definition ?package
WHERE {
    # Capture datatypes marked with dl:isPrimitive
    ?datatype dl:isPrimitive "True" .
    OPTIONAL { ?datatype rdfs:label ?label . }
    OPTIONAL { ?datatype skos:definition ?definition . }
    OPTIONAL { ?datatype dl:Package ?package . }
}
"""
