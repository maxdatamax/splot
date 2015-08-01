import pandas as pd
import numpy as np
from scipy import stats
from bokeh.plotting import figure


def generate_test_dataframe(n=1000):

    # base dataframe
    df = pd.DataFrame({'x1': np.random.randn(n),
                       'c1': pd.Categorical(np.random.choice(list('ABCDEFGH'), n), ordered=True),
                       'b1': np.random.choice(a=[np.nan, 1], size=n, replace=True, p=[0.1, .90])})

    # interactions. x2 depends on the levels of c1.
    df['x2'] = np.cos(df.c1.cat.codes)*.5 + df.x1

    # now make x3 the same as x2,  but with the random missing values (real world,  we have missing data)
    df['x3'] = df['x2'] * df['b1']

    return df


def get_summary_stats(x=None, group=None, data=None):

    # create a df of just the two variables and summarize it
    # TODO:  Consider if dropna() should be always applied?
    dt = data[[x, group]].dropna()

    # make a group by object to be used later.
    dtg = dt.groupby(group)[x]

    st = dtg.agg([('25%', lambda x: np.percentile(x, 25)),
                  ('50%', lambda x: np.percentile(x, 50)),
                  ('75%', lambda x: np.percentile(x, 75))])

    # compute the iqr and upper, lower whisker limits for each level of the group
    st['iqr'] = st['75%'] - st['25%']
    st['lwl'] = st['25%'] - 1.5 * st['iqr']
    st['uwl'] = st['75%'] + 1.5 * st['iqr']

    # join the uwl and lwl to the raw data, check if outlier and store boolean with data table
    dt = dt.join(st[['lwl', 'uwl']], on=group)
    dt['outlier'] = ~dt[x].between(dt['lwl'], dt['uwl'])

    # get the values of the upper and lower whiskers based on the min and max non-outliers (Tukey Boxplot)
    st = dt[dt.outlier].groupby(group)[x].agg([('lwp', np.min), ('uwp', np.max)]).join(st)

    # only return the bare minimum in the summary table and data table.
    return st.drop(['uwl', 'lwl'], axis=1),  dt[[x, group, 'outlier']]


def make_stripplot(x, g, dt, jw=.3, jitter_points=None):

    p = figure(x_range=list(dt[g].cat.categories),
               tools='', width=600, height=400)

    if not jitter_points:
        p.scatter(dt[g].cat.codes+1, dt[x])

    else:
        p.scatter(dt[g].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw, dt[x], alpha=.5)

    return p


def make_boxplot(x, g, st, dt, jw=.3, bw=.6, jitter_points=True, show_points=True, show_outliers=True):

    # create a figure
    p = figure(x_range=list(dt[g].cat.categories),
               tools='', width=600, height=400)

    # styling
    p.grid.grid_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.axis.major_tick_out = 4
    p.axis.major_tick_in = 0

    # *** Raw points ***

    # jitter categorical data
    if jitter_points:
        dt['xc'] = dt[g].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw

    else:
        dt['xc'] = dt[g].cat.codes+1

    # plot non-outliers
    if show_points:
        p.scatter(dt[~dt.outlier]['xc'], dt[~dt.outlier][x],
                  color='black', marker='o', size=4, alpha=0.5, line_color=None)

    # plot outliers
    if show_outliers:
        p.scatter(dt[dt.outlier]['xc'], dt[dt.outlier][x], color='red', marker='x', size=4, alpha=1)

    # *** Box and Whiskers ***
    # get centered locations of the boxes
    st['xc'] = st.index.codes+1

    # plot boxes (left, right, top, bottom)
    p.quad(st['xc']-bw/2,  st['xc']+bw/2, st['75%'], st['25%'], color='black', alpha=0.5, fill_color='grey')

    # plot median
    p.segment(st['xc']-bw/2, st['50%'], st['xc']+bw/2, st['50%'], color='black')

    # plot lower and upper whiskers (x0, y0, x1, y1)
    p.segment(st['xc'], st['25%'], st['xc'], st['lwp'], color='black')
    p.segment(st['xc'], st['75%'], st['xc'], st['uwp'], color='black')

    # plot lower and upper whisker terminations
    p.segment(st['xc']-bw/6, st['uwp'], st['xc']+bw/6, st['uwp'], color='black')
    p.segment(st['xc']-bw/6, st['lwp'], st['xc']+bw/6, st['lwp'], color='black')

    return p


def make_violinplot(x, g, st, dt, jw=.3, bw=.6, jitter_points=True, show_points=True, show_outliers=True):

    # create a figure
    p = figure(x_range=list(dt[g].cat.categories),
               tools='', width=600, height=400)

    # styling
    p.grid.grid_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.axis.major_tick_out = 4
    p.axis.major_tick_in = 0

    # get the centers for the violins
    st['xc'] = st.index.codes+1

    # jitter categorical data (TODO:  should only be done if showpoints is True)
    if jitter_points:
        dt['xc'] = dt[g].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw

    else:
        dt['xc'] = dt[g].cat.codes+1

    # plot non-outliers
    if show_points:
        p.scatter(dt[~dt.outlier]['xc'], dt[~dt.outlier][x],
                  color='black', marker='o', size=4, alpha=0.5, line_color=None)

    # plot outliers
    if show_outliers:
        p.scatter(dt[dt.outlier]['xc'], dt[dt.outlier][x], color='red', marker='x', size=4, alpha=1)

    # draw the violins
    ix = 1
    for cat in dt.c1.cat.categories:

        # subset values and get kde function.
        xd = dt[x][dt[g] == cat]
        kde = stats.gaussian_kde(xd,  bw_method='scott')

        # define the range over which to evaluate the kde
        xg = np.linspace(xd.min(), xd.max(), 50)

        # compute the coordinates of the patch and add it to the plot
        yv = np.append(xg, xg[::-1])
        xv = np.append(kde(xg), -kde(xg[::-1]))
        p.patch((xv+ix), yv, alpha=0.3, color='black')

        ix += 1

    # plot median
    p.scatter(st['xc'], st['50%'], marker='x', color='black')

    # plot lower and upper whiskers (x0, y0, x1, y1)
    p.segment(st['xc'], st['25%'], st['xc'], st['lwp'], color='black', line_width=1)
    p.segment(st['xc'], st['75%'], st['xc'], st['uwp'], color='black', line_width=1)

    # plot lower and upper whisker terminations
    p.segment(st['xc']-bw/6, st['uwp'], st['xc']+bw/6, st['uwp'], color='black')
    p.segment(st['xc']-bw/6, st['lwp'], st['xc']+bw/6, st['lwp'], color='black')

    # styling options
    p.grid.grid_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.axis.major_tick_out = 4
    p.axis.major_tick_in = 0

    return p
