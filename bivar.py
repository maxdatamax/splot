import numpy as np
from scipy import stats
from bokeh.plotting import figure
from summarize_df import get_summary_stats


def make_base_plot(x=None, y=None, data=None, width=640, height=480, tools=''):

    # create a figure (allow setting)
    p = figure(x_range=list(data[x].cat.categories), tools=tools, width=width, height=height)

    # styling - outline of plot
    p.outline_line_color = 'grey'
    p.outline_line_width = 1

    # styling - title
    p.title = y + ' vs. ' + x
    p.title_text_font_size = "12pt"

    # styling - grid lines
    p.xgrid.grid_line_color = None

    # styling - axis labels
    p.xaxis.axis_label = x
    p.xaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label = y
    p.yaxis.axis_label_text_font_size = "12pt"

    # styling - axes lines
    p.xaxis.axis_line_color = None
    p.yaxis.axis_line_color = None

    # styling - axes ticks
    p.axis.major_tick_out = 4
    p.axis.major_tick_in = 0
    p.yaxis.minor_tick_line_color = None

    return p


def make_strip_plot(x=None, y=None, data=None, jitter_points=False, jw=0.3):

    # subset to the columns of interest and drop missing
    dt = data[[x, y]].dropna()

    # create a figure
    p = make_base_plot(x=x, y=y, data=dt)

    if jitter_points:
        p.scatter(dt[x].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw, dt[y],
                  color='black', marker='o', size=4, alpha=1, line_color=None)

    else:
        p.scatter(dt[x].cat.codes+1, dt[y], color='black', marker='o', size=4, alpha=1, line_color=None)

    return p


def make_box_plot(x=None, y=None, data=None, jw=.3, bw=.6, jitter_points=False, show_points=False, show_outliers=True,
                  box_fill_color='lightgrey', box_line_color='grey', box_line_width=1,
                  whisker_line_color='grey', whisker_line_width=1):

    # make a dataframe of just the variables needed,  drop missing values.
    dt = data[[x, y]].dropna()

    # summarize the data and mark the outliers
    st, dt = get_summary_stats(x, y, dt)

    # make the base plot
    p = make_base_plot(x=x, y=y, data=dt)

    # ************************
    # *** Box and Whiskers ***
    # ************************

    # get centered locations of the boxes
    st['xc'] = st.index.codes+1

    # plot boxes (left, right, top, bottom)
    p.quad(st['xc']-bw/2,  st['xc']+bw/2, st['q3'], st['q1'], fill_color=box_fill_color,
           line_color=box_line_color, line_width=box_line_width)

    # plot median
    p.segment(st['xc']-bw/2, st['med'], st['xc']+bw/2, st['med'],
              line_color=whisker_line_color, line_width=whisker_line_width)

    # plot lower and upper whiskers (x0, y0, x1, y1)
    p.segment(st['xc'], st['q1'], st['xc'], st['lwp'],
              line_color=whisker_line_color, line_width=whisker_line_width)
    p.segment(st['xc'], st['q3'], st['xc'], st['uwp'],
              line_color=whisker_line_color, line_width=whisker_line_width)

    # plot lower and upper whisker terminations
    p.segment(st['xc']-bw/6, st['uwp'], st['xc']+bw/6, st['uwp'],
              line_color=whisker_line_color, line_width=whisker_line_width)
    p.segment(st['xc']-bw/6, st['lwp'], st['xc']+bw/6, st['lwp'],
              line_color=whisker_line_color, line_width=whisker_line_width)

    # ******************
    # *** Raw Points ***
    # ******************

    # jitter categorical data
    if jitter_points:
        dt['xc'] = dt[x].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw

    else:
        dt['xc'] = dt[x].cat.codes+1

    # plot non-outliers
    if show_points:
        p.scatter(dt[~dt.outlier]['xc'], dt[~dt.outlier][y],
                  color='black', marker='o', size=4, alpha=1, line_color=None)

    # plot outliers
    if show_outliers:
        p.scatter(dt[dt.outlier]['xc'], dt[dt.outlier][y], color='red', marker='x', size=4, alpha=1)

    return p


def make_violin_plot(x=None, y=None, data=None, jw=.3, vw=.8, jitter_points=False, show_points=False,
                     show_outliers=True, bw_method='scott', violin_padding=.1, grid_points=50):

    # make a data frame of just the variables needed,  and drop missing values.
    dt = data[[x, y]].dropna()

    # summarize the data and mark the outliers
    st, dt = get_summary_stats(x, y, dt)

    # make the base plot
    p = make_base_plot(x=x, y=y, data=dt)

    # ***************
    # *** Violins ***
    # ***************

    ix = 1
    for category in dt[x].cat.categories:

        # subset values and get kde function.
        y_data = dt[dt[x] == category][y]

        # If kde can be calculated,  then compute pdf values and add to plot
        if len(y_data) > 1:

            # define the points within the range over which to compute the pdf.
            y_min, y_max = y_data.min(), y_data.max()
            y_padding = (y_max - y_min) * violin_padding
            y_grid = np.linspace(y_min - y_padding, y_max + y_padding, grid_points)

            # get the pdf function for the y_data, compute and normalize the pdf values to desired width
            pdf = stats.gaussian_kde(y_data, bw_method)
            x_pdf = pdf(y_grid)
            x_pdf = x_pdf/x_pdf.max()*vw/2

            # Build arrays that describe the patch points by appending reversed arrays (and negated for x)
            x_patch = np.append(x_pdf, -x_pdf[::-1])   # negated and reversed to get the left side of the violin
            y_patch = np.append(y_grid, y_grid[::-1])  # reversed to start left violin where right violin ended

            # add the patch to the plot
            p.patch((x_patch + ix), y_patch, alpha=1, color='lightgrey', line_color='grey', line_width=1)

        ix += 1

    # ******************
    # *** Raw Points ***
    # ******************

    # jitter categorical data (TODO:  should only be done if showpoints is True)
    if jitter_points:
        dt['xc'] = dt[x].cat.codes+1 + (np.random.random(len(dt))-0.5) * jw

    else:
        dt['xc'] = dt[x].cat.codes+1

    # plot non-outliers
    if show_points:
        p.scatter(dt[~dt.outlier]['xc'], dt[~dt.outlier][y],
                  color='black', marker='o', size=4, alpha=1, line_color=None)

    # plot outliers
    if show_outliers:
        p.scatter(dt[dt.outlier]['xc'], dt[dt.outlier][y], color='red', marker='x', size=4, alpha=1)

    # ************************
    # *** Box and Whiskers ***
    # ************************

    # get centered locations of the boxes
    st['xc'] = st.index.codes+1

    # plot median
    p.scatter(st['xc'], st['med'], marker='o', color='black')

    # plot lower and upper whiskers (x0, y0, x1, y1)
    p.segment(st['xc'], st['q1'], st['xc'], st['lwp'], color='black', line_width=1)
    p.segment(st['xc'], st['q3'], st['xc'], st['uwp'], color='black', line_width=1)

    # plot lower and upper whisker terminations
    p.segment(st['xc']-jw/6, st['uwp'], st['xc']+jw/6, st['uwp'], color='black')
    p.segment(st['xc']-jw/6, st['lwp'], st['xc']+jw/6, st['lwp'], color='black')

    return p
