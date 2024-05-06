# [Aspect ratio and size control tutorial](https://docs.makie.org/stable/tutorials/aspect-tutorial/#aspect_ratio_and_size_control_tutorial)

A very common problem in plotting is dealing with aspect ratios and other ways to precisely control figures.

For example, many plots need square axes. If you have looked at the documentation of `Axis`, you might know that it has an `aspect` attribute that can control the aspect ratio of the axis box. This aspect is not concerned with what the data limits are, it's just about the relative visual length of the axes.

Let's look at one common example, a square axis with a color bar next to it:

```julia
using CairoMakie

set_theme!(backgroundcolor = :gray90)

f = Figure(size = (800, 500))
ax = Axis(f[1, 1], aspect = 1)
Colorbar(f[1, 2])
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_514499fb.svg)

As you can see, the axis is square, but there's also a large gap between it and the colorbar. Why is that?

We can visualize the reason by adding a Box to the same cell where the axis is:

```julia
Box(f[1, 1], color = (:red, 0.2), strokewidth = 0)
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/aspect_tutorial_example.svg)

The red area of the box extends out into the whitespace left by the Axis. This demonstrates what the `aspect` keyword is actually doing. It reduces the size of the Axis, such that the chosen aspect ratio is achieved. It doesn't tell the layout that the Axis lives in "please make this cell adhere to this aspect ratio". As far as the layout is concerned, the Axis has an undefined size and its layout cell can therefore have any size that the layout deems correct, based on all other content of the layout and the figure size.

Therefore, using `aspect` will always cause gaps, unless the layout cell where the Axis lives happens to have exactly the correct aspect ratio by chance. This means `aspect` should only be used if the whitespace caused by it does not matter too much.

For all other cases, there is a different approach.

We want to force the layout to keep the axis cell at a specific aspect ratio. Therefore, we have to manipulate the layout itself, not the axis.

By default, each GridLayout row and column has a size of `Auto()`. This means that the size can depend on fixed-size content if there is any, otherwise it expands to fill the available space. If we want to force a cell to have an aspect ratio, we need to set either its respective row or column size to `Aspect`.

Let's try the example from above again, but this time we force the column of the Axis to have an aspect ratio of 1.0 relative to the row of the Axis, which is row 1.

```julia
f = Figure(size = (800, 500))
ax = Axis(f[1, 1])
Colorbar(f[1, 2])
colsize!(f.layout, 1, Aspect(1, 1.0))
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_30244828.svg)

As you can see, this time the colorbar sticks close to the axis, there is no unnecessary whitespace between them. We can visualize the effect of `Aspect` again with a red box, that shows us the extent of the layout cell:

```julia
Box(f[1, 1], color = (:red, 0.2), strokewidth = 0)
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_4e7f8a8f.svg)

So this time the layout cell itself is square, therefore the Axis that fills it is also square. Let me just demonstrate that we can play the same game again and give the Axis an `aspect` that is different from the square one that the layout cell has. This will again cause unnecessary whitespace:

```julia
ax.aspect = 0.5
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_b4205ee8.svg)

And now we change the column aspect again, to remove this gap:

```julia
colsize!(f.layout, 1, Aspect(1, 0.5))
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_497107d7.svg)

Let's return to our previous state with a square axis:

```julia
f = Figure(size = (800, 500))
ax = Axis(f[1, 1])
Colorbar(f[1, 2])
colsize!(f.layout, 1, Aspect(1, 1.0))
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_b0b4f0d6.svg)

Now you might think that there is no whitespace anymore between Axis and Colorbar, but there is a lot of it to the left and the right. Why can the layout not fix this problem for us?

Well, in Makie, the layout has to operate within the confines of the figure size that we have set. It cannot just decrease the figure size if there's too little content. This is because lots of times, figures are created to fit the sizing rules of some academic journal exactly, therefore the content you plot is not allowed to mess with the figure size.

So what we have done in our example is introducing constraints to the sizes of objects in our layout, such that it's impossible to fill all the space that is theoretically available. If you think about it, it's impossible to fill this Figure with a square axis and a thin colorbar while filling the rectangular space. We need a smaller figure!

But how small should it be exactly? It would be quite difficult to eyeball this, but thankfully there's a function for this exact purpose. By calling `resize_to_layout!`, we can adjust the figure size to the size that the layout needs for all its content.

Let's try it out:

```julia
resize_to_layout!(f)
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_fe0cb179.svg)

As you can see, the whitespace at the sides has been trimmed. (If the scaling looks smaller or bigger, that is just because of the display on this site, not the underlying figure size).

This technique is useful for all kinds of situations where the content should decide the figure size, and not the other way around.

For example, let's say we have a facet plot with 25 square axes which are all of size 150 by 150. We can just make these axes with fixed widths and heights. The `Auto` sized columns and rows of the default layout pick up these measurements and adjust themselves accordingly.

Of course, the figure size will by default not be appropriate for such an arrangement, and the content will clip:

```julia
f = Figure()
for i in 1:5, j in 1:5
    Axis(f[i, j], width = 150, height = 150)
end
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_fdc02e3a.svg)

But like before we can call `resize_to_layout!` and the size will be corrected so no clipping occurs.

```julia
resize_to_layout!(f)
f
```

![](https://docs.makie.org/stable/assets/tutorials/aspect-tutorial/code/output/example_c7311eb4.svg)

# [Preface](https://docs.makie.org/stable/tutorials/basic-tutorial/#preface)

Here is a quick tutorial to get you started with Makie!

Makie is the name of the whole plotting ecosystem and `Makie.jl` is the main package that describes how plots work. To actually render and save plots, we need a backend that knows how to translate plots into images or vector graphics.

There are three main backends which you can use to render plots (for more information, have a look at [Backends](https://docs.makie.org/stable/explanations/backends/index.html#backends)):

- `CairoMakie.jl` if you want to render vector graphics or high quality 2D images and don't need interactivity or true 3D rendering.
    
- `GLMakie.jl` if you need interactive windows and true 3D rendering but no vector output.
    
- Or `WGLMakie.jl` which is similar to `GLMakie` but works in web browsers, not native windows.
    

This tutorial uses CairoMakie, but the code can be executed with any backend. Note that CairoMakie can _create_ images but it cannot _display_ them.

To see the output of plotting commands when using CairoMakie, we recommend you either use an IDE which supports png or svg output, such as VSCode, Atom/Juno, Jupyter, Pluto, etc., or try using a viewer package such as [ElectronDisplay.jl](https://github.com/queryverse/ElectronDisplay.jl), or alternatively save your plots to files directly. The Julia REPL by itself does not have the ability to show the plots.

Ok, now that this is out of the way, let's get started!

## [Importing](https://docs.makie.org/stable/tutorials/basic-tutorial/#importing)

First, we import CairoMakie. This makes all the exported symbols from `Makie.jl` available as well.

```julia
using CairoMakie
```

## [Important objects](https://docs.makie.org/stable/tutorials/basic-tutorial/#important_objects)

The objects most important for our first steps with Makie are the `Figure`, the `Axis` and plots. In a normal Makie plot you will usually find a `Figure` which contains an `Axis` which contains one or more plot objects like `Lines` or `Scatter`.

In the next steps, we will take a look at how we can create these objects.

## [An empty figure](https://docs.makie.org/stable/tutorials/basic-tutorial/#an_empty_figure)

The basic container object in Makie is the [`Figure`](https://docs.makie.org/stable/api/#Figure). It is a canvas onto which we can add objects like `Axis`, `Colorbar`, `Legend` and others.

Let's create a `Figure` and give it a background color other than the default white so we can see it. Returning a `Figure` from an expression will `display` it if your coding environment can show images.

```julia
f = Figure(backgroundcolor = :tomato)
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_bf37b103.svg)

