# Module that will be used to inject data types into the RDF/XML file

import re

from typing import Dict

from xml.etree.ElementTree import ElementTree

from dataclasses import dataclass


@dataclass
class Namespaces:
    rdf: str = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xsd: str = "http://www.w3.org/2001/XMLSchema#"


def rdf_dtype_injector(data: str, schema_registry: Dict[str, str]) -> ElementTree:
    """
    Inject data types into the RDF/XML file.

    This function will inject data types into the RDF/XML file based on the schema registry - that
    was obtained from the ontology files.

    _Operation Example_:
    >>> data = "
    ... <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    ...          xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    ...          xmlns:ex="http://example.com/ontology/people#">
    ...     <rdf:Description rdf:about="http://example.com/ontology/people#person1">
    ...         <rdf:type rdf:resource="http://example.com/ontology/people#Person"/>
    ...         <ex:id>1</ex:id>
    ...     </rdf:Description>
    ... </rdf:RDF>
    ... "
    >>> schema_registry = {
    ...     "http://example.com/ontology/people#id": "http://www.w3.org/2001/XMLSchema#integer",
    ... }
    >>> injector(data, schema_registry)
    >>> "
    >>> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    ...          xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    ...          xmlns:ex="http://example.com/ontology/people#">
    ...     <rdf:Description rdf:about="http://example.com/ontology/people#person1">
    ...         <ex:id rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</ex:id>
    ...     </rdf:Description>
    ... </rdf:RDF>
    ... "

    Args:
        data (str): The RDF/XML file to inject data types into.
        schema_registry (Dict[str, str]): The schema registry obtained from the ontology files.

    Returns:
        ElementTree: The RDF/XML file with data types injected.
    """

    for element in data.iter():
        rdf_about = element.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")

        if rdf_about and rdf_about.startswith("file://"):
            sanitized_about = re.sub(r"^file://.*?#", "#", rdf_about)
            element.set(
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about", sanitized_about
            )

        dtype = schema_registry.get(element.tag.split("}")[-1], None)

        if dtype:
            element.set(f"{{{Namespaces.rdf}}}datatype", f"{Namespaces.xsd}{dtype}")

    return data
