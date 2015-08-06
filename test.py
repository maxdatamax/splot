from generate_df import *
from summarize_df import *
from bivar import *
from bokeh.plotting import output_file, show, gridplot
import seaborn as sns


# generate some test data
df = generate_test_dataframe(2000)

# set x and y variables
x, y = 'cv1', 'yv3'

df.dropna(inplace=True)

# output to static HTML file
output_file("test.html", title="Test Plots")

# make a few instances plots
p1 = make_stripplot(x=x, y=y, data=df, jitter_points=False, jw=0.3)
p2 = make_stripplot(x=x, y=y, data=df, jitter_points=True, jw=0.3)

p3 = make_boxplot(x, y, df, .3, .7, True, True, True)
p4 = make_boxplot(x, y, df, .3, .5, False, False, True)

p5 = make_violinplot(x=x, y=y, data=df, jw=.2, vw=.8, bw_method=.2, jitter_points=True, show_points=True,
                     show_outliers=True)

p6 = make_violinplot(x=x, y=y, data=df, jw=.2, vw=.7, jitter_points=False, show_points=False, show_outliers=True)

# get some seaborn data for comparison
tips = sns.load_dataset("tips")
x, y = 'day', 'total_bill'

st, dt = get_summary_stats('day', 'total_bill', tips)

p7 = make_boxplot(x=x, y=y, data=dt, jw=.15, bw=.7, jitter_points=True, show_points=True, show_outliers=True)

p8 = make_boxplot(x=x, y=y, data=dt, jw=.15, bw=.7, jitter_points=False, show_points=False, show_outliers=True)

p9 = make_violinplot(x=x, y=y, data=dt, jw=.2, vw=.8, jitter_points=False, show_points=True, show_outliers=True,
                     bw_method=.3)

p10 = make_violinplot(x=x, y=y, data=dt, jw=0, vw=.6, jitter_points=False, show_points=False, show_outliers=True)

# render the plots
p = gridplot([[p1, p2], [p3, p4], [p5, p6], [p7, p8], [p9, p10]])

show(p)
