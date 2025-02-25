# Utilities around pandas operations

import pandas as pd
from pandas import DataFrame

from typing import Dict
from typing import Union


def convert_df_to_dict(df: DataFrame, key_col: str, value_col: str) -> Dict[str, str]:
    """
    Convert a pandas dataframe to a key-value dictionary.

    From a string value indicated which dataframe columns should be kept as keys and another
    indicating which column should be kept as values, this function will return a dictionary
    with the key-value pairs.

    _Example_:
    >>> data = {'key': ['a', 'b', 'c'], 'value': [1, 2, 3], 'another_col': [4, 5, 6]}
    >>> df = pd.DataFrame(data)
    >>> convert_df_to_dict(df, 'key', 'value')
    {'a': 1, 'b': 2, 'c': 3}

    Args:
        df (DataFrame): The pandas dataframe.
        key_col (str): The column to be used as key.
        value_col (str): The column to be used as value.

    Returns:
        Dict[str, str]: The dictionary.
    """

    return {row[key_col]: row[value_col] for row in df.to_dict(orient="records")}


def dfs_conciliator(
    df_1: DataFrame, df_2: DataFrame, target_col: str, values_col: str
) -> DataFrame:
    """
    Handles the differences between two pandas dataframes.

    This function can be used on two different use cases:
    1. Whenever there's missing records in one of the dataframes - when that happens, the missing
    records will be pulled from the second dataframe into the first one;
    2. Whenever there's values that are different between the two dataframes - when that happens,
    the values from the first dataframe will be replaced by the values from the second one.

    _Example1_:
    >>> df_1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'value': [1, 2, 3]})
    >>> df_2 = pd.DataFrame({'key': ['b', 'c', 'd'], 'value': [2, 3, 4]})
    >>> dfs_conciliator(df_1, df_2)
    {'key': ['a', 'b', 'c', 'd'], 'value': [1, 2, 3, 4]}


    _Example2_:
    >>> df_1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'value': [1, 1, 1]})
    >>> df_2 = pd.DataFrame({'key': ['b', 'c', 'd'], 'value': [2, 3, 4]})
    >>> dfs_conciliator(df_1, df_2)
    {'key': ['a', 'b', 'c'], 'value': [1, 2, 3]}

    Args:
        df_1 (DataFrame): The first dataframe.
        df_2 (DataFrame): The second dataframe.
        target_col (str): The column to be used as target.
        values_col (str): The column that contains the values.

    Returns:
        DataFrame: The cleaned dataframe.
    """

    def _merge_dfs(df_1: DataFrame, df_2: DataFrame, target_col: str) -> DataFrame:
        """
        This subfunction will handle the first case of the dfs_conciliator function.
        """

        # Identify records in df2 that are not in df1
        df2_unique = df_2[~df_2[target_col].isin(df_1[target_col])]

        # Concatenate df1 with the unique records from df2
        merged_df = pd.concat([df_1, df2_unique], ignore_index=True)

        return merged_df

    def _replace_values(
        df_1: DataFrame, df_2: DataFrame, target_col: str, values_col: str
    ) -> DataFrame:
        """
        This subfunction will handle the second case of the dfs_conciliator function.
        """

        # Merge the two dataframes on target_col to compare values
        merged_df = pd.merge(
            df_1, df_2, on=target_col, how="left", suffixes=("_1", "_2")
        )

        # Replace values in values_col column from df_1 with those from df_2 where they differ
        merged_df[values_col] = merged_df[values_col + "_2"].where(
            merged_df[values_col + "_1"] != merged_df[values_col + "_2"],
            merged_df[values_col + "_2"],
        )

        # Select only the relevant columns
        cleaned_df = merged_df[[target_col, values_col]]

        return cleaned_df

    df = _replace_values(df_1, df_2, target_col, values_col)
    df = _merge_dfs(df, df_2, target_col)

    return df


def df_diff_reporter(
    df_1: DataFrame,
    df_2: DataFrame,
    merging_col: str = "property",
    target_col: str = "datatype",
) -> Union[int, int]:
    """
    Reports the differences between two dataframes.

    The differences covered by this method can be of two kinds:
    1. there's missing records on the first dataframe, when compared to the second one;
    2. there's different values for the same property in the two dataframes.

    Args:
        df_1 (DataFrame): The first dataframe.
        df_2 (DataFrame): The second dataframe.
        merging_col (str): The column to be used for merging the two dataframes.

    Returns:
        int, int: the number of missing records and the number of different values.
    """

    merged_df = pd.merge(
        df_1, df_2, on=merging_col, how="outer", suffixes=("_df1", "_df2")
    )
    diff_datatypes = merged_df[
        merged_df[f"{target_col}_df1"] != merged_df[f"{target_col}_df2"]
    ]

    missing_records = (
        merged_df[[f"{target_col}_df1", f"{target_col}_df2"]].isna().sum().sum()
    )
    diff_records = diff_datatypes.shape[0] - missing_records

    return missing_records, diff_records
