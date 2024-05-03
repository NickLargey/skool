using GLMakie

function jacobi_iteration!(x, A, b)
    n = length(b)
    new_x = copy(x)  # Create a copy to store new values
    for i in 1:n
        sum = b[i]
        for j in 1:n
            if i != j
                sum -= A[i, j] * x[j]
            end
        end
        new_x[i] = sum / A[i, i]
    end
    x .= new_x  # Update x with new values
end

function animate_jacobi(A, b, x0, num_iterations)
    fig = Figure(resolution = (1200, 600))
    ax = Axis3(fig[1, 1], title = "Jacobi Iteration with A and x0")

    # Create a grid for each element in A, scale by index to avoid overlap
    x_indices = repeat(1:size(A, 2), 1, size(A, 1))  # Repeat each column index
    y_indices = repeat(1:size(A, 1), size(A, 2), 1)  # Repeat each row index flat
    A_flat = vec(A)  # Flatten A to use in z-values initialization
    
    # Initialize z-values with the same shape as A, but use x0 values for height
    z_values = Observable(Matrix{Float32}(undef, size(A)...))
    z_values[][1:size(x0, 1), 1] .= x0  # Initialize first column with x0, assume x0 fits within the rows

    # Initial plot with the first iteration, create a surface for each column of A corresponding to x0 values
    surface_plot = surface!(ax, x_indices, y_indices, z_values, colormap = :viridis)
    cbar = Colorbar(fig[1, 2], label = "Value of x")

    record(fig, "jacobi_surface_animation.mp4", 1:num_iterations; framerate = 2) do i
        jacobi_iteration!(x0, A, b)
        z_values[][1:size(x0, 1), :] .= repeat(x0, 1, size(A, 2))  # Update z-values to reflect x0 over all columns
        notify(z_values)  # Notify the update
        
        ax.title = "Iteration $i"
    end
    return fig
end

# Example usage
A = [4.0 -1.0 0.0; -1.0 4.0 -1.0; 0.0 -1.0 3.0]
b = [1.0, 2.0, 2.0]
x0 = zeros(3)  # Initial guess
animate_jacobi(A, b, x0, 25)