Another common thing to do is to give a figure a different size. The default is 800x600, let's try halving the height:

```julia
f = Figure(backgroundcolor = :tomato, size = (800, 300))
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_e9fd1799.svg)

## [Adding an Axis](https://docs.makie.org/stable/tutorials/basic-tutorial/#adding_an_axis)

The most common object you can add to a figure which you need for most plotting is the [Axis](https://docs.makie.org/stable/reference/blocks/axis/index.html#axis). The usual syntax for adding such an object to a figure is to specify a position in the `Figure`'s layout as the first argument. We'll learn more about layouts later, but for now the position `f[1, 1]` will just fill the whole figure.

```julia
f = Figure()
ax = Axis(f[1, 1])
f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_b26cf0eb.svg)

The default axis has no title or labels, you can pass those as keyword arguments. For a whole list of available attributes, check the docstring for [`Axis`](https://docs.makie.org/stable/api/#Axis) (you can also do that by running `?Axis` in the REPL). Be warned, it's very long!

```julia
f = Figure()
ax = Axis(f[1, 1],
    title = "A Makie Axis",
    xlabel = "The x label",
    ylabel = "The y label"
)
f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_34abb989.svg)

## [Adding a plot to an Axis](https://docs.makie.org/stable/tutorials/basic-tutorial/#adding_a_plot_to_an_axis)

Now we're ready to actually plot something into an `Axis`!

Makie has many different plotting functions, the first we will learn about is [lines!](https://docs.makie.org/stable/reference/plots/lines/index.html#lines). Let's try plotting a sine function into an `Axis`, by passing it as the first argument:

```julia
f = Figure()
ax = Axis(f[1, 1])
x = range(0, 10, length=100)
y = sin.(x)
lines!(ax, x, y)
f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_4b86fd02.svg)

There we have our first line plot.

## [Scatter plot](https://docs.makie.org/stable/tutorials/basic-tutorial/#scatter_plot)

Another common function is [scatter!](https://docs.makie.org/stable/reference/plots/scatter/index.html#scatter). It works very similar to `lines!` but shows separate markers for each input point.

```julia
f = Figure()
ax = Axis(f[1, 1])
x = range(0, 10, length=100)
y = sin.(x)
scatter!(ax, x, y)
f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_c9748f6f.svg)

## [Creating Figure, Axis and plot in one call](https://docs.makie.org/stable/tutorials/basic-tutorial/#creating_figure_axis_and_plot_in_one_call)

So far we have seen how to plot into an existing `Axis` with `lines!` and `scatter!`.

However, it would be nice if we didn't have to explicitly create `Figure` and `Axis` for every plot that we're making.

That's why every plotting function comes in a pair, one version that plots into an existing `Axis` and one that creates its own `Axis` implicitly for convenience. For example, `lines!` mutates an existing `Axis`, `lines` creates an implicit one, `scatter!` mutates, `scatter` does not, and so on.

Let's see how to make a line plot without creating `Figure` and `Axis` ourselves first.

```julia
x = range(0, 10, length=100)
y = sin.(x)
lines(x, y)
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_1d097e0a.svg)

The return type of `lines(x, y)` is `FigureAxisPlot`. The `lines` function first creates a `Figure`, then puts an `Axis` into it and finally adds a plot of type `Lines` to that axis.

Because these three objects are created at once, the function returns all three, just bundled up into one `FigureAxisPlot` object. That's just so we can overload the `display` behavior for that type to match `Figure`. Normally, multiple return values are returned as `Tuple`s in Julia but it's uncommon to overload `display` for `Tuple` types.

If you need the objects, for example to add more things to the figure later and edit axis and plot attributes, you could destructure the return value:

```julia
figure, axis, lineplot = lines(x, y)
figure
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_e024b4c6.svg)

As you can see, the output of returning the extracted figure is the same.

## [Passing Figure and Axis styles](https://docs.makie.org/stable/tutorials/basic-tutorial/#passing_figure_and_axis_styles)

You might wonder how to specify a different resolution for this scatter plot, or set an axis title and labels. Because a normal plotting function like `lines` or `scatter` creates these objects before it creates the plot, you can pass special keyword arguments to it called `axis` and `figure`. You can pass any kind of object with symbol-value pairs and these will be used as keyword arguments for `Figure` and `Axis`, respectively.

```julia
x = range(0, 10, length=100)
y = sin.(x)
scatter(x, y;
    figure = (; size = (400, 400)),
    axis = (; title = "Scatter plot", xlabel = "x label")
)
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_79588abc.svg)

The `;` in `(; size = (400, 400))` is nothing special, it just clarifies that we want a one-element `NamedTuple` and not a variable called `size`. It's good habit to include it but it's not needed for `NamedTuple`s with more than one entry.

## [Argument conversions](https://docs.makie.org/stable/tutorials/basic-tutorial/#argument_conversions)

So far we have called `lines` and `scatter` with `x` and `y` arguments, where `x` was a range object and `y` vector of numbers. Most plotting functions have different options how you can call them. The input arguments are converted internally to one or more target representations that can be handled by the rendering backends.

Here are a few different examples of what you can use with `lines`:

An interval and a function:

```julia
lines(0..10, sin)
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_6e691a0c.svg)

A collection of numbers and a function:

```julia
lines(0:1:10, cos)
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_ad618f31.svg)

A collection of `Point`s from `GeometryBasics.jl` (which supplies most geometric primitives in Makie):

```julia
lines([Point(0, 0), Point(5, 10), Point(10, 5)])
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_77f6e6de.svg)

The input arguments you can use with `lines` and `scatter` are mostly the same because they have the same conversion trait `PointBased`. Other plotting functions have different conversion traits, [heatmap](https://docs.makie.org/stable/reference/plots/heatmap/index.html#heatmap) for example expects two-dimensional grid data. The respective trait is called `CellGrid`.

## [Layering multiple plots](https://docs.makie.org/stable/tutorials/basic-tutorial/#layering_multiple_plots)

As we've seen above, every plotting function has a version with and one without `!` at the end. For example, there's `scatter` and `scatter!`, `lines` and `lines!`, etc.

To plot two things into the same axis, you can use the mutating plotting functions like `lines!` and `scatter!`. For example, here's how you could plot two lines on top of each other:

```julia
x = range(0, 10, length=100)

f, ax, l1 = lines(x, sin)
l2 = lines!(ax, x, cos)
f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_3ce15027.svg)

The second `lines!` call plots into the axis created by the first `lines` call. It's colored differently because the `Axis` keeps track of what has been plotted into it and cycles colors for similar plotting functions.

