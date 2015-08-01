from bivar import *
from bokeh.plotting import output_file, show, gridplot
from bokeh.charts import BoxPlot
from bokeh import mpl
import seaborn as sns

# generate some test data
df = generate_test_dataframe(1000)
x, g = 'x3', 'c1'

# make the boxplot
st, dt = get_summary_stats(x, g, df)

# output to static HTML file
output_file("test.html", title="Test Plots")

# make a few versions of the plot
p1 = make_stripplot(x, g, dt, .3, False)
p2 = make_stripplot(x, g, dt, .3, True)

p3 = make_boxplot(x, g, st, dt, .3, .7, True, True, True)
p4 = make_boxplot(x, g, st, dt, .3, .5, False, False, True)

p5 = make_violinplot(x, g, st, dt, .3, .7, True, True, True)
p6 = make_violinplot(x, g, st, dt, .3, 0, False, False, True)

# make the bokeh version of the plot
d = {}
for level in df.c1.cat.categories:
    d.update({level: np.array(df[df['c1'] == level]['x3'])})

p7 = make_boxplot(x, g, st, dt, .5, .8, False, False, True)
p8 = BoxPlot(d, marker='circle', outliers=True, tools='')

# make a seaborn version of the boxplot
p9 = make_boxplot(x, g, st, dt, .5, .8, False, False, True)

sns.boxplot(g, x, data=df, color='c')

# render the plots
p = gridplot([[p1, p2], [p3, p4], [p5, p6], [p7, p8], [p9, mpl.to_bokeh()]])

show(p)
