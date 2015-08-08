# splot

This is a project to test out a few statistical plots based on the bokeh plotting package.  Other packages such as
pandas, numpy and scipy are also leveraged.  Currently,  this python code is written functionally,  not object oriented.
I would appreciate some help and guidance for turning these functions into methods on objects.

Here are some examples of the definition calls and the plots which are generated.

The first grouping of 6 plots below shows stripplot,  boxplot and violinplot of a continuous y variable vs a categorical
x variable.  The data for the plot is just some dummy random data generated using pandas and numpy.random.  

The plots on the left show what the plot looks like with the default call and no other options.  The plots on the right show the same data,  but with some other options (showing points,  outliers,  etc).

Note that the name of the variables (from the dateframe) are automatically used for the axis labels and each plot is given a default title of y vs x (I wish this was a overridable,  but gobal default for bokeh!)


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
