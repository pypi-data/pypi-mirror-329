<h1 align='center'>
    <strong> Schema Validation </strong>
</h1>

<p align='center'>
    Validate your RDF data against an ontology and SHACL files - even when the data instance lacks datatypes definition.
</p>


<div align="center">

  <a href="code coverage">![coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)</a>
  <a href="tests">![tests](https://img.shields.io/badge/tests-76%20passed%2C%200%20failed-brightgreen)</a>
  <a href="python version">![sbt_version](https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=white)</a>
  <a href="https://pypi.org/project/dsi-schema-assurance/">![PyPI](https://img.shields.io/pypi/v/dsi-schema-assurance)</a>

</div>

## **1. Intro**

The Resource Description Framework (RDF) is a method to describe and exchange graph data.

An RDF data instance can be complemented with two additional artefacts that enable RDF schema validation:

- **Ontology**: describes the concepts and resources of a data instance using RDF language and allows for the detection of logically impossible assertions in the model.
- **SHACL (Shapes Constraint Language)**: a W3C standard that describes and validates the contents of RDF graphs instances.

Sometimes RDF data might lack datatypes definition. Under these circumstances, W3C states that when no datatype is specified, the data is by default considered `Literal` (the equivalent of a `string`).

These can be tricky. In that scenario, a standard validation will not produce the desired validation outcome. It can also be especially challenging when the data instance cannot be altered to comply with the W3C standard, be it by the standard definition (e.g., CIM), or by the inability to alter the source system to add the datatypes.

This is where the Schema Validation comes in. It dynamically injects the datatypes into the data instance, inferring the datatypes by navigating the hierarchy, and validates it against the desired ontologies and SHACL files.

### **1.1. Ontologies vs SHACLs**

Ontologies provide **inference rules, but they do not enforce constrains** in the same way SHACLs do. Which means that the **validation is only as good as the SHACL provided.**

Taking this into account, the package **will always prioritize the SHACLs** when it comes to the datatypes definition, however, the inference of these datatypes will be created as a result of a cross-check between the ontologies and the SHACLs, when selected by the user.

This is why the package has two hunters: one for the ontologies and another one for the SHACLs. When there's conflicts between the results obtained by them, the ones produced by the SHACLs will be the ones considered.

## **2. How to Use - _high level_**

There's three way to use the Schema Validation package: (1) default queries, (2) custom queries, and (3) list of custom queries that will be executed sequentially.

**_Option 1_ - Default queries**

The package has a set of default queries used to capture and extract the datatypes that will be leveraged if no query is provided by the user.

```python
from rdflib import Graph

from dsi_schema_assurance import SchemaCertifier

data_graph = Graph()
data_graph.parse(data_path, format='xml')

shacl_graph = Graph()
shacl_graph.parse(shacl_path, format='turtle')

ont_graph = Graph()
ont_graph.parse(ont_path, format='xml')

validation_result = SchemaCertifier(
    data_graph=data_graph,
    shacl_graph=shacl_graph,
    ont_graph=ont_graph,
    inference_type="both"
).run()
```

**_Option 2_ - Custom query**

```python
from rdflib import Graph

from dsi_schema_assurance import SchemaCertifier

data_graph = Graph()
data_graph.parse(data_path, format='xml')

shacl_graph = Graph()
shacl_graph.parse(shacl_path, format='turtle')

ont_graph = Graph()
ont_graph.parse(ont_path, format='xml')

ont_query = """
[CUSTOM QUERY]
"""

validation_result = SchemaCertifier(
    data_graph=data_graph,
    shacl_graph=shacl_graph,
    ont_graph=ont_graph,
    ont_query=ont_query,
    inference_type="both"
).run()
````

**_Option 3_ - List of custom queries**

```python
from rdflib import Graph

from dsi_schema_assurance import SchemaCertifier

data_graph = Graph()
data_graph.parse(data_path, format='xml')

shacl_graph = Graph()
shacl_graph.parse(shacl_path, format='turtle')

ont_graph = Graph()
ont_graph.parse(ont_path, format='xml')

ont_query = [
    """
    [CUSTOM QUERY 1]
    """,
    """
    [CUSTOM QUERY 2]
    """,
]

validation_result = SchemaCertifier(
    data_graph=data_graph,
    shacl_graph=shacl_graph,
    ont_graph=ont_graph,
    ont_query=ont_query,
    inference_type="both"
).run()
```

**_Option 4_ - Use queries from the utilities**

```python
from rdflib import Graph

from dsi_schema_assurance import SchemaCertifier

from dsi_schema_assurance.utils import default_dtypes_query
from dsi_schema_assurance.utils import default_primitive_query

data_graph = Graph()
data_graph.parse(data_path, format='xml')

shacl_graph = Graph()
shacl_graph.parse(shacl_path, format='turtle')

ont_graph = Graph()
ont_graph.parse(ont_path, format='xml')

validation_result = SchemaCertifier(
    data_graph=data_graph,
    ont_graph=ont_graph,
    ont_query=default_dtypes_query,
    ont_primitive_query=default_primitive_query,
    inference_type="both"
).run()
```

If you're using the CIM ontology, you can use the following utilities to get the default queries:

```python
from dsi_schema_assurance.utils import get_cim_datatype_query
from dsi_schema_assurance.utils import get_cim_primitive_datatype_query
```

For further detail on these, you can check the [folder](./dsi_schema_assurance/utils/ddl/).


**_Notes_**

a. The list of queries will be executed sequentially - if there's a query that returns an error, the whole process will be aborted;

b. The queries **must always** retain two fields: `property` and `datatype` for it to be considered valid, otherwise the Schema Validation tool will raise multiple errors because its _modus operandi_ relies on that assumption.

_Example of a valid custom query:_

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cims: <http://iec.ch/TC57/1999/rdf-schema-extensions-19990926#>

SELECT DISTINCT ?property ?datatype ?stereotype
WHERE {
    ?property cims:dataType ?datatype .
    OPTIONAL {
        ?datatype cims:stereotype ?stereotype .
    }
}
```

_Example of an **invalid** custom query:_

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cims: <http://iec.ch/TC57/1999/rdf-schema-extensions-19990926#>

SELECT DISTINCT ?field ?dtype ?stereotype
WHERE {
    ?field cims:dataType ?dtype .
    OPTIONAL {
        ?dtype cims:stereotype ?stereotype .
    }
}
```

For more information - on how this validation can be used - you can check the [`demo`](./demo) folder. There you'll find a notebook that showcases the validation of CIM and other types of data that was used as a _proof of concept_.

**Note:** there's still some indefinition around how we're going to package all the modules together, which means that the way to use the Schema Validation might change in the future.

## **3. How it works under the hood**

<p align="center">
    <img src="./.docs/schema_certifier_mo.png" width="1200" height="250">
</p>

This solution divides itself into three main parts:

- The **_Datatypes Hunter_**: extracts the datatypes from ontologies or SHACLs.
- The **_Datatypes Injector_**: injects the datatypes into the RDF data instance.
- The **_Validator_**: validates the RDF data instance against the ontologies and SHACL files.

Let's dive into each one of them.

### **3.1. Datatypes Hunter**

As stated before, the datatypes hunter is the module that will be responsible for the following:
- extract the datatypes by parsing either an ontology or a SHACL file;
- the parsing is done via SPARQL queries;
- the queries naviagate through a nested hierarchy like the one in the image below:

<p align="center">
    <img src="./.docs/ontology_hierarchy.png" width="500" height="550">
</p>

Additionally, it's important to retain something about it's implementation. We have an hunter that is fully dedicated for the ontologies, and another one for the SHACL files.

This is because the ontologies and the SHACL files have different structures, and therefore, different strategies to extract the datatypes.

### **3.2. Datatypes Injector**

Single function that injects the datatypes, collected by the `DatatypeHunter`, to the RDF data instance.

### **3.3. Validator**

Last but not least, the validator script contains the SchemaCertifier class. This class is the one that will be responsible for the validation of the data.

Going back to module mentioned (Datatypes Hunter), this module will be responsible for concialiating the outcomes of the hunters (if the user provides both ontologies and SHACL files).

By default, the SHACLs are more assertive when it comes to datatypes definition, and therefore, the datatypes obtained from these will be the ones responsible for dictating the final datatypes.

This module leverages the pyshacl to perform the validation.

The user can choose the specs that will be leveraged on the validation process.

---

## **A1. Tests and Coverage**

To run the tests and coverage, use the following command:

```bash
❯ coverage run -m unittest discover tests/
```

the current coverage report is the following:

```bash
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
dsi_schema_assurance/detectors/ontology.py      38      0   100%
dsi_schema_assurance/detectors/shacl.py         12      0   100%
dsi_schema_assurance/injector.py                17      0   100%
dsi_schema_assurance/utils/ddl/cim.py            2      0   100%
dsi_schema_assurance/utils/ddl/default.py        3      0   100%
dsi_schema_assurance/utils/ddl/dl.py             1      0   100%
dsi_schema_assurance/utils/pandas.py            25      0   100%
dsi_schema_assurance/validator.py              148      1    99%
----------------------------------------------------------------
TOTAL                                          246      1    99%
```
