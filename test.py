from bivar import *
from df_generator import *
from bokeh.plotting import output_file, show, gridplot
import seaborn as sns


# generate some test data
df = generate_test_dataframe(1000)

# set x and y variables
x, y = 'cv1', 'yv3'

# make the boxplot
st, dt = get_summary_stats(x, y, df)

dt.dropna(inplace=True)

# output to static HTML file
output_file("test.html", title="Test Plots")

# make a few versions of the plot
p1 = make_stripplot(x, y, dt, .3, False)
p2 = make_stripplot(x, y, dt, .3, True)

p3 = make_boxplot(x, y, st, dt, .3, .7, True, True, True)
p4 = make_boxplot(x, y, st, dt, .3, .5, False, False, True)

p5 = make_violinplot(x=x, y=y, st=st, dt=dt, jw=.1, vw=.8,
                     jitter_points=True, show_points=True, show_outliers=True)

p6 = make_violinplot(x=x, y=y, st=st, dt=dt, jw=.1, vw=.7,
                     jitter_points=False, show_points=False, show_outliers=True)

# get some seaborn data for comparison
tips = sns.load_dataset("tips")
x, y = 'day', 'total_bill'

st, dt = get_summary_stats('day', 'total_bill', tips)

p7 = make_boxplot(x=x, y=y, st=st, dt=dt, jw=.3, bw=.7,
                  jitter_points=True, show_points=True, show_outliers=True)

p8 = make_boxplot(x=x, y=y, st=st, dt=dt, jw=.3, bw=.7,
                  jitter_points=False, show_points=False, show_outliers=True)

p9 = make_violinplot(x=x, y=y, st=st, dt=dt, jw=.2, vw=.8,
                     jitter_points=True, show_points=True, show_outliers=True)

p10 = make_violinplot(x=x, y=y, st=st, dt=dt, jw=0, vw=.6,
                      jitter_points=False, show_points=False, show_outliers=True)

# render the plots
p = gridplot([[p1, p2], [p3, p4], [p5, p6], [p7, p8], [p9, p10]])

show(p)
