# splot

This is a project to test out a few statistical plots based on the bokeh plotting package.  Other packages such as
pandas, numpy and scipy are also leveraged.  Currently,  this python code is written functionally,  not object oriented.
I would appreciate some help and guidance for turning these functions into methods on objects.

Here are some examples of the definition calls and the plots which are generated.

The first grouping of 6 plots below shows stripplot,  boxplot and violinplot of a continuous y variable vs a categorical
x variable.  The data for the plot is just some dummy random data generated using pandas and numpy.random.  

The plots on the left show what the plot looks like with the default call and no other options.  The plots on the right show the same data,  but with some other options (showing points,  outliers,  etc).

Note that the name of the variables (from the dateframe) are automatically used for the axis labels and each plot is given a default title of y vs x (I wish this was the default behavior for bokeh!)


```python
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
```

![alt tag](https://github.com/rsgoodwin/splot/blob/master/example1.PNG)

The second groups of plots are from some data that is with the seaborn (and is also used to demonstrate plots in R using
lattice and ggplot)

```python
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
```

![alt tag](https://github.com/rsgoodwin/splot/blob/master/example2.PNG)
