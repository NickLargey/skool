using CUDA
CUDA.versioninfo()

#### EXAMPLE ####
N = 2^20
x = fill(1.0f0, N)  # a vector filled with 1.0 (Float32)
y = fill(2.0f0, N)  # a vector filled with 2.0

y .+= x             # increment each element of y with the corresponding element of x

using Test
@test all(y .== 3.0f0)

function sequential_add!(y, x)
  for i in eachindex(y, x)
      @inbounds y[i] += x[i]
  end
  return nothing
end

fill!(y, 2)
sequential_add!(y, x)
@test all(y .== 3.0f0)

function parallel_add!(y, x)
  Threads.@threads for i in eachindex(y, x)
      @inbounds y[i] += x[i]
  end
  return nothing
end

fill!(y, 2)
parallel_add!(y, x)
@test all(y .== 3.0f0)

using BenchmarkTools
@btime sequential_add!($y, $x)
@btime parallel_add!($y, $x)

#### Your first GPU computation ####
using CUDA

x_d = CUDA.fill(1.0f0, N)  # a vector stored on the GPU filled with 1.0 (Float32)
y_d = CUDA.fill(2.0f0, N)  # a vector stored on the GPU filled with 2.0

y_d .+= x_d
@test all(Array(y_d) .== 3.0f0)

function add_broadcast!(y, x)
  CUDA.@sync y .+= x
  return
end

@btime add_broadcast!($y_d, $x_d)

#### Writing your first GPU kernel ####

function gpu_add1!(y, x)
  for i = 1:length(y)
      @inbounds y[i] += x[i]
  end
  return nothing
end

fill!(y_d, 2)
@cuda gpu_add1!(y_d, x_d)
@test all(Array(y_d) .== 3.0f0)

function bench_gpu1!(y, x)
  CUDA.@sync begin
      @cuda gpu_add1!(y, x)
  end
end

@btime bench_gpu1!($y_d, $x_d)

bench_gpu1!(y_d, x_d)  # run it once to force compilation
CUDA.@profile bench_gpu1!(y_d, x_d)

CUDA.@profile trace=true bench_gpu1!(y_d, x_d)

function gpu_add2!(y, x)
  index = threadIdx().x    # this example only requires linear indexing, so just use `x`
  stride = blockDim().x
  for i = index:stride:length(y)
      @inbounds y[i] += x[i]
  end
  return nothing
end

fill!(y_d, 2)
@cuda threads=256 gpu_add2!(y_d, x_d)
@test all(Array(y_d) .== 3.0f0)

function bench_gpu2!(y, x)
  CUDA.@sync begin
      @cuda threads=256 gpu_add2!(y, x)
  end
end

@btime bench_gpu2!($y_d, $x_d)

function gpu_add3!(y, x)
  index = (blockIdx().x - 1) * blockDim().x + threadIdx().x
  stride = gridDim().x * blockDim().x
  for i = index:stride:length(y)
      @inbounds y[i] += x[i]
  end
  return
end

numblocks = ceil(Int, N/256)

fill!(y_d, 2)
@cuda threads=256 blocks=numblocks gpu_add3!(y_d, x_d)
@test all(Array(y_d) .== 3.0f0)

function bench_gpu3!(y, x)
  numblocks = ceil(Int, length(y)/256)
  CUDA.@sync begin
      @cuda threads=256 blocks=numblocks gpu_add3!(y, x)
  end
end

@btime bench_gpu3!($y_d, $x_d)

CUDA.@profile trace=true bench_gpu3!(y_d, x_d)

kernel = @cuda launch=false gpu_add3!(y_d, x_d)
config = launch_configuration(kernel.fun)
threads = min(N, config.threads)
blocks = cld(N, threads)

fill!(y_d, 2)
kernel(y_d, x_d; threads, blocks)
@test all(Array(y_d) .== 3.0f0)

function bench_gpu4!(y, x)
  kernel = @cuda launch=false gpu_add3!(y, x)
  config = launch_configuration(kernel.fun)
  threads = min(length(y), config.threads)
  blocks = cld(length(y), threads)

  CUDA.@sync begin
      kernel(y, x; threads, blocks)
  end
end

@btime bench_gpu4!($y_d, $x_d)

function gpu_add2_print!(y, x)
  index = threadIdx().x    # this example only requires linear indexing, so just use `x`
  stride = blockDim().x
  @cuprintln("thread $index, block $stride")
  for i = index:stride:length(y)
      @inbounds y[i] += x[i]
  end
  return nothing
end

@cuda threads=16 gpu_add2_print!(y_d, x_d)
synchronize()

a = CuArray{Int}(undef, 1024)

# essential memory operations, like copying, filling, reshaping, ...
b = copy(a)
fill!(b, 0)
@test b == CUDA.zeros(Int, 1024)

# automatic memory management
a = nothing

a = CUDA.zeros(1024)
b = CUDA.ones(1024)
a.^2 .+ sin.(b)

a = CUDA.zeros(1024)

function kernel_2(a)
    i = threadIdx().x
    a[i] += 1
    return
end

@cuda threads=length(a) kernel_2(a)

CUDA.@elapsed begin
  # code that will be timed using CUDA events
end

# or

for device in CUDA.devices()
  @show capability(device)
end

version = Ref{Cint}()
CUDA.cuDriverGetVersion(version)
@show version[]