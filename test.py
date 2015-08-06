from generate_df import *
from bivar import *
from bokeh.plotting import output_file, show, gridplot
import seaborn as sns


# generate some test data
df = generate_test_dataframe(500)

# output to static HTML file
output_file("test.html", title="Test Plots")

# make a few instances plots
p1 = make_strip_plot(x='cv1', y='yv3', data=df)
p2 = make_strip_plot(x='cv1', y='yv3', data=df, jitter_points=True, jw=0.3)

p3 = make_box_plot(x='cv1', y='yv3', data=df)

p4 = make_box_plot(x='cv1', y='yv3', data=df, jw=.2, bw=.5, jitter_points=True,
                   show_points=True, show_outliers=True)

p5 = make_violin_plot(x='cv1', y='yv3', data=df)

p6 = make_violin_plot(x='cv1', y='yv3', data=df, jw=.2, vw=.7, jitter_points=True,
                      show_points=True, show_outliers=True)

# get some seaborn data for comparison
tips = sns.load_dataset("tips")

p7 = make_box_plot(x='day', y='total_bill', data=tips)

p8 = make_box_plot(x='day', y='total_bill', data=tips, jw=.15, bw=.7, jitter_points=True,
                   show_points=True, show_outliers=True)

p9 = make_violin_plot(x='day', y='total_bill', data=tips)

p10 = make_violin_plot(x='day', y='total_bill', data=tips, jw=.15, vw=.6, jitter_points=True,
                       show_points=True, show_outliers=True)

# render the plots
p = gridplot([[p1, p2], [p3, p4], [p5, p6], [p7, p8], [p9, p10]])

show(p)
