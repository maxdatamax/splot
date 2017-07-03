import numpy as np
from scipy import stats
from bokeh.plotting import figure
from bokeh.models import Title
from summarize_df import get_summary_stats


def make_base_plot(x=None, y=None, data=None, width=640, height=480, tools='', plot=None):

    # create a plot figure is one is not passed
    if plot is None:
        plot = figure(x_range=list(data[x].cat.categories), tools=tools, width=width, height=height)

    # styling - outline of plot
    plot.outline_line_color = 'grey'
    plot.outline_line_width = 1

    # styling - title
    plot.title = Title(text=y + ' vs. ' + x, align="center")
    #plot.title_text_font_size = "12pt"

    # styling - grid lines
    plot.xgrid.grid_line_color = None

    # styling - axis labels
    plot.xaxis.axis_label = x
    plot.xaxis.axis_label_text_font_size = "12pt"
    plot.yaxis.axis_label = y
    plot.yaxis.axis_label_text_font_size = "12pt"

    # styling - axes lines
    plot.xaxis.axis_line_color = None
    plot.yaxis.axis_line_color = None

    # styling - axes ticks
    plot.axis.major_tick_out = 4
    plot.axis.major_tick_in = 0
    plot.yaxis.minor_tick_line_color = None

    return plot


def make_strip_plot(x=None, y=None, data=None,
                    point_color='black', point_marker='o', point_alpha=1, point_size=3,
                    jitter_points=False, jitter_width=0.3, plot=None):

    # subset to the columns of interest and drop missing
    dt = data[[x, y]].dropna()

    # create a figure if one does not already exist
    if plot is None:
        plot = make_base_plot(x=x, y=y, data=data)

    # add the points to the plot
    if jitter_points:
        x_points = dt[x].cat.codes+1 + (np.random.random(len(dt))-0.5) * jitter_width
    else:
        x_points = dt[x].cat.codes+1

    plot.scatter(x_points, dt[y], color=point_color, marker=point_marker, size=point_size, alpha=point_alpha)

    return plot


def make_box_plot(x=None, y=None, data=None, st=None, box_width=.6, show_points=False, show_outliers=True,
                  box_fill_color='lightgrey', box_line_color='grey', box_line_width=1,
                  whisker_line_color='grey', whisker_line_width=1, plot=None, **kwargs):

    # if no summary table (st) is passed, then we need to create one and mark the outliers in the data
    if st is None and 'outliers' not in data.columns:
        st, dt = get_summary_stats(x, y, data[[x, y]].dropna())
    else:
        dt = data

    # create a figure if one does not already exist
    if plot is None:
        plot = make_base_plot(x=x, y=y, data=dt)

    # ************************
    # *** Box and Whiskers ***
    # ************************

    # get centered locations of the boxes
    st['xc'] = st.index.codes + 1

    # plot boxes (left, right, top, bottom)
    plot.quad(st['xc'] - box_width / 2,  st['xc'] + box_width / 2, st['q3'], st['q1'], fill_color=box_fill_color,
              line_color=box_line_color, line_width=box_line_width)

    # plot median
    plot.segment(st['xc'] - box_width / 2, st['med'], st['xc'] + box_width / 2, st['med'],
                 line_color=whisker_line_color, line_width=whisker_line_width)

    # plot lower and upper whiskers (x0, y0, x1, y1)
    plot.segment(st['xc'], st['q1'], st['xc'], st['lwp'],
                 line_color=whisker_line_color, line_width=whisker_line_width)
    plot.segment(st['xc'], st['q3'], st['xc'], st['uwp'],
                 line_color=whisker_line_color, line_width=whisker_line_width)

    # plot lower and upper whisker terminations
    plot.segment(st['xc'] - box_width / 6, st['uwp'], st['xc']+box_width / 6, st['uwp'],
                 line_color=whisker_line_color, line_width=whisker_line_width)
    plot.segment(st['xc'] - box_width / 6, st['lwp'], st['xc']+box_width / 6, st['lwp'],
                 line_color=whisker_line_color, line_width=whisker_line_width)

    # **********************
    # *** Add Raw Points ***
    # **********************

    # plot outliers (always?)
    if show_outliers:
        plot = make_strip_plot(x, y, dt[dt.outlier],
                               point_color='red', point_marker='x', plot=plot, point_size=5, **kwargs)

    if show_points:
        plot = make_strip_plot(x, y, dt[~dt.outlier],
                               point_color='black', point_marker='o', plot=plot, **kwargs)

    return plot


def make_violin_plot(x=None, y=None, data=None,
                     bw_method='scott', violin_padding=.1, grid_points=50, violin_width=.8,
                     show_points=False, show_outliers=True, show_boxes=True, plot=None, **kwargs):

    # make a data frame of just the variables needed,  and drop missing values.
    dt = data[[x, y]].dropna()

    # create a figure if one does not already exist
    if plot is None:
        plot = make_base_plot(x=x, y=y, data=dt)

    # *******************
    # *** Add Violins ***
    # *******************

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
            x_pdf = x_pdf / x_pdf.max() * violin_width / 2

            # Build arrays that describe the patch points by appending reversed arrays (and negated for x)
            x_patch = np.append(x_pdf, -x_pdf[::-1])   # negated and reversed to get the left side of the violin
            y_patch = np.append(y_grid, y_grid[::-1])  # reversed to start left violin where right violin ended

            # add the patch to the plot
            plot.patch((x_patch + ix), y_patch, alpha=1, color='lightgrey', line_color='grey', line_width=1)

        ix += 1

    # ********************************
    # *** Add boxes and raw points ***
    # ********************************

    # summarize the data and mark the outliers in the data table
    st, dt = get_summary_stats(x, y, dt)

    if show_boxes:
        plot = make_box_plot(x=x, y=y, data=dt, st=st,
                             box_width=violin_width/4, plot=plot, show_outliers=False, show_points=False, **kwargs)

    # plot outliers
    if show_outliers:
        plot = make_strip_plot(x, y, dt[dt.outlier], point_color='red', point_marker='x', plot=plot, point_size=5, **kwargs)

    # plot non outliers
    if show_points:
        plot = make_strip_plot(x, y, dt[~dt.outlier], point_color='black', point_marker='o', plot=plot, **kwargs)

    return plot
