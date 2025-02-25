# sparql queries that will be used on cim

cim_primitive_query = """
PREFIX cims: <http://iec.ch/TC57/1999/rdf-schema-extensions-19990926#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?datatype ?label ?comment ?definition ?package
WHERE {
    # Capture datatypes explicitly marked as Primitive (using cims:stereotype)
    ?datatype cims:stereotype "Primitive" .
    OPTIONAL { ?datatype rdfs:label ?label . }
    OPTIONAL { ?datatype rdfs:comment ?comment . }
}
"""

cim_dtypes_query = """
PREFIX cims: <http://iec.ch/TC57/1999/rdf-schema-extensions-19990926#>
PREFIX cim: <http://iec.ch/TC57/NonStandard/UML#>

SELECT ?property ?datatype ?stereotype
WHERE {
  {
    ?property cims:dataType ?datatype .
    OPTIONAL {
      ?datatype cims:stereotype ?stereotype .
    }
  }
  UNION
  {
    ?property cim:dataType ?datatype .
    OPTIONAL {
      ?datatype cim:stereotype ?stereotype .
    }
  }
}
"""