You can also leave out the axis argument for convenience, then the axis being used is the `current_axis()`, which is usually just the axis that was created last.

```julia
x = range(0, 10, length=100)

f, ax, l1 = lines(x, sin)
lines!(x, cos)
f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_5eb66f5d.svg)

Note that you cannot pass `figure` and `axis` keywords to mutating plotting functions like `lines!` or `scatter!`. That's because they don't create an `Figure` and `Axis`, and we chose not to allow modification of the existing objects in plotting calls so it's clearer what is going on.

## [Attributes](https://docs.makie.org/stable/tutorials/basic-tutorial/#attributes)

Every plotting function has attributes which you can set through keyword arguments. The lines in the previous example have colors from Makie's default palette, but we can easily specify our own.

There are multiple ways you can specify colors, but common ones are:

- By name, like `:red` or `"red"`
    
- By hex string, like `"#ffccbk"`
    
- With color types like the Makie-exported `RGBf(0.5, 0, 0.6)` or `RGBAf(0.3, 0.8, 0.2, 0.8)`
    
- As a tuple where the first part is a color and the second an alpha value to make it transparent, like `(:red, 0.5)`
    

You can read more about colors at [juliagraphics.github.io/Colors.jl](https://juliagraphics.github.io/Colors.jl).

Here's a plot with one named color and one where we use `RGBf`:

```julia
x = range(0, 10, length=100)

f, ax, l1 = lines(x, sin, color = :tomato)
l2 = lines!(ax, x, cos, color = RGBf(0.2, 0.7, 0.9))
f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_205e27a3.svg)

Other plotting functions have different attributes. The function `scatter`, for example, does not only have the `color` attribute, but also a `markersize` attribute.

You can read about all possible attributes by running `?scatter` in the REPL, and examples are shown on the page [scatter](https://docs.makie.org/stable/reference/plots/scatter/index.html#scatter).

```julia
x = range(0, 10, length=100)

f, ax, sc1 = scatter(x, sin, color = :red, markersize = 5)
sc2 = scatter!(ax, x, cos, color = :blue, markersize = 10)
f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_67db1296.svg)

You can also manipulate most plot attributes afterwards with the syntax `plot.attribute = new_value`.

```julia
sc1.marker = :utriangle
sc1.markersize = 20

sc2.color = :transparent
sc2.markersize = 20
sc2.strokewidth = 1
sc2.strokecolor = :purple

f
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_1d6160db.svg)

## [Array attributes](https://docs.makie.org/stable/tutorials/basic-tutorial/#array_attributes)

A lot of attributes can be set to either a single value or an array with as many elements as there are data points. For example, it is usually much more performant to draw many points with one scatter object, than to create many scatter objects with one point each.

Here, we vary markersize and color:

```julia
x = range(0, 10, length=100)

scatter(x, sin,
    markersize = range(5, 15, length=100),
    color = range(0, 1, length=100),
    colormap = :thermal
)
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_2fae83cf.svg)

Note that the color array does not actually contain colors, rather the numerical values are mapped to the plot's `colormap`. There are many different colormaps to choose from, take a look on the [Colors](https://docs.makie.org/stable/explanations/colors/index.html#colors) page.

The values are mapped to colors via the `colorrange` attribute, which by default goes from the minimum to the maximum color value. But we can also limit or expand the range manually. For example, we can constrain the previous scatter plot's color range to (0.33, 0.66), which will clip the colors at the bottom and the top.

```julia
x = range(0, 10, length=100)

scatter(x, sin,
    markersize = range(5, 15, length=100),
    color = range(0, 1, length=100),
    colormap = :thermal,
    colorrange = (0.33, 0.66)
)
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_36c473bb.svg)

Of course you can also use an array of colors directly, in which case the `colorrange` is ignored:

```julia
using CairoMakie

x = range(0, 10, length=100)

colors = repeat([:crimson, :dodgerblue, :slateblue1, :sienna1, :orchid1], 20)

scatter(x, sin, color = colors, markersize = 20)
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_76f1aed3.svg)

## [Simple legend](https://docs.makie.org/stable/tutorials/basic-tutorial/#simple_legend)

If you add label attributes to your plots, you can call the `axislegend` function to add a `Legend` with all labeled plots to the current `Axis`, or optionally to one you pass as the first argument.

```julia
using CairoMakie

x = range(0, 10, length=100)

lines(x, sin, color = :red, label = "sin")
lines!(x, cos, color = :blue, label = "cos")
axislegend()
current_figure()
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_fe174e64.svg)

## [Subplots](https://docs.makie.org/stable/tutorials/basic-tutorial/#subplots)

Makie uses a powerful layout system under the hood, which allows you to create very complex figures with many subplots. So far, we have only used the default position [1, 1], where the Axis is created in a standard plotting call.

We can make subplots by giving the location of the subplot in our layout grid as the first argument to our plotting function. The basic syntax for specifying the location in a figure is `fig[row, col]`.

```julia
using CairoMakie

x = LinRange(0, 10, 100)
y = sin.(x)

fig = Figure()
lines(fig[1, 1], x, y, color = :red)
lines(fig[1, 2], x, y, color = :blue)
lines(fig[2, 1:2], x, y, color = :green)

fig
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_c9ffcd2a.svg)

Each `lines` call creates a new axis in the position given as the first argument, that's why we use `lines` and not `lines!` here.

We can also create a couple of axes manually at first and then plot into them later. For example, we can create a figure with three axes.

```julia
using CairoMakie

fig = Figure()
ax1 = Axis(fig[1, 1])
ax2 = Axis(fig[1, 2])
ax3 = Axis(fig[2, 1:2])
fig
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_ed86e528.svg)

And then we can continue to plot into these empty axes.

```julia
lines!(ax1, 0..10, sin)
lines!(ax2, 0..10, cos)
lines!(ax3, 0..10, sqrt)
fig
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_f65269a8.svg)

## [Legend and Colorbar](https://docs.makie.org/stable/tutorials/basic-tutorial/#legend_and_colorbar)

We have seen two `Blocks` so far, the [Axis](https://docs.makie.org/stable/reference/blocks/axis/index.html#axis) and the [Legend](https://docs.makie.org/stable/tutorials/layout-tutorial/index.html#legend) which was created by the function `axislegend`. All `Block`s can be placed into the layout of a figure at arbitrary positions, which makes it easy to assemble complex figures.

In the same way as with the [Axis](https://docs.makie.org/stable/reference/blocks/axis/index.html#axis) before, you can also create a [Legend](https://docs.makie.org/stable/tutorials/layout-tutorial/index.html#legend) manually and then place it freely, wherever you want, in the figure. There are multiple ways to create [Legend](https://docs.makie.org/stable/tutorials/layout-tutorial/index.html#legend)s, for one of them you pass one vector of plot objects and one vector of label strings.

You can see here that we can deconstruct the return value from the two `lines` calls into one newly created axis and one plot object each. We can then feed the plot objects to the legend constructor. We place the legend in the second column and across both rows, which centers it nicely next to the two axes.

```julia
using CairoMakie

