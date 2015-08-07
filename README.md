# splot

This is a project to test out a few statistical plots based on the bokeh plotting library.  Other packages such as
pandas, numpy and scipy are also leveraged.  Currently,  this python code is written functionally,  not object oriented.
I would love some help and guidance turning these definitions into full fledged objects.

Here are some current example of the calls and the output that is generated.

The first grouping of 6 plots below shows stripplot,  boxplot and violinplot of a continuous x variable vs a categorical
y variable.  The data for the plot is just some dummy random data generated using pandas and numpy.random.  The plots on
the left show what the plot looks like with the defaults.  The plots on the right show the same data,  but with some
other options (showing points,  outliers,  etc)


```python
p1 = make_strip_plot(x='cv1', y='yv3', data=df)

p2 = make_strip_plot(x='cv1', y='yv3', data=df, jitter_points=True, jw=0.3)

p3 = make_box_plot(x='cv1', y='yv3', data=df)

p4 = make_box_plot(x='cv1', y='yv3', data=df, jw=.2, bw=.5, jitter_points=True,
                   show_points=True, show_outliers=True)

p5 = make_violin_plot(x='cv1', y='yv3', data=df)

p6 = make_violin_plot(x='cv1', y='yv3', data=df, jw=.2, vw=.7, jitter_points=True,
                      show_points=True, show_outliers=True)
```
![alt tag](https://github.com/rsgoodwin/splot/blob/master/example1.PNG)

The second groups of plots are from some data that is with the seaborn (and is also used to demonstrate plots in R using
lattice and ggplot)

```python
tips = sns.load_dataset("tips")

p7 = make_box_plot(x='day', y='total_bill', data=tips)

p8 = make_box_plot(x='day', y='total_bill', data=tips, jw=.15, bw=.7, jitter_points=True,
                   show_points=True, show_outliers=True)

p9 = make_violin_plot(x='day', y='total_bill', data=tips)

p10 = make_violin_plot(x='day', y='total_bill', data=tips, jw=.15, vw=.6, jitter_points=True,
                       show_points=True, show_outliers=True)
```

![alt tag](https://github.com/rsgoodwin/splot/blob/master/example2.PNG)
