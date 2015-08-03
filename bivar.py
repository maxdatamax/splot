import numpy as np
from scipy import stats
from bokeh.plotting import figure


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


def make_stripplot(x=None, y=None, dt=None, jw=.3, jitter_points=None):

    p = figure(x_range=list(dt[x].cat.categories),
               tools='', width=600, height=400)

    if not jitter_points:
        p.scatter(dt[x].cat.codes+1, dt[y])

    else:
        p.scatter(dt[x].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw, dt[y])

    return p


def make_boxplot(x=None, y=None, st=None, dt=None, jw=.3, bw=.6,
                 jitter_points=True, show_points=True, show_outliers=True):

    # create a figure
    p = figure(x_range=list(dt[x].cat.categories),
               tools='', width=600, height=400)

    # styling
    p.grid.grid_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.axis.major_tick_out = 4
    p.axis.major_tick_in = 0

    # *** Raw points ***

    # jitter categorical data
    if jitter_points:
        dt['xc'] = dt[x].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw

    else:
        dt['xc'] = dt[x].cat.codes+1

    # plot non-outliers
    if show_points:
        p.scatter(dt[~dt.outlier]['xc'], dt[~dt.outlier][y],
                  color='black', marker='o', size=4, alpha=0.5, line_color=None)

    # plot outliers
    if show_outliers:
        p.scatter(dt[dt.outlier]['xc'], dt[dt.outlier][y], color='red', marker='x', size=4, alpha=1)

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


def make_violinplot(x=None, y=None, st=None, dt=None, jw=.3, vw=.8,
                    jitter_points=True, show_points=True, show_outliers=True):

    # create a figure
    p = figure(x_range=list(dt[x].cat.categories),
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
        dt['xc'] = dt[x].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw

    else:
        dt['xc'] = dt[x].cat.codes+1

    # plot non-outliers
    if show_points:
        p.scatter(dt[~dt.outlier]['xc'], dt[~dt.outlier][y],
                  color='black', marker='o', size=4, alpha=0.5, line_color=None)

    # plot outliers
    if show_outliers:
        p.scatter(dt[dt.outlier]['xc'], dt[dt.outlier][y], color='red', marker='x', size=4, alpha=1)

    # draw the violins
    ix = 1
    for cat in dt[x].cat.categories:

        # subset values and get kde function.
        yd = dt[dt[x] == cat][y]

        # get the kde function fot hsi data
        pdf = stats.gaussian_kde(yd)

        # define the point within the range over which to compute the pdf.
        # using the same rule as matlab (but generalizing it)
        ymin, ymax = yd.min(), yd.max()
        yrange = ymax-ymin
        padding = yrange * 0.2
        yp = np.linspace(ymin-padding, ymax+padding, 50)

        # compute x and y values of the patch and add it to the plot
        yv = np.append(yp, yp[::-1])

        # compute the pdf (x values) and normalize the max pdf value
        xp = pdf(yp)
        xp = xp/xp.max()*vw/2
        xv = np.append(xp, -xp[::-1])

        p.patch((xv+ix), yv, alpha=0.3, color='black')

        ix += 1

    # plot median
    p.scatter(st['xc'], st['50%'], marker='x', color='black')

    # plot lower and upper whiskers (x0, y0, x1, y1)
    p.segment(st['xc'], st['25%'], st['xc'], st['lwp'], color='black', line_width=1)
    p.segment(st['xc'], st['75%'], st['xc'], st['uwp'], color='black', line_width=1)

    # plot lower and upper whisker terminations
    p.segment(st['xc']-jw/6, st['uwp'], st['xc']+jw/6, st['uwp'], color='black')
    p.segment(st['xc']-jw/6, st['lwp'], st['xc']+jw/6, st['lwp'], color='black')

    # styling options
    p.grid.grid_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.axis.major_tick_out = 4
    p.axis.major_tick_in = 0

    return p