fig = Figure()
ax1, l1 = lines(fig[1, 1], 0..10, sin, color = :red)
ax2, l2 = lines(fig[2, 1], 0..10, cos, color = :blue)
Legend(fig[1:2, 2], [l1, l2], ["sin", "cos"])
fig
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_e51a7527.svg)

The [Colorbar](https://docs.makie.org/stable/reference/blocks/colorbar/index.html#colorbar) works in a very similar way. We just need to pass a position in the figure to it, and one plot object. In this example, we use a `heatmap`.

You can see here that we split the return value of `heatmap` into three parts: the newly created figure, the axis and the heatmap plot object. This is useful as we can then continue with the figure `fig` and the heatmap `hm` which we need for the colorbar.

```julia
using CairoMakie

fig, ax, hm = heatmap(randn(20, 20))
Colorbar(fig[1, 2], hm)
fig
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_6fb7599e.svg)

The previous short syntax is basically equivalent to this longer, manual version. You can switch between those workflows however you please.

```julia
using CairoMakie

fig = Figure()
ax = Axis(fig[1, 1])
hm = heatmap!(ax, randn(20, 20))
Colorbar(fig[1, 2], hm)
fig
```

![](https://docs.makie.org/stable/assets/tutorials/basic-tutorial/code/output/example_5666cc5e.svg)

## [Next steps](https://docs.makie.org/stable/tutorials/basic-tutorial/#next_steps)

We've only looked at a small subset of Makie's functionality here.

You can read about the different available plotting functions with examples in the [Plotting Functions](https://docs.makie.org/stable/tutorials/basic-tutorial/#) section.

If you want to learn about making complex figures with nested sublayouts, have a look at the [Layout Tutorial](https://docs.makie.org/stable/tutorials/layout-tutorial/index.html#layout_tutorial) section.

If you're interested in creating interactive visualizations that use Makie's special `Observables` workflow, this is explained in more detail in the [Observables & Interaction](https://docs.makie.org/stable/explanations/nodes/index.html#observables_interaction) section.

If you want to create animated movies, y
ou can find more information in the [Animations](https://docs.makie.org/stable/explanations/animation/index.html#animations) section.

# [Layout Tutorial](https://docs.makie.org/stable/tutorials/layout-tutorial/#layout_tutorial)

In this tutorial, you will learn how to create a complex figure using Makie's layout tools.

Let's say that we want to create the following figure:

![final_result.png](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/final_result.png)

Here's the full code for reference:

```julia
using CairoMakie
using Makie.FileIO

f = Figure(backgroundcolor = RGBf(0.98, 0.98, 0.98),
    size = (1000, 700))
ga = f[1, 1] = GridLayout()
gb = f[2, 1] = GridLayout()
gcd = f[1:2, 2] = GridLayout()
gc = gcd[1, 1] = GridLayout()
gd = gcd[2, 1] = GridLayout()
axtop = Axis(ga[1, 1])
axmain = Axis(ga[2, 1], xlabel = "before", ylabel = "after")
axright = Axis(ga[2, 2])

linkyaxes!(axmain, axright)
linkxaxes!(axmain, axtop)

labels = ["treatment", "placebo", "control"]
data = randn(3, 100, 2) .+ [1, 3, 5]

for (label, col) in zip(labels, eachslice(data, dims = 1))
    scatter!(axmain, col, label = label)
    density!(axtop, col[:, 1])
    density!(axright, col[:, 2], direction = :y)
end

ylims!(axtop, low = 0)
xlims!(axright, low = 0)

axmain.xticks = 0:3:9
axtop.xticks = 0:3:9

leg = Legend(ga[1, 2], axmain)

hidedecorations!(axtop, grid = false)
hidedecorations!(axright, grid = false)
leg.tellheight = true

colgap!(ga, 10)
rowgap!(ga, 10)

Label(ga[1, 1:2, Top()], "Stimulus ratings", valign = :bottom,
    font = :bold,
    padding = (0, 0, 5, 0))

xs = LinRange(0.5, 6, 50)
ys = LinRange(0.5, 6, 50)
data1 = [sin(x^1.5) * cos(y^0.5) for x in xs, y in ys] .+ 0.1 .* randn.()
data2 = [sin(x^0.8) * cos(y^1.5) for x in xs, y in ys] .+ 0.1 .* randn.()

ax1, hm = contourf(gb[1, 1], xs, ys, data1,
    levels = 6)
ax1.title = "Histological analysis"
contour!(ax1, xs, ys, data1, levels = 5, color = :black)
hidexdecorations!(ax1)

ax2, hm2 = contourf(gb[2, 1], xs, ys, data2,
    levels = 6)
contour!(ax2, xs, ys, data2, levels = 5, color = :black)

cb = Colorbar(gb[1:2, 2], hm, label = "cell group")
low, high = extrema(data1)
edges = range(low, high, length = 7)
centers = (edges[1:6] .+ edges[2:7]) .* 0.5
cb.ticks = (centers, string.(1:6))

cb.alignmode = Mixed(right = 0)

colgap!(gb, 10)
rowgap!(gb, 10)

brain = load(assetpath("brain.stl"))

ax3d = Axis3(gc[1, 1], title = "Brain activation")
m = mesh!(
    ax3d,
    brain,
    color = [tri[1][2] for tri in brain for i in 1:3],
    colormap = Reverse(:magma),
)
Colorbar(gc[1, 2], m, label = "BOLD level")

axs = [Axis(gd[row, col]) for row in 1:3, col in 1:2]
hidedecorations!.(axs, grid = false, label = false)

for row in 1:3, col in 1:2
    xrange = col == 1 ? (0:0.1:6pi) : (0:0.1:10pi)

    eeg = [sum(sin(pi * rand() + k * x) / k for k in 1:10)
        for x in xrange] .+ 0.1 .* randn.()

    lines!(axs[row, col], eeg, color = (:black, 0.5))
end

axs[3, 1].xlabel = "Day 1"
axs[3, 2].xlabel = "Day 2"

Label(gd[1, :, Top()], "EEG traces", valign = :bottom,
    font = :bold,
    padding = (0, 0, 5, 0))

rowgap!(gd, 10)
colgap!(gd, 10)

for (i, label) in enumerate(["sleep", "awake", "test"])
    Box(gd[i, 3], color = :gray90)
    Label(gd[i, 3], label, rotation = pi/2, tellheight = false)
end

colgap!(gd, 2, 0)

n_day_1 = length(0:0.1:6pi)
n_day_2 = length(0:0.1:10pi)

colsize!(gd, 1, Auto(n_day_1))
colsize!(gd, 2, Auto(n_day_2))

for (label, layout) in zip(["A", "B", "C", "D"], [ga, gb, gc, gd])
    Label(layout[1, 1, TopLeft()], label,
        fontsize = 26,
        font = :bold,
        padding = (0, 5, 5, 0),
        halign = :right)
end

colsize!(f.layout, 1, Auto(0.5))

rowsize!(gcd, 1, Auto(1.5))

f
```

How do we approach this task?

In the following sections, we'll go over the process step by step. We're not always going to use the shortest possible syntax, as the main goal is to get a better understanding of the logic and the available options.

## [Basic layout plan](https://docs.makie.org/stable/tutorials/layout-tutorial/#basic_layout_plan)

When building figures, you always think in terms of rectangular boxes. We want to find the biggest boxes that enclose meaningful groups of content, and then we realize those boxes either using `GridLayout` or by placing content objects there.

If we look at our target figure, we can imagine one box around each of the labelled areas A, B, C and D. But A and C are not in one row, neither are B and D. This means that we don't use a 2x2 GridLayout, but have to be a little more creative.

We could say that A and B are in one column, and C and D are in one column. We can have different row heights for both groups by making one big nested `GridLayout` within the second column, in which we place C and D. This way the rows of column 2 are decoupled from column 1.

Ok, let's create the figure first with a gray backgroundcolor, and a predefined font:

```julia
using CairoMakie
using FileIO

f = Figure(backgroundcolor = RGBf(0.98, 0.98, 0.98),
    size = (1000, 700))
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_f3d79cee.png)

