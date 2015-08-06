import numpy as np


def get_summary_stats(x=None, y=None, data=None):

    # create a df of just the two variables and summarize it
    dt = data[[x, y]]

    # make a group by object to be used later.
    dtg = dt.groupby(x)[y]

    st = dtg.agg([('q1', lambda x: np.percentile(x, 25)),
                  ('med', lambda x: np.percentile(x, 50)),
                  ('q3', lambda x: np.percentile(x, 75))])

    st['iqr'] = st['q3'] - st['q1']
    st['lwl'] = st['q1'] - 1.5 * st['iqr']
    st['uwl'] = st['q3'] + 1.5 * st['iqr']

    # join the uwl and lwl to the raw data, check if outlier and store boolean with data table
    dt = dt.join(st[['lwl', 'uwl']], on=x)
    dt['outlier'] = ~dt[y].between(dt['lwl'], dt['uwl'])

    # get the values of the upper and lower whiskers based on the min and max non-outliers (Tukey Boxplot)
    st = dt[~dt.outlier].groupby(x)[y].agg([('lwp', np.min), ('uwp', np.max)]).join(st)

    # only return the bare minimum in the summary table and data table.
    return st.drop(['uwl', 'lwl'], axis=1),  dt[[x, y, 'outlier']]
