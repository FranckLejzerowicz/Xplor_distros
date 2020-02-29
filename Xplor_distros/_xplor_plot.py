# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import random
import pandas as pd
import numpy as np
from scipy.stats import skew
from os.path import isdir, dirname

from matplotlib.colors import rgb2hex
from matplotlib.pyplot import cm

import altair
altair.data_transformers.disable_max_rows()


def get_colors(feats: list) -> list:
    """
    Get the color map / palette for the number
    of numeric variables in the metadata.

    Parameters
    ----------
    feats : list
        Features in the metadata strata

    Returns
    -------
    colors : list
        One color per feature
    """
    colors = list(set([rgb2hex(x) for x in cm.rainbow(np.linspace(0, 1, len(feats)))]))
    return colors


def get_unstacked_md(numerical_factor_md: pd.DataFrame) -> pd.DataFrame:
    """
    Subset the metadata table to its numeric columns.

    Parameters
    ----------
    numerical_factor_md : pd.DataFrame
        Metadata table subset to the current stratification factors.

    Returns
    -------
    unstacked_md : pd.DataFrame
        Merge of the current factors' numerical dataframe
        with the median and skewness computed for these variable.
    """
    variables = list(numerical_factor_md.columns.tolist())
    medians = list(np.nanmedian(numerical_factor_md, axis=0))
    skewness = list(skew(numerical_factor_md.values, axis=0, nan_policy='omit'))
    to_merge = pd.DataFrame({'variable': variables,
                             'median': medians,
                             'skewness': skewness})

    unstacked_md = numerical_factor_md.unstack().reset_index().rename(
        columns={'level_0': 'variable', 0: 'value'}).copy()

    unstacked_md = unstacked_md.merge(to_merge, on='variable', how='left')
    return unstacked_md


def make_plots(metadatas: dict, stratas: dict, numerical: dict,
               distributions: str, number_of_samples: int, logs: list) -> None:
    """
    Make the rows of interactive figures (three panels)
    for each metadata table and for each stratification.
    Write the output as interactive html file.

    Parameters
    ----------
    metadatas : dict
        Key     = File path to a metadata file.
        Value   = Metadata table.
    stratas : dict
        Key     = Metadata file path.
        Value   = List of variables to stratify on.
    numerical : dict
        Key     = Metadata file path.
        Value   = Metadata variables that are numeric.
    distributions : str
        Output visualization file path.
    number_of_samples : int
        Number of samples to randomly select to compute the distributions.
    logs : list
        List of lists: each nested list is:
            [variable, metadata file path, warning message, a number]
    """

    if stratas:
        chart = None
        first_chart = True
        for md_fp, md in metadatas.items():
            for strata in stratas[md_fp]:
                for factor, factor_md in md.groupby(strata):

                    numerical_md = factor_md[numerical[md_fp]].copy()
                    unstacked_md = get_unstacked_md(numerical_md)

                    title = '\n'.join([md_fp, strata, factor])
                    figure_tab = subset_samples(md_fp, factor, unstacked_md,
                                                number_of_samples, logs)

                    strati_chart = plot_altair(title, figure_tab)
                    if first_chart:
                        chart = strati_chart
                        first_chart = False
                    else:
                        chart = (chart & strati_chart)

        # write plot output
        out_dir = dirname(distributions)
        if not isdir(out_dir):
            os.makedirs(out_dir)
        if not distributions.endswith('.html'):
            distributions = '%s.html' % distributions
        chart.save(distributions)


def subset_samples(md_fp: str, factor: str, unstacked_md: pd.DataFrame,
                   number_of_samples: int, logs:list) -> pd.DataFrame:
    """
    Subset the metadata to a maximum set of 100 samples.
    ! ATTENTION ! In case there are many columns with np.nan,
                  these should be selected to select samples
                  that do have actual numerical values...

    Parameters
    ----------
    md_fp : str
        Metadata file path.
    factor : str
        Stratification factor.
    unstacked_md : pd.DataFrame
        Metadata table subset for the current
        stratification and numerical variables.
    number_of_samples : int
        Number of samples to randomly select to
        compute the distributions.
    logs : list
        List of lists: each nested list is:
            [variable, metadata file path, warning message, a number]

    Returns
    -------
    figure_tab : pd.DataFrame
        re-stacked metadata table
    """
    # get the unique samples names
    samples = set(list(unstacked_md.sample_name.tolist()))
    # take either 100 or if less, all the samples as data for the figure
    if len(samples) < number_of_samples:
        logs.append([factor, md_fp, 'not enough samples', len(samples)])
        figure_tab = unstacked_md.copy()
    else:
        random_samples = random.sample(samples, number_of_samples)
        figure_tab = unstacked_md.loc[unstacked_md.sample_name.isin(random_samples),:].copy()
    return figure_tab


def plot_altair(title: str, figure_tab: pd.DataFrame):
    """
    Make the Altair interactive figure: one row of
    interactive figures (three panels) for the
    current metadata table and stratification.

    Parameters
    ----------
    title : str
        Title for the row plots.
    figure_tab : pd.DataFrame
        Metadata table ready for plotting.

    Returns
    -------
    chart : altair.vegalite.v3.api.VConcatChart
        Group of three panels figure for the current
        metadata table and stratification.
    """
    figure_tab['median_log10'] = [np.log10(x) if x> 0 else x for x in figure_tab['median']]

    variables = figure_tab.variable.tolist()
    colors_scale = get_colors(variables)
    color_scale = altair.Scale(domain=sorted(set(variables)), range=colors_scale)

    # Main plot dataset
    brush = altair.selection(type='interval')
    base = altair.Chart(figure_tab, title=title).properties(
        width=1100,
        height=400
    ).add_selection(
        brush
    )

    # First panel
    points1 = base.mark_point(filled=True, size=100).encode(
        x=altair.X('median:Q',
                   scale=altair.Scale(domain=[
                       min(figure_tab['median']),
                       max(figure_tab['median'])
                   ])),
        y=altair.Y('skewness:Q',
                   scale=altair.Scale(domain=[
                       min(figure_tab['skewness']),
                       max(figure_tab['skewness'])]
                   )),
        color=altair.condition(brush, 'variable:N',
                               altair.value('lightgray'),
                               scale=color_scale,
                               legend=None),
        tooltip = ['variable:N']
    ).properties(width=400, height=400)

    # Second panel
    points2 = base.mark_point(filled=True, size=100).encode(
        x=altair.X('median_log10:Q',
                scale=altair.Scale(domain=[
                    min(figure_tab['median_log10']),
                    max(figure_tab['median_log10'])
                ])),
        y=altair.Y('skewness:Q',
                   scale=altair.Scale(domain=[
                       min(figure_tab['skewness']),
                       max(figure_tab['skewness'])
                   ])),
        color=altair.condition(brush, 'variable:N',
                            altair.value('lightgray'),
                            scale=color_scale,
                            legend=None),
        tooltip=['variable:N']
    ).properties(width=400, height=400)

    # Third panel
    hists = base.mark_bar(opacity=0.7, thickness=100).encode(
        x=altair.X('value',
                bin=altair.Bin(maxbins=50)),
        y=altair.Y('count()', stack=None),
        color=altair.Color('variable:N',
                        scale=color_scale,
                        legend=None)
    ).transform_filter(brush).properties(width=700, height=400)

    chart = (points1 | points2 | hists)
    return chart