## [Setting up GridLayouts](https://docs.makie.org/stable/tutorials/layout-tutorial/#setting_up_gridlayouts)

Now, let's make the four nested GridLayouts that are going to hold the objects of A, B, C and D. There's also the layout that holds C and D together, so the rows are separate from A and B. We are not going to see anything yet as we have no visible content, but that will come soon.

Note

It's not strictly necessary to first create separate `GridLayout`s, then use them to place objects in the figure. You can also implicitly create nested grids using multiple indexing, for example like `Axis(f[1, 2:3][4:5, 6])`. This is further explained in [GridPositions and GridSubpositions](https://docs.makie.org/stable/explanations/figure/index.html#gridpositions_and_gridsubpositions). But if you want to manipulate your nested grids afterwards, for example to change column sizes or row gaps, it's easier if you have them stored in variables already.

```julia
ga = f[1, 1] = GridLayout()
gb = f[2, 1] = GridLayout()
gcd = f[1:2, 2] = GridLayout()
gc = gcd[1, 1] = GridLayout()
gd = gcd[2, 1] = GridLayout()
```

## [Panel A](https://docs.makie.org/stable/tutorials/layout-tutorial/#panel_a)

Now we can start placing objects into the figure. We start with A.

There are three axes and a legend. We can place the axes first, link them appropriately, and plot the first data into them.

```julia
axtop = Axis(ga[1, 1])
axmain = Axis(ga[2, 1], xlabel = "before", ylabel = "after")
axright = Axis(ga[2, 2])

linkyaxes!(axmain, axright)
linkxaxes!(axmain, axtop)

labels = ["treatment", "placebo", "control"]
data = randn(3, 100, 2) .+ [1, 3, 5]

for (label, col) in zip(labels, eachslice(data, dims = 1))
    scatter!(axmain, col, label = label)
    density!(axtop, col[:, 1])
    density!(axright, col[:, 2], direction = :y)
end

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_014ac2be.png)

There's a small gap between the density plots and their axes, which we can remove by fixing one side of the limits.

```julia
ylims!(axtop, low = 0)
xlims!(axright, low = 0)

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_46b0e664.png)

We can also choose different x ticks with whole numbers.

```julia
axmain.xticks = 0:3:9
axtop.xticks = 0:3:9

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_3fbe3569.png)

### [Legend](https://docs.makie.org/stable/tutorials/layout-tutorial/#legend)

We have set the `label` attribute in the scatter call so it's easier to construct the legend. We can just pass `axmain` as the second argument to `Legend`.

```julia
leg = Legend(ga[1, 2], axmain)

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_0b2e02f2.png)

### [Legend Tweaks](https://docs.makie.org/stable/tutorials/layout-tutorial/#legend_tweaks)

There are a couple things we want to change. There are unnecessary decorations for the side axes, which we are going to hide.

Also, the top axis does not have the same height as the legend. That's because a legend is usually used on the right of an `Axis` and is therefore preset with `tellheight = false`. We set this attribute to `true` so the row in which the legend sits can contract to its known size.

```julia
hidedecorations!(axtop, grid = false)
hidedecorations!(axright, grid = false)
leg.tellheight = true

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_08d743bd.png)

The axes are still a bit too far apart, so we reduce column and row gaps.

```julia
colgap!(ga, 10)
rowgap!(ga, 10)

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_965af4c3.png)

We can make a title by placing a label across the top two elements.

```julia
Label(ga[1, 1:2, Top()], "Stimulus ratings", valign = :bottom,
    font = :bold,
    padding = (0, 0, 5, 0))

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_c43e9c5c.png)

## [Panel B](https://docs.makie.org/stable/tutorials/layout-tutorial/#panel_b)

Let's move to B. We have two axes stacked on top of each other, and a colorbar alongside them. This time, we create the axes by just plotting into the right `GridLayout` slots. This can be more convenient than creating an `Axis` first.

```julia
xs = LinRange(0.5, 6, 50)
ys = LinRange(0.5, 6, 50)
data1 = [sin(x^1.5) * cos(y^0.5) for x in xs, y in ys] .+ 0.1 .* randn.()
data2 = [sin(x^0.8) * cos(y^1.5) for x in xs, y in ys] .+ 0.1 .* randn.()

ax1, hm = contourf(gb[1, 1], xs, ys, data1,
    levels = 6)
ax1.title = "Histological analysis"
contour!(ax1, xs, ys, data1, levels = 5, color = :black)
hidexdecorations!(ax1)

ax2, hm2 = contourf(gb[2, 1], xs, ys, data2,
    levels = 6)
contour!(ax2, xs, ys, data2, levels = 5, color = :black)

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_c43b4e0e.png)

### [Colorbar](https://docs.makie.org/stable/tutorials/layout-tutorial/#colorbar)

Now we need a colorbar. Because we haven't set specific edges for the two contour plots, just how many levels there are, we can make a colorbar using one of the contour plots and then label the bins in there from one to six.

```julia
cb = Colorbar(gb[1:2, 2], hm, label = "cell group")
low, high = extrema(data1)
edges = range(low, high, length = 7)
centers = (edges[1:6] .+ edges[2:7]) .* 0.5
cb.ticks = (centers, string.(1:6))

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_d3d39e74.png)

#### [Mixed alignmode](https://docs.makie.org/stable/tutorials/layout-tutorial/#mixed_alignmode)

The right edge of the colorbar is currently aligned with the right edge of the upper density plot. This can later cause a bit of a gap between the density plot and content on the right.

In order to improve this, we can pull the colorbar labels into its layout cell using the `Mixed` alignmode. The keyword `right = 0` means that the right side of the colorbar should pull its protrusion content inward with an additional padding of `0`.

```julia
cb.alignmode = Mixed(right = 0)

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_7d00650e.png)

As in A, the axes are a bit too far apart.

```julia
colgap!(gb, 10)
rowgap!(gb, 10)

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_6161fd40.png)

## [Panel C](https://docs.makie.org/stable/tutorials/layout-tutorial/#panel_c)

Now, we move on to panel C. This is just an `Axis3` with a colorbar on the side.

```julia
brain = load(assetpath("brain.stl"))

