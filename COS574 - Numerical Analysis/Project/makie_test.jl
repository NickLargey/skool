using GLMakie

f = Figure(backgroundcolor = :tomato, size = (800, 300))
ax = Axis(f[1,1],
          title = "Tomato Axies",
          xlabel = "X Axis",
          ylabel = "Y Axis"
)

x = range(0,10, length=100)
y = sin.(x)
lines!(ax, x, y)
y1 = cos.(x)
scatter!(ax,x,y1)