# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd


def read_meta_pd(meta: str) -> pd.DataFrame:
    """
    Read metadata with first column as index.

    Parameters
    ----------
    meta : str
        Metadata file path.

    Returns
    -------
    meta_pd : pd.DataFrame
        Metadata table.
    """
    with open(meta) as f:
        for line in f:
            first_col = line.split()[0]
            break
    meta_pd = pd.read_csv(meta, header=0, sep='\t', dtype={first_col: str}, low_memory=False)
    meta_pd.rename(columns={first_col: 'sample_name'}, inplace=True)
    meta_pd.set_index('sample_name', inplace=True)

    # remove NaN only columns
    meta_pd = meta_pd.loc[:,~meta_pd.isna().all()]

    return meta_pd


def get_metadata_files(metadata_files: tuple) -> dict:
    """
    Collect the metadata tables as pandas DataFrame.

    Parameters
    ----------
    metadata_files : tuple
        Paths to the metadata file for which to make visualizations.

    Returns
    -------
    metadatas : dict
        Key     = File path to a metadata file.
        Value   = Metadata table.
    """
    metadatas = {}
    for meta in metadata_files:
        meta_pd = read_meta_pd(meta)
        metadatas[meta] = meta_pd

    return metadatas