ax3d = Axis3(gc[1, 1], title = "Brain activation")
m = mesh!(
    ax3d,
    brain,
    color = [tri[1][2] for tri in brain for i in 1:3],
    colormap = Reverse(:magma),
)
Colorbar(gc[1, 2], m, label = "BOLD level")

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_b12a4e74.png)

Note that the z label overlaps the plot to the left a little bit. `Axis3` can't have automatic protrusions because the label positions change with the projection and the cell size of the axis, which is different from the 2D `Axis`.

You can set the attribute `ax3.protrusions` to a tuple of four values (left, right, bottom, top) but in this case we just continue plotting until we have all objects that we want, before we look if small tweaks like that are necessary.

## [Panel D](https://docs.makie.org/stable/tutorials/layout-tutorial/#panel_d)

We move on to Panel D, which has a grid of 3x2 axes.

```julia
axs = [Axis(gd[row, col]) for row in 1:3, col in 1:2]
hidedecorations!.(axs, grid = false, label = false)

for row in 1:3, col in 1:2
    xrange = col == 1 ? (0:0.1:6pi) : (0:0.1:10pi)

    eeg = [sum(sin(pi * rand() + k * x) / k for k in 1:10)
        for x in xrange] .+ 0.1 .* randn.()

    lines!(axs[row, col], eeg, color = (:black, 0.5))
end

axs[3, 1].xlabel = "Day 1"
axs[3, 2].xlabel = "Day 2"

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_bbb4e093.png)

We can make a little title for the six axes by placing a `Label` in the top protrusion of row 1 and across both columns.

```julia
Label(gd[1, :, Top()], "EEG traces", valign = :bottom,
    font = :bold,
    padding = (0, 0, 5, 0))

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_956013f1.png)

Again, we bring the subplots closer together by reducing gap sizes.

```julia
rowgap!(gd, 10)
colgap!(gd, 10)

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_3107bb52.png)

### [EEG labels](https://docs.makie.org/stable/tutorials/layout-tutorial/#eeg_labels)

Now, we add three boxes on the side with labels in them. In this case, we just place them in another column to the right.

```julia
for (i, label) in enumerate(["sleep", "awake", "test"])
    Box(gd[i, 3], color = :gray90)
    Label(gd[i, 3], label, rotation = pi/2, tellheight = false)
end

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_142b4f5f.png)

The boxes are in the correct positions, but we still need to remove the column gap.

```julia
colgap!(gd, 2, 0)

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_c88290a8.png)

### [Scaling axes relatively](https://docs.makie.org/stable/tutorials/layout-tutorial/#scaling_axes_relatively)

The fake eeg data we have created has more datapoints on day 1 than day 2. We want to scale the axes so that they both have the same zoom level. We can do this by setting the column widths to `Auto(x)` where x is a number proportional to the number of data points of the axis. This way, both will have the same relative scaling.

```julia
n_day_1 = length(0:0.1:6pi)
n_day_2 = length(0:0.1:10pi)

colsize!(gd, 1, Auto(n_day_1))
colsize!(gd, 2, Auto(n_day_2))

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_f4f316a2.png)

## [Subplot labels](https://docs.makie.org/stable/tutorials/layout-tutorial/#subplot_labels)

Now, we can add the subplot labels. We already have our four `GridLayout` objects that enclose each panel's content, so the easiest way is to create `Label`s in the top left protrusion of these layouts. That will leave all other alignments intact, because we're not creating any new columns or rows. The labels belong to the gaps between the layouts instead.

```julia
for (label, layout) in zip(["A", "B", "C", "D"], [ga, gb, gc, gd])
    Label(layout[1, 1, TopLeft()], label,
        fontsize = 26,
        font = :bold,
        padding = (0, 5, 5, 0),
        halign = :right)
end

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_255b77bb.png)

## [Final tweaks](https://docs.makie.org/stable/tutorials/layout-tutorial/#final_tweaks)

This looks pretty good already, but the first column of the layout is a bit too wide. We can reduce the column width by setting it to `Auto` with a number smaller than 1, for example. This gives the column a smaller weight when distributing widths between all columns with `Auto` sizes.

You can also use `Relative` or `Fixed` but they are not as flexible if you add more things later, so I prefer using `Auto`.

```julia
colsize!(f.layout, 1, Auto(0.5))

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/example_726c1f57.png)

The EEG traces are currently as high as the brain axis, let's increase the size of the row with the panel C layout a bit so it has more space.

And that is the final result:

```julia
rowsize!(gcd, 1, Auto(1.5))

f
```

![](https://docs.makie.org/stable/assets/tutorials/layout-tutorial/code/output/final_result.png)


# [Scene tutorial](https://docs.makie.org/stable/tutorials/scenes/#scene_tutorial)

The scene constructor:

```julia
scene = Scene(;
    # clear everything behind scene
    clear = true,
    # the camera struct of the scene.
    visible = true,
    # ssao and light are explained in more detail in `Documetation/Lighting`
    ssao = Makie.SSAO(),
    # Creates lights from theme, which right now defaults to `
    # set_theme!(lightposition=:eyeposition, ambient=RGBf(0.5, 0.5, 0.5))`
    lights = Makie.automatic,
    backgroundcolor = :gray,
    size = (500, 500);
    # gets filled in with the currently set global theme
    theme_kw...
)
```

A scene is doing four things:

- holds a local theme, that gets applied to all plot objects in that scene
    
- manages the camera, projection and transformation matrices
    
- defines the window size. For sub-scenes, the child scene can have smaller window areas than the parent area.
    
- holds a reference to all window events
    

## [Scenes and subwindows](https://docs.makie.org/stable/tutorials/scenes/#scenes_and_subwindows)

With scenes, one can create subwindows. The window extends are given by a `Rect{2, Int}` and the position is always in window pixels and relative to the parent.

```julia
using GLMakie, Makie
GLMakie.activate!()
scene = Scene(backgroundcolor=:gray)
subwindow = Scene(scene, viewport=Rect(100, 100, 200, 200), clear=true, backgroundcolor=:white)
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_8c180ae6.png)

When using `Scenes` directly, one needs to manually set up the camera and center the camera to the content of the scene As described in more detail the camera section, we have multiple `cam***!` functions to set a certain projection and camera type for the scene.

```julia
cam3d!(subwindow)
meshscatter!(subwindow, rand(Point3f, 10), color=:gray)
center!(subwindow)
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_da233646.png)

Instead of a white background, we can also stop clearing the background to make the scene see-through, and give it an outline instead. The easiest way to create an outline is, to make a sub scene with a projection that goes from 0..1 for the whole window. To make a subscene with a certain projection type, Makie offers for each camera function a version without `!`, that will create a subscene, and apply the camera type. We call the space that goes from 0..1 `relative` space, so `camrelative` will give this projection:

```julia
subwindow.clear = false
relative_space = Makie.camrelative(subwindow)
# this draws a line at the scene window boundary
lines!(relative_space, Rect(0, 0, 1, 1))
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_43040ac8.png)

We can also now give the parent scene a more exciting background by using `campixel!` and plotting an image to the window:

