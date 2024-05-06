using GLMakie
using MatrixMarket
using LinearAlgebra
# Define the Jacobi method function
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

# Define the matrix A and vector b
j_A = MatrixMarket.mmread("data/fidapm37.mtx")
A = j_A[1:size(j_A, 1), 1:size(j_A, 1)]

b = rand(size(A, 1))
x0 = zeros(size(b))

# Run the Jacobi method
history = jacobi_method(A, b, x0, 1e-5, 25)

# Convert history to a suitable format for plotting
history_matrix = hcat(history...)'

# Create a heatmap of the solution vector
fig = Figure()
ax = Axis(fig[1, 1], title = "Heatmap of Solution Vector", xlabel = "Component Index", ylabel = "Iteration Number")
heatmap!(ax, history_matrix, colormap = :viridis, colorrange = (minimum(history_matrix), maximum(history_matrix)))

fig