# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd


def show_log(logs: list, max_strata: int) -> None:
    """
    Show logs on a per type-of-issue basis.

    Parameters
    ----------
    logs : list
        List of lists: each nested list is:
            [variable, metadata file path, warning message, a number]
    max_strata : int
        Maximum number of stratification to create.
    """
    print()
    logs_pd = pd.DataFrame(logs, columns = ['variable', 'path', 'warning', 'number'])
    for warning, warning_pd in logs_pd.groupby('warning'):
        print('[%s]' % warning)

        for md_fp, md_pd in warning_pd.groupby('path'):
            print(md_fp)
            if warning == 'too many factors':
                for var, num in md_pd[['variable', 'number']].values:
                    print(' - variable %s has %s factor'
                          '(max %s [options "-s"])' % (var, num, max_strata))

            elif warning == 'not categorical':
                for var in md_pd.variable.unique():
                    print(' -', var)

            elif warning == 'not in':
                for var in md_pd.variable.unique():
                    print(' -', var)

            elif warning == 'not enough samples':
                for var, num in md_pd[['variable', 'number']].values:
                    print(' - %s samples for factor %s' % (var, num))
