from generate_df import *
from bivar import *
from bokeh.plotting import output_file, show, gridplot
import seaborn as sns


# generate some test data
df = generate_test_dataframe(1000)

# output to static HTML file
output_file("test.html", title="Test Plots")

# make a few instances plots
p1 = make_strip_plot(x='cv1', y='yv3', data=df)
p2 = make_strip_plot(x='cv1', y='yv3', data=df, jitter_points=True, jitter_width=.3)

p3 = make_box_plot(x='cv1', y='yv3', data=df)

p4 = make_box_plot(x='cv1', y='yv3', data=df, box_width=.8,
                   show_points=True, jitter_points=True, jitter_width=.4)

p5 = make_violin_plot(x='cv1', y='yv3', data=df)

p6 = make_violin_plot(x='cv1', y='yv3', data=df, violin_width=.7,
                      show_points=True, jitter_points=True, jitter_width=.3)

# get some seaborn data for comparison
tips = sns.load_dataset("tips")

p7 = make_box_plot(x='day', y='total_bill', data=tips)

p8 = make_box_plot(x='day', y='total_bill', data=tips, box_width=.7,
                   show_points=True, jitter_width=.2, jitter_points=True)

p9 = make_violin_plot(x='day', y='total_bill', data=tips)

p10 = make_violin_plot(x='day', y='total_bill', data=tips, violin_width=.9,
                       show_points=True, jitter_width=.05, jitter_points=True)

# render the plots
p = gridplot([[p1, p2], [p3, p4], [p5, p6], [p7, p8], [p9, p10]])

show(p)