```julia
campixel!(scene)
w, h = size(scene) # get the size of the scene in pixels
# this draws a line at the scene window boundary
image!(scene, [sin(i/w) + cos(j/h) for i in 1:w, j in 1:h])
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_9ae234ea.png)

We can fix this by translating the scene further back:

```julia
translate!(scene.plots[1], 0, 0, -10000)
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_6cdc80d2.png)

We need a fairly high translation, since the far + near plane for `campixel!` goes from `-1000` to `1000`, while for `cam3d!` those get automatically adjusted to the camera parameters. Both end up in the same depth buffer, transformed to the range `0..1` by the far & near plane, so to stay behind the 3D scene, it needs to be set to a high value.

With `clear = true` we wouldn't have this problem!

In GLMakie, we can actually take a look at the depth buffer, to see how it looks now:

```julia
screen = display(scene) # use display, to get a reference to the screen object
depth_color = GLMakie.depthbuffer(screen)
close(screen)
# Look at result:
f, ax, pl = heatmap(depth_color)
Colorbar(f[1, 2], pl)
f
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_be215c6a.png)

## [Window Events](https://docs.makie.org/stable/tutorials/scenes/#window_events)

Every scene also holds a reference to all global window events:

```julia
scene.events
```

```
Events:
  window_area:      GeometryBasics.HyperRectangle{2, Int64}([0, 0], [600, 450])
  window_dpi:       96.09458128078816
  window_open:      false
  mousebutton:      Makie.MouseButtonEvent(Makie.Mouse.none, Makie.Mouse.release)
  mousebuttonstate: Set{Makie.Mouse.Button}()
  mouseposition:    (0.0, 0.0)
  scroll:           (0.0, 0.0)
  keyboardbutton:   Makie.KeyEvent(Makie.Keyboard.unknown, Makie.Keyboard.release)
  keyboardstate:    Set{Makie.Keyboard.Button}()
  unicode_input:    \0
  dropped_files:    String[]
  hasfocus:         false
  entered_window:   false
```

We can use those events to e.g. move the subwindow. If you execute the below in GLMakie, you can move the sub-window around by pressing left mouse & ctrl:

```julia
on(scene.events.mouseposition) do mousepos
    if ispressed(subwindow, Mouse.left & Keyboard.left_control)
        subwindow.viewport[] = Rect(Int.(mousepos)..., 200, 200)
    end
end
```

## [Projections and Camera](https://docs.makie.org/stable/tutorials/scenes/#projections_and_camera)

We've already talked a bit about cameras, but not really how it works. Lets start from zero. By default, the scene x/y extends go from -1 to 1. So, to draw a rectangle outlining the scene window, the following rectangle does the job:

```julia
scene = Scene(backgroundcolor=:gray)
lines!(scene, Rect2f(-1, -1, 2, 2), linewidth=5, color=:black)
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_017ad1f3.png)

this is, because the projection matrix and view matrix are the identity matrix by default, and Makie's unit space is what's called `Clip space` in the OpenGL world

```julia
cam = Makie.camera(scene) # this is how to access the scenes camera
```

```
Camera:
  0 steering observables connected
  pixel_space: Float32[0.0033333334 0.0 0.0 -1.0; 0.0 0.0044444446 0.0 -1.0; 0.0 0.0 -0.0001 -0.0; 0.0 0.0 0.0 1.0]
  view: Float32[1.0 0.0 0.0 0.0; 0.0 1.0 0.0 0.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0]
  projection: Float32[1.0 0.0 0.0 0.0; 0.0 1.0 0.0 0.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0]
  projectionview: Float32[1.0 0.0 0.0 0.0; 0.0 1.0 0.0 0.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0]
  resolution: Float32[600.0, 450.0]
  lookat: Float32[0.0, 0.0, 0.0]
  eyeposition: Float32[1.0, 1.0, 1.0]
```

One can change the mapping, to e.g. draw from -3 to 5 with an orthographic projection matrix:

```julia
cam.projection[] = Makie.orthographicprojection(-3f0, 5f0, -3f0, 5f0, -100f0, 100f0)
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_f41e43ad.png)

one can also change the camera to a perspective 3d projection:

```julia
w, h = size(scene)
nearplane = 0.1f0
farplane = 100f0
aspect = Float32(w / h)
cam.projection[] = Makie.perspectiveprojection(45f0, aspect, nearplane, farplane)
# Now, we also need to change the view matrix
# to "put" the camera into some place.
eyeposition = Vec3f(10)
lookat = Vec3f(0)
upvector = Vec3f(0, 0, 1)
cam.view[] = Makie.lookat(eyeposition, lookat, upvector)
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_ec52546f.png)

## [Interaction with Axis & Layouts](https://docs.makie.org/stable/tutorials/scenes/#interaction_with_axis_layouts)

The Axis contains a scene, which has the projection set to make the coordinates go from `(x/y)limits_min ... (x/y)limits_max`. That's what we plot into. Besides that, it's a normal scene, which we can use to create subscenes with smaller window size or a different projection.

So, we can use `camrelative` and friends to e.g. plot in the middle of the axis:

```julia
figure, axis, plot_object = scatter(1:4)
relative_projection = Makie.camrelative(axis.scene);
scatter!(relative_projection, [Point2f(0.5)], color=:red)
# offset & text are in pixelspace
text!(relative_projection, "Hi", position=Point2f(0.5), offset=Vec2f(5))
lines!(relative_projection, Rect(0, 0, 1, 1), color=:blue, linewidth=3)
figure
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_9c4da820.png)

## [Transformations and Scene graph](https://docs.makie.org/stable/tutorials/scenes/#transformations_and_scene_graph)

So far we've been discussing only camera transformations of the scene. In contrast, there are also scene transformations, or commonly referred to as world transformations. To learn more about the different spaces, [learn opengl](https://learnopengl.com/Getting-started/Coordinate-Systems) offers some pretty nice explanations

The "world" transformation is implemented via the `Transformation` struct in Makie. Scenes and plots both contain these, so these types are considered as "Makie.Transformable". The transformation of a scene will get inherited by all plots added to the scene. An easy way to manipulate any `Transformable` is via these 3 functions:

[translate!](https://docs.makie.org/stable/tutorials/scenes/#translate!)

```
translate!(scene::Transformable, xyz::VecTypes)
translate!(scene::Transformable, xyz...)
```

Apply an absolute translation to the Scene, translating it to `x, y, z`.

```
translate!(Accum, scene::Transformable, xyz...)
```

Translate the scene relative to its current position.

[rotate!](https://docs.makie.org/stable/tutorials/scenes/#rotate!)

```
rotate!(Accum, scene::Transformable, axis_rot...)
```

Apply a relative rotation to the Scene, by multiplying by the current rotation.

```
rotate!(t::Transformable, axis_rot::Quaternion)
rotate!(t::Transformable, axis_rot::AbstractFloat)
rotate!(t::Transformable, axis_rot...)
```

Apply an absolute rotation to the Scene. Rotations are all internally converted to `Quaternion`s.

[scale!](https://docs.makie.org/stable/tutorials/scenes/#scale!)

```
scale!(t::Transformable, x, y)
scale!(t::Transformable, x, y, z)
scale!(t::Transformable, xyz)
scale!(t::Transformable, xyz...)
```

Scale the given `Transformable` (a Scene or Plot) to the given arguments. Can take `x, y` or `x, y, z`. This is an absolute scaling, and there is no option to perform relative scaling.

```julia
scene = Scene()
cam3d!(scene)
sphere_plot = mesh!(scene, Sphere(Point3f(0), 0.5), color=:red)
scale!(scene, 0.5, 0.5, 0.5)
rotate!(scene, Vec3f(1, 0, 0), 0.5) # 0.5 rad around the y axis
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_a5c5927e.png)

