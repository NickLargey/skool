using GLMakie
using MatrixMarket
using LinearAlgebra
using ColorSchemes

function jacobi_method(A, b, x0, tol, max_iters)
    x = x0
    n = length(b)
    history = [copy(x)]
    for iter in 1:max_iters
        x_new = zeros(n)
        for i in 1:n
            sum = b[i] - dot(A[i, :], x) + A[i, i] * x[i]
            x_new[i] = sum / A[i, i]
        end
        push!(history, copy(x_new))
        if norm(x_new - x, Inf) < tol
            break
        end
        x = x_new
    end
    return history
end

M = "data/fidapm05.mtx"

j_A = MatrixMarket.mmread(M)
A = j_A[1:size(j_A, 1), 1:size(j_A, 1)]

function input_matrix_viz() 
  f, ax, plt = spy(A, markersize = 4,colormap = :hawaii50, marker = :circle, framecolor = :lightgrey)
  hidedecorations!(ax)
  ax.title = "Vizualization of input Matrix $M"
  f

end

input_matrix_fig = with_theme(input_matrix_viz, theme_black())
save("$M_matrix.png", input_matrix_fig)



b = rand(size(A, 1))
# A = [4 1 -1;
#      2 7 1;
#      1 -3 12]

# b = [19; 3; 31]

x0 = zeros(size(b))

history = jacobi_method(A, b, x0, 1e-6, 50)

history_matrix = hcat(history...)'

hsize = size(history_matrix,1)


function plot_series()
  pts = Point2f.(hsize, history[hsize])
  fig = Figure(size=(1200, 800))
  ax = Axis(fig[1, 1], title = "Jacobi Iteration Convergence", xlabel = "Iteration", ylabel = "Values of x")
  series!(1:hsize, transpose(history_matrix), color=:hawaii50, linewidth=1, labels=["X$i" for i in 1:hsize])
  scatter!(pts, color=:white, markersize=10)
  text!(ax,["$i" for i in history[hsize]], color = :white, position = [pt + Point2f(-.5, .15) for pt in pts])
  fig
end
series_fig = with_theme(plot_series, theme_black())


save("fidapm05_jacobi_series_convergence.png", series_fig)