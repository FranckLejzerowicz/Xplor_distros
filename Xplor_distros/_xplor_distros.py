# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from Xplor_distros._xplor_md import get_metadata_files
from Xplor_distros._xplor_dtypes import get_dtypes, split_variables_types
from Xplor_distros._xplot_strata import get_stratification
from Xplor_distros._xplor_plot import make_plots
from Xplor_distros._xplor_logs import show_log


def xplor_distros(
        metadata_files: tuple,
        stratify: tuple,
        number_of_samples: int,
        distributions: str,
        max_strata: int,
        merge: bool) -> None:
    """
    Main script preparing the distributions visualizations
    for the numeric variables in a metadata file.

    Parameters
    ----------
    metadata_files : tuple
        Paths to the metadata file for which to make visualizations.
    stratify : tuple
        Metadata variables on which to split the visualizations.
    number_of_samples : int
        Number of samples to randomly select to compute the distributions.
    distributions : str
        Output visualization file path.
    max_strata : int
        Maximum number of stratification to create.
    merge : bool
        Whether to merge multiple stratification variables or not.
    """

    logs = []
    # Collect the metadata tables as pandas DataFrame
    metadatas = get_metadata_files(metadata_files)
    # Get the dtypes of each column for each metadata table
    dtypes = get_dtypes(metadatas)
    numerical, categorical = split_variables_types(dtypes)
    # Get categorical metadata variables to stratify on
    stratas = get_stratification(metadatas, categorical, stratify,
                                 max_strata, merge, logs)
    make_plots(metadatas, stratas, numerical, distributions, number_of_samples, logs)

    if logs:
        show_log(logs, max_strata)
