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

M = "data/can___24.mtx"

j_A = MatrixMarket.mmread(M)
A = j_A[1:size(j_A, 1), 1:size(j_A, 1)]

function input_matrix_viz() 
  f, ax, plt = spy(A, markersize = 4,colormap = :hawaii50, marker = :circle, framecolor = :lightgrey)
  hidedecorations!(ax)
  ax.title = "Vizualization of input Matrix $M"
  f

end

input_matrix_fig = with_theme(input_matrix_viz, theme_black())
save("matrix_$M.png", input_matrix_fig)



b = rand(size(A, 1))
# A = [4 1 -1;
    #  2 7 1;
    #  1 -3 12.0]
# 
# b = [19; 3; 31.0]

x0 = zeros(size(b))

history = jacobi_method(A, b, x0, 1e-6, 50)

history_matrix = hcat(history...)'

hsize = size(history_matrix,1)
viz_A = (Matrix(A) \ history[hsize])
x = size(A,1)
y = size(A,1)
z = viz_A
pts = Point3f.(x, y, z)
function plot_surface()
  cmap = :viridis
  fig = Figure(size = (1200, 800))
  ax = Axis3(fig[1, 1], perspectiveness = 0.5, elevation = π / 9,
    xzpanelcolor = (:black, 0.75), yzpanelcolor = (:black, 0.75),
    zgridcolor = :grey, ygridcolor = :grey, xgridcolor = :grey)
  sm = surface!(ax, 1:x,1:y,z)

  fig
end
surface_fig = plot_surface()


save("fidapm05_jacobi_series_convergence.png", series_fig)