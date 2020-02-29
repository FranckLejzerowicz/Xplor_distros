# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import click

from Xports import __version__
from Xplor_distros._xplor_distros import xplor_distros


@click.command()
@click.option(
    "-m", "--m-metadata-file", required=True, multiple=True,
    help="Metadata file(s) containing numeric valriables (to plot) "
         "and categorical variables (to stratify)."
)
@click.option(
    "-p", "--p-stratify", required=False, multiple=True, default=None,
    show_default=True, help="Categorical variables to use for stratification."
)
@click.option(
    "-s", "--p-max-strata", required=False, default=20, type=int,
    show_default=True, help="Maximum number of stratification to create "
                            "(Some categorical variables may contain a "
                            "high number of categories and you may not "
                            "want hundreds of panels per variable, and "
                            "for each metadata file...)."
)
@click.option(
    "-n", "--p-number-of-samples", required=False, default=100, type=int,
    show_default=True, help="Number of samples to randomly select to "
                            "compute the distributions."
)
@click.option(
    "-o", "--o-distributions", required=True, help="Output visualization file."
)
@click.option(
    "--merge/--no-merge", default=False, show_default=True,
    help="Merge multiple stratification variables. For example, "
         "if 'sex' and 'wine_consumed' are passed: use their "
         "combined factors: 'Male__Yes', 'Female__Yes', "
         "'Male_No', 'Female__No'."
)
@click.version_option(__version__, prog_name="Xplor_distros")


def standalone_xplor(
        m_metadata_file,
        p_stratify,
        p_number_of_samples,
        o_distributions,
        p_max_strata,
        merge
):

    xplor_distros(
        m_metadata_file,
        p_stratify,
        p_number_of_samples,
        o_distributions,
        p_max_strata,
        merge
    )


if __name__ == "__main__":
    standalone_xplor()
