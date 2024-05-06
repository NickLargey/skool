using BenchmarkTools
using LinearAlgebra
using MatrixMarket
using GLMakie
using CUDA

A = [4 1 -1;
  2 7 1;
  1 -3 12.0]

b = [19; 3; 31.0]

j_A = MatrixMarket.mmread("data/add32.mtx")
A = j_A[1:size(j_A, 1), 1:size(j_A, 1)]

b = rand(size(A, 1))
cuda_A = CuArray(M[1:size(M, 1), 1:size(M, 1)])
cuda_b = CuArray(rand(-10.0:10.0, size(cuda_A, 1)))


function jacobi(A, b, tol)
  iter = 0
  x = zeros(size(b, 1))
  n = size(A, 1)
  x_new = zeros(size(b, 1))
  t = tol
  while n > t
    t = tol * norm(x, Inf)
    x_new .= Diagonal(A) \ (-(tril(A, -1) + triu(A, 1)) * x + b)
    n = norm(x_new - x, Inf)
    x .= x_new
    iter += 1
  end
  return x, iter
end

Base.@kwdef mutable struct Jacobi
  tol::Float64 = 6e-5
  t::Float64
  A::Matrix{Float64}
  b::Vector{Float64}
  n::Vector{Float64}
  x::Vector{Float64}
  y::Matrix{Float64}
  z::Float16 = 0.0
end

function step!(j::Jacobi)
  j.t = j.tol * norm(j.x, Inf)
  dx .= Diagonal(j.A) \ (-(tril(j.A, -1) + triu(j.A, 1)) * j.x + j.b)
  j.n = norm(dx - j.x, Inf)
  j.x .= dx
  j.z += 1.0
  j.y += j.dt * dy
  j.z += j.dt * dz
  Point3f([j.x], [j.y], j.z)
end


function anim_jacobi(A, b)
  xs = []
  ys = []
  zs = []

  tol = 6e-5
  iter = 0
  x = zeros(size(b, 1))
  n = size(A, 1)
  x_new = zeros(size(b, 1))
  t = tol
  while n > t
    push!(xs, A * n)
    push!(ys, A * x)
    push!(zs, fill(size(A, 1), iter))


  end

  return xs, ys, zs
end


function build_animation(xs, ys, zs)

  fig = surface(xs, ys, zs,
    colormap=:darkterrain,
    colorrange=(80, 190),
    axis=(type=Axis3, azimuth=pi / 4))

  record(fig, "jacobi.mp4", 1:120) do frame
    notify(xs)
    notify(ys)
    notify(zs)
  end
end



x, y, z = anim_jacobi(A, b)
build_animation(x, y, z)








attractor = Lorenz()

points = Observable(Point3f[]) # Signal that can be used to update plots efficiently
colors = Observable(Int[])

set_theme!(theme_black())

fig, ax, l = lines(points, color=colors,
  colormap=:inferno, transparency=true,
  axis=(; type=Axis3, protrusions=(0, 0, 0, 0),
    viewmode=:fit, limits=(-30, 30, -30, 30, 0, 50)))

record(fig, "lorenz.mp4", 1:120) do frame
  for i in 1:50
    # update arrays inplace
    push!(points[], step!(attractor))
    push!(colors[], frame)
  end
  ax.azimuth[] = 1.7pi + 0.3 * sin(2pi * frame / 120) # set the view angle of the axis
  notify(points)
  notify(colors) # tell points and colors that their value has been updated
  l.colorrange = (0, frame) # update plot attribute directly
end







function parallel_jacobi!(A, b, tol)
  CUDA.@sync begin
    iter = 0
    x = zeros(size(b, 1))
    n = size(A, 1)
    x_new = zeros(size(b, 1))
    t = tol

    while n > t
      t = tol * norm(x, Inf)
      x_new .= Diagonal(A) \ (-(tril(A, -1) + triu(A, 1)) * x + b)
      n = norm(x_new - x, Inf)
      x .= x_new
      iter += 1
    end
  end
  # println(x)
  # println(iter)
  return
end

@btime parallel_jacobi!(A, b, 6e-5)

cuda_A = nothing
A = nothing
cuda_b = nothing
b = nothing