One can also transform the plot objects directly, which then adds the transformation from the plot object on top of the transformation from the scene. One can add subscenes and interact with those dynamically. Makie offers here what's usually referred to as a scene graph.

```julia
translate!(sphere_plot, Vec3f(0, 0, 1))
scene
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_76d8fa2b.png)

The scene graph can be used to create rigid transformations, like for a robot arm:

```julia
parent = Scene()
cam3d!(parent; clipping_mode = :static)

# One can set the camera lookat and eyeposition, by getting the camera controls and using `update_cam!`
camc = cameracontrols(parent)
update_cam!(parent, camc, Vec3f(0, 8, 0), Vec3f(4.0, 0, 0))
# One may need to adjust the
# near and far clip plane when adjusting the camera manually
camc.far[] = 100f0
s1 = Scene(parent, camera=parent.camera)
mesh!(s1, Rect3f(Vec3f(0, -0.1, -0.1), Vec3f(5, 0.2, 0.2)))
s2 = Scene(s1, camera=parent.camera)
mesh!(s2, Rect3f(Vec3f(0, -0.1, -0.1), Vec3f(5, 0.2, 0.2)), color=:red)
translate!(s2, 5, 0, 0)
s3 = Scene(s2, camera=parent.camera)
mesh!(s3, Rect3f(Vec3f(-0.2), Vec3f(0.4)), color=:blue)
translate!(s3, 5, 0, 0)
parent
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_5d162538.png)

```julia
# Now, rotate the "joints"
rotate!(s2, Vec3f(0, 1, 0), 0.5)
rotate!(s3, Vec3f(1, 0, 0), 0.5)
parent
```

![](https://docs.makie.org/stable/assets/tutorials/scenes/code/output/example_a0974cd1.png)

With this basic principle, we can even bring robots to life :) [Kevin Moerman](https://github.com/Kevin-Mattheus-Moerman) was so nice to supply a Lego mesh, which we're going to animate! When the scene graph is really just about a transformation graph, one can use the `Transformation` struct directly, which is what we're going to do here. This is more efficient and easier than creating a scene for each model.

```julia
using MeshIO, FileIO, GeometryBasics

colors = Dict(
    "eyes" => "#000",
    "belt" => "#000059",
    "arm" => "#009925",
    "leg" => "#3369E8",
    "torso" => "#D50F25",
    "head" => "yellow",
    "hand" => "yellow"
)

origins = Dict(
    "arm_right" => Point3f(0.1427, -6.2127, 5.7342),
    "arm_left" => Point3f(0.1427, 6.2127, 5.7342),
    "leg_right" => Point3f(0, -1, -8.2),
    "leg_left" => Point3f(0, 1, -8.2),
)

rotation_axes = Dict(
    "arm_right" => Vec3f(0.0000, -0.9828, 0.1848),
    "arm_left" => Vec3f(0.0000, 0.9828, 0.1848),
    "leg_right" => Vec3f(0, -1, 0),
    "leg_left" => Vec3f(0, 1, 0),
)

function plot_part!(scene, parent, name::String)
    # load the model file
    m = load(assetpath("lego_figure_" * name * ".stl"))
    # look up color
    color = colors[split(name, "_")[1]]
    # Create a child transformation from the parent
    child = Transformation(parent)
    # get the transformation of the parent
    ptrans = Makie.transformation(parent)
    # get the origin if available
    origin = get(origins, name, nothing)
    # center the mesh to its origin, if we have one
    if !isnothing(origin)
        centered = m.position .- origin
        m = GeometryBasics.Mesh(meta(centered; normals=m.normals), faces(m))
        translate!(child, origin)
    else
        # if we don't have an origin, we need to correct for the parents translation
        translate!(child, -ptrans.translation[])
    end
    # plot the part with transformation & color
    return mesh!(scene, m; color=color, transformation=child)
end

function plot_lego_figure(s, floor=true)
    # Plot hierarchical mesh and put all parts into a dictionary
    figure = Dict()
    figure["torso"] = plot_part!(s, s, "torso")
        figure["head"] = plot_part!(s, figure["torso"], "head")
            figure["eyes_mouth"] = plot_part!(s, figure["head"], "eyes_mouth")
        figure["arm_right"] = plot_part!(s, figure["torso"], "arm_right")
            figure["hand_right"] = plot_part!(s, figure["arm_right"], "hand_right")
        figure["arm_left"] = plot_part!(s, figure["torso"], "arm_left")
            figure["hand_left"] = plot_part!(s, figure["arm_left"], "hand_left")
        figure["belt"] = plot_part!(s, figure["torso"], "belt")
            figure["leg_right"] = plot_part!(s, figure["belt"], "leg_right")
            figure["leg_left"] = plot_part!(s, figure["belt"], "leg_left")

    # lift the little guy up
    translate!(figure["torso"], 0, 0, 20)
    # add some floor
    floor && mesh!(s, Rect3f(Vec3f(-400, -400, -2), Vec3f(800, 800, 2)), color=:white)
    return figure
end

# Finally, lets let him walk and record it as a video with the new, experimental ray tracing backend.

# Note: RPRMakie is still not very stable and rendering out the video is quite slow on CI, so the shown video is prerendered!

using RPRMakie
# iterate rendering 200 times, to get less noise and more light
RPRMakie.activate!(iterations=200)

radiance = 50000
# Note, that only RPRMakie supports `EnvironmentLight` so far
lights = [
    EnvironmentLight(1.5, rotl90(load(assetpath("sunflowers_1k.hdr"))')),
    PointLight(Vec3f(50, 0, 200), RGBf(radiance, radiance, radiance*1.1)),
]
s = Scene(size=(500, 500), lights=lights)
cam3d!(s)
c = cameracontrols(s)
c.near[] = 5
c.far[] = 1000
update_cam!(s, c, Vec3f(100, 30, 80), Vec3f(0, 0, -10))
figure = plot_lego_figure(s)

rot_joints_by = 0.25*pi
total_translation = 50
animation_strides = 10

a1 = LinRange(0, rot_joints_by, animation_strides)
angles = [a1; reverse(a1[1:end-1]); -a1[2:end]; reverse(-a1[1:end-1]);]
nsteps = length(angles); #Number of animation steps
translations = LinRange(0, total_translation, nsteps)

Makie.record(s, "lego_walk.mp4", zip(translations, angles)) do (translation, angle)
    #Rotate right arm+hand
    for name in ["arm_left", "arm_right",
                            "leg_left", "leg_right"]
        rotate!(figure[name], rotation_axes[name], angle)
    end
    translate!(figure["torso"], translation, 0, 20)
end
```