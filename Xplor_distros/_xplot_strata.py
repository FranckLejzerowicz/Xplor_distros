# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import numpy as np
import pandas as pd


def get_possible_stratas(metadatas: dict, categorical: dict,
                         stratify: tuple, logs: list) -> dict:
    """
    Collect for each metadata table the metadata variables
    that amongst the variables passed to the "-p", "--p-stratify"
    option are categorical and occurring in the metadata tables.

    Parameters
    ----------
    metadatas : dict
        Key     = Metadata file path.
        Value   = Metadata table.
    categorical : dict
        Key     = Metadata file path.
        Value   = Metadata variables that are categorical.
    stratify : tuple
        Metadata variables on which to split the visualizations.
    logs : list
        List of lists: each nested list is:
            [variable, metadata file path, warning message, a number]

    Returns
    -------
    possible_stratas : dict
        Key     = Metadata file path.
        Value   = List of variables to possibly stratify on.
    """
    possible_stratas = {}
    for md_fp, categorical_variables in categorical.items():
        md = metadatas[md_fp]
        for strata in stratify:
            if strata in md.columns:
                if strata in categorical_variables:
                    possible_stratas.setdefault(md_fp, []).append(strata)
                else:
                    logs.append([strata, md_fp, 'not categorical', np.nan])
            else:
                logs.append([strata, md_fp, 'not in', np.nan])
    return possible_stratas


def make_merged_columns(md: pd.DataFrame, strata_: list) -> str:
    """
    Join variables contents for multiple,
    merged combination stratification.

    Parameters
    ----------
    md : pd.DataFrame
        Metadata table.
    strata_ : list
        Variables to stratify on.

    Returns
    -------
    new_column : str
        Name of the variable created from joined variables.
    """
    new_column = '__'.join(strata_)
    md[new_column] = md[strata_].fillna('nan').agg('__'.join, axis=1)
    return new_column


def get_stratas(metadatas: dict, possible_stratas: dict,
                max_strata: int, merge: bool, logs: list) -> dict:
    """
    For each metadata table, collect for each of its categorical
    metadata variables those that have a number of factors that
    is not too high, after merging or not.

    Parameters
    ----------
    metadatas : dict
        Key     = Metadata file path.
        Value   = Metadata table.
    possible_stratas : dict
        Key     = Metadata file path.
        Value   = List of variables to possibly stratify on.
    max_strata : int
        Maximum number of stratification to create.
    merge : bool
        Whether to merge multiple stratification variables or not.
    logs : list
        List of lists: each nested list is:
            [variable, metadata file path, warning message, a number]

    Returns
    -------
    stratas : dict
        Key     = Metadata file path.
        Value   = List of variables to stratify on.
    """
    stratas = {}
    for md_fp, strata_ in possible_stratas.items():
        md = metadatas[md_fp]
        if merge:
            new_column = make_merged_columns(md, strata_)
            strata = [new_column]
        else:
            strata = strata_

        for s in strata:
            n_factors = md[s].value_counts().size
            if n_factors > max_strata:
                logs.append([s, md_fp, 'too many factors', n_factors])
                continue
            stratas.setdefault(md_fp, []).append(s)
    return stratas


def get_dummy_stratas(metadatas: dict) -> dict:
    """
    Create a dummy, one-factor 'no_stratification' categorical
    metadata variables to stratify on for each metadata table.

    Parameters
    ----------
    metadatas : dict
        Key     = Metadata file path.
        Value   = Metadata table.

    Returns
    -------
    stratas : dict
        Key     = Metadata file path.
        Value   = List of one dummy 'no_stratification' variable to stratify on.
    """
    stratas = {}
    for md_fp, md in metadatas.items():
        md['no_stratification'] = 'no_stratification'
        stratas[md_fp] = ['no_stratification']
    return stratas


def get_stratification(metadatas: dict, categorical: dict,
                       stratify: tuple, max_strata: int,
                       merge: bool, logs: list) -> dict:
    """
    Collect the categorical metadata variables to
    stratify on for each metadata table.

    Parameters
    ----------
    metadatas : dict
        Key     = Metadata file path.
        Value   = Metadata table.
    categorical : dict
        Key     = Metadata file path.
        Value   = Metadata variables that are categorical.
    stratify : tuple
        Metadata variables on which to split the visualizations.
    max_strata : int
        Maximum number of stratification to create.
    merge : bool
        Whether to merge multiple stratification variables or not.
    logs : list
        List of lists: each nested list is:
            [variable, metadata file path, warning message, a number]

    Returns
    -------
    stratas : dict
        Key     = Metadata file path.
        Value   = List of variables to stratify on.
    """
    if stratify:
        possible_stratas = get_possible_stratas(metadatas, categorical, stratify, logs)
        stratas = get_stratas(metadatas, possible_stratas, max_strata, merge, logs)
    else:
        stratas = get_dummy_stratas(metadatas)
    return stratas
