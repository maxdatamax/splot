import numpy as np


def get_summary_stats(x=None, y=None, data=None):

    # create a df of just the two variables and summarize it
    # TODO:  Change this to only return the summary table.
    dt = data[[x, y]]

    # make a group by object to be used later.
    dtg = dt.groupby(x)[y]

    st = dtg.agg([('25%', lambda x: np.nanpercentile(x, 25)),
                  ('50%', lambda x: np.nanpercentile(x, 50)),
                  ('75%', lambda x: np.nanpercentile(x, 75))])

    # compute the iqr and upper, lower whisker limits for each level of the group
    st['iqr'] = st['75%'] - st['25%']
    st['lwl'] = st['25%'] - 1.5 * st['iqr']
    st['uwl'] = st['75%'] + 1.5 * st['iqr']

    # TODO:  Make separate function to compute and flag outliers.
    # join the uwl and lwl to the raw data, check if outlier and store boolean with data table
    dt = dt.join(st[['lwl', 'uwl']], on=x)
    dt['outlier'] = ~dt[y].between(dt['lwl'], dt['uwl'])

    # get the values of the upper and lower whiskers based on the min and max non-outliers (Tukey Boxplot)
    st = dt[~dt.outlier].groupby(x)[y].agg([('lwp', np.min), ('uwp', np.max)]).join(st)

    # only return the bare minimum in the summary table and data table.
    return st.drop(['uwl', 'lwl'], axis=1),  dt[[x, y, 'outlier']]