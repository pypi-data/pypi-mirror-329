# Functions that will be used to detect the data types from ontology files

import pandas as pd
from pandas import DataFrame

from typing import List
from typing import Union
from typing import Optional

from rdflib import Graph

from dsi_schema_assurance.utils.ddl.default import default_shacl_query


def shacl_datatypes_hunter(
    shacl_graph: Graph,
    shacl_query: Optional[Union[str, List[str]]] = default_shacl_query,
) -> DataFrame:
    """
    Query all the datatypes from the set of rules provided by the SHACL graph.

    There's two types of data type declarations that will be captured by the default query:
    1. rdf:datatype: default for rdf data
    2. stereotypes: when there's a specification of the types of the data

    On the second case, we want to filter out all the stereotypes that are not of the type Primitive.

    Args:
        shacl_graph (Graph): The shacl graph.
        shacl_query (Optional, Union[str, List[str]]): the SPARQL query or list of queries to be used
        for the validation

    Returns:
        DataFrame: A dataframe with the data types.
    """

    queries = [shacl_query] if isinstance(shacl_query, str) else shacl_query

    dfs_lst = [
        DataFrame(
            [
                {
                    "property": str(row.property).split("#")[-1],
                    "datatype": str(row.datatype).split("#")[-1].lower(),
                }
                for row in shacl_graph.query(query)
            ]
        )
        for query in queries
    ]

    df = pd.concat(dfs_lst, axis=0)

    return df
