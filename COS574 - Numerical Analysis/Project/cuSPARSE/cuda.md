- must be installed in conda environment. currently in `coda activate CUDA`.

- [Compatible with Julia](https://cuda.juliagpu.org/stable/)

# Basics

We'll first demonstrate GPU computations at a high level using the `CuArray` type, without explicitly writing a kernel function:

```julia
using CUDA

x_d = CUDA.fill(1.0f0, N)  # a vector stored on the GPU filled with 1.0 (Float32)
y_d = CUDA.fill(2.0f0, N)  # a vector stored on the GPU filled with 2.0
```
Here the `d` means "device," in contrast with "host". Now let's do the increment:

```julia
y_d .+= x_d
@test all(Array(y_d) .== 3.0f0)
```

```
Test Passed
```

The statement `Array(y_d)` moves the data in `y_d` back to the host for testing. If we want to benchmark this, let's put it in a function:

```julia
function add_broadcast!(y, x)
    CUDA.@sync y .+= x
    return
end
```

```
add_broadcast! (generic function with 1 method)
```

```julia
@btime add_broadcast!($y_d, $x_d)
```

```
  67.047 μs (84 allocations: 2.66 KiB)
```

The most interesting part of this is the call to `CUDA.@sync`. The CPU can assign jobs to the GPU and then go do other stuff (such as assigning _more_ jobs to the GPU) while the GPU completes its tasks. Wrapping the execution in a `CUDA.@sync` block will make the CPU block until the queued GPU tasks are done, similar to how `Base.@sync` waits for distributed CPU tasks. Without such synchronization, you'd be measuring the time takes to launch the computation, not the time to perform the computation. But most of the time you don't need to synchronize explicitly: many operations, like copying memory from the GPU to the CPU, implicitly synchronize execution.

For this particular computer and GPU, you can see the GPU computation was significantly faster than the single-threaded CPU computation, and that the use of multiple CPU threads makes the CPU implementation competitive. Depending on your hardware you may get different results.

### Writing your first GPU kernel

Using the high-level GPU array functionality made it easy to perform this computation on the GPU. However, we didn't learn about what's going on under the hood, and that's the main goal of this tutorial. So let's implement the same functionality with a GPU kernel:

```julia
function gpu_add1!(y, x)
    for i = 1:length(y)
        @inbounds y[i] += x[i]
    end
    return nothing
end

fill!(y_d, 2)
@cuda gpu_add1!(y_d, x_d)
@test all(Array(y_d) .== 3.0f0)
```

```
Test Passed
```

Aside from using the `CuArray`s `x_d` and `y_d`, the only GPU-specific part of this is the _kernel launch_ via `@cuda`. The first time you issue this `@cuda` statement, it will compile the kernel (`gpu_add1!`) for execution on the GPU. Once compiled, future invocations are fast. You can see what `@cuda` expands to using `?@cuda` from the Julia prompt.

Let's benchmark this:

```julia
function bench_gpu1!(y, x)
    CUDA.@sync begin
        @cuda gpu_add1!(y, x)
    end
end
```

```
bench_gpu1! (generic function with 1 method)
```

```julia
@btime bench_gpu1!($y_d, $x_d)
```

```
  119.783 ms (47 allocations: 1.23 KiB)
```

That's a _lot_ slower than the version above based on broadcasting. What happened?

### Profiling

When you don't get the performance you expect, usually your first step should be to profile the code and see where it's spending its time:

```julia
bench_gpu1!(y_d, x_d)  # run it once to force compilation
CUDA.@profile bench_gpu1!(y_d, x_d)
```

```
Profiler ran for 51.45 ms, capturing 523 events.

Host-side activity: calling CUDA APIs took 42.37 ms (82.37% of the trace)
┌──────────┬───────────┬───────┬───────────┬───────────┬───────────┬────────────
│ Time (%) │      Time │ Calls │  Avg time │  Min time │  Max time │ Name      ⋯
├──────────┼───────────┼───────┼───────────┼───────────┼───────────┼────────────
│   82.36% │  42.37 ms │     1 │  42.37 ms │  42.37 ms │  42.37 ms │ cuStreamS ⋯
│    0.19% │   96.8 µs │     1 │   96.8 µs │   96.8 µs │   96.8 µs │ cuLaunchK ⋯
│    0.00% │   1.19 µs │     1 │   1.19 µs │   1.19 µs │   1.19 µs │ cuCtxSetC ⋯
│    0.00% │ 715.26 ns │     1 │ 715.26 ns │ 715.26 ns │ 715.26 ns │ cuCtxGetD ⋯
│    0.00% │ 238.42 ns │     1 │ 238.42 ns │ 238.42 ns │ 238.42 ns │ cuDeviceG ⋯
└──────────┴───────────┴───────┴───────────┴───────────┴───────────┴────────────
                                                                1 column omitted

Device-side activity: GPU was busy for 51.25 ms (99.61% of the trace)
┌──────────┬──────────┬───────┬──────────┬──────────┬──────────┬────────────────
│ Time (%) │     Time │ Calls │ Avg time │ Min time │ Max time │ Name          ⋯
├──────────┼──────────┼───────┼──────────┼──────────┼──────────┼────────────────
│   99.61% │ 51.25 ms │     1 │ 51.25 ms │ 51.25 ms │ 51.25 ms │ _Z9gpu_add1_1 ⋯
└──────────┴──────────┴───────┴──────────┴──────────┴──────────┴────────────────
                                                                1 column omitted
```

You can see that almost all of the time was spent in `ptxcall_gpu_add1__1`, the name of the kernel that CUDA.jl assigned when compiling `gpu_add1!` for these inputs. (Had you created arrays of multiple data types, e.g., `xu_d = CUDA.fill(0x01, N)`, you might have also seen `ptxcall_gpu_add1__2` and so on. Like the rest of Julia, you can define a single method and it will be specialized at compile time for the particular data types you're using.)

For further insight, run the profiling with the option `trace=true`

```julia
CUDA.@profile trace=true bench_gpu1!(y_d, x_d)
```

```
Profiler ran for 51.79 ms, capturing 523 events.

Host-side activity: calling CUDA APIs took 48.25 ms (93.17% of the trace)
┌─────┬──────────┬───────────┬────────┬─────────────────────┐
│  ID │    Start │      Time │ Thread │ Name                │
├─────┼──────────┼───────────┼────────┼─────────────────────┤
│   2 │ 74.15 µs │  47.92 µs │      1 │ cuLaunchKernel      │
│ 517 │   3.1 ms │   3.58 µs │      2 │ cuCtxSetCurrent     │
│ 518 │  3.11 ms │ 715.26 ns │      2 │ cuCtxGetDevice      │
│ 519 │  3.12 ms │ 238.42 ns │      2 │ cuDeviceGetCount    │
│ 521 │  3.13 ms │  48.25 ms │      2 │ cuStreamSynchronize │
└─────┴──────────┴───────────┴────────┴─────────────────────┘

Device-side activity: GPU was busy for 51.24 ms (98.95% of the trace)
┌────┬───────────┬──────────┬─────────┬────────┬──────┬─────────────────────────
│ ID │     Start │     Time │ Threads │ Blocks │ Regs │ Name                   ⋯
├────┼───────────┼──────────┼─────────┼────────┼──────┼─────────────────────────
│  2 │ 119.21 µs │ 51.24 ms │       1 │      1 │   16 │ _Z9gpu_add1_13CuDevice ⋯
└────┴───────────┴──────────┴─────────┴────────┴──────┴─────────────────────────
                                                                1 column omitted
```

The key thing to note here is that we are only using a single block with a single thread. These terms will be explained shortly, but for now, suffice it to say that this is an indication that this computation ran sequentially. Of note, sequential processing with GPUs is much slower than with CPUs; where GPUs shine is with large-scale parallelism.

### Writing a parallel GPU kernel

To speed up the kernel, we want to parallelize it, which means assigning different tasks to different threads. To facilitate the assignment of work, each CUDA thread gets access to variables that indicate its own unique identity, much as [`Threads.threadid()`](https://docs.julialang.org/en/latest/manual/parallel-computing/#Multi-Threading-(Experimental)-1) does for CPU threads. The CUDA analogs of `threadid` and `nthreads` are called `threadIdx` and `blockDim`, respectively; one difference is that these return a 3-dimensional structure with fields `x`, `y`, and `z` to simplify cartesian indexing for up to 3-dimensional arrays. Consequently we can assign unique work in the following way:

```julia
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
```

```
Test Passed
```

Note the `threads=256` here, which divides the work among 256 threads numbered in a linear pattern. (For a two-dimensional array, we might have used `threads=(16, 16)` and then both `x` and `y` would be relevant.)

Now let's try benchmarking it:

```julia
function bench_gpu2!(y, x)
    CUDA.@sync begin
        @cuda threads=256 gpu_add2!(y, x)
    end
end
```

```
bench_gpu2! (generic function with 1 method)
```

```julia
@btime bench_gpu2!($y_d, $x_d)
```

```
  1.873 ms (47 allocations: 1.23 KiB)
```

Much better!

But obviously we still have a ways to go to match the initial broadcasting result. To do even better, we need to parallelize more. GPUs have a limited number of threads they can run on a single _streaming multiprocessor_ (SM), but they also have multiple SMs. To take advantage of them all, we need to run a kernel with multiple _blocks_. We'll divide up the work like this:

![block grid](https://cuda.juliagpu.org/stable/tutorials/intro1.png)

This diagram was [borrowed from a description of the C/C++ library](https://devblogs.nvidia.com/even-easier-introduction-cuda/); in Julia, threads and blocks begin numbering with 1 instead of 0. In this diagram, the 4096 blocks of 256 threads (making 1048576 = 2^20 threads) ensures that each thread increments just a single entry; however, to ensure that arrays of arbitrary size can be handled, let's still use a loop:

```julia
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
```

```
Test Passed
```

The benchmark:

```julia
function bench_gpu3!(y, x)
    numblocks = ceil(Int, length(y)/256)
    CUDA.@sync begin
        @cuda threads=256 blocks=numblocks gpu_add3!(y, x)
    end
end
```

```
bench_gpu3! (generic function with 1 method)
```

```julia
@btime bench_gpu3!($y_d, $x_d)
```

```
  67.268 μs (52 allocations: 1.31 KiB)
```

Finally, we've achieved the similar performance to what we got with the broadcasted version. Let's profile again to confirm this launch configuration:

```julia
CUDA.@profile trace=true bench_gpu3!(y_d, x_d)
```

```
Profiler ran for 22.2 ms, capturing 68 events.

Host-side activity: calling CUDA APIs took 76.06 µs (0.34% of the trace)
┌────┬──────────┬─────────┬─────────────────────┐
│ ID │    Start │    Time │ Name                │
├────┼──────────┼─────────┼─────────────────────┤
│  2 │ 22.09 ms │ 48.4 µs │ cuLaunchKernel      │
│ 66 │ 22.17 ms │ 5.96 µs │ cuStreamSynchronize │
└────┴──────────┴─────────┴─────────────────────┘

Device-side activity: GPU was busy for 30.52 µs (0.14% of the trace)
┌────┬──────────┬──────────┬─────────┬────────┬──────┬──────────────────────────
│ ID │    Start │     Time │ Threads │ Blocks │ Regs │ Name                    ⋯
├────┼──────────┼──────────┼─────────┼────────┼──────┼──────────────────────────
│  2 │ 22.14 ms │ 30.52 µs │     256 │   4096 │   34 │ _Z9gpu_add3_13CuDeviceA ⋯
└────┴──────────┴──────────┴─────────┴────────┴──────┴──────────────────────────
                                                                1 column omitted
```

In the previous example, the number of threads was hard-coded to 256. This is not ideal, as using more threads generally improves performance, but the maximum number of allowed threads to launch depends on your GPU as well as on the kernel. To automatically select an appropriate number of threads, it is recommended to use the launch configuration API. This API takes a compiled (but not launched) kernel, returns a tuple with an upper bound on the number of threads, and the minimum number of blocks that are required to fully saturate the GPU:

```julia
kernel = @cuda launch=false gpu_add3!(y_d, x_d)
config = launch_configuration(kernel.fun)
threads = min(N, config.threads)
blocks = cld(N, threads)
```

```
1024
```

The compiled kernel is callable, and we can pass the computed launch configuration as keyword arguments:

```julia
fill!(y_d, 2)
kernel(y_d, x_d; threads, blocks)
@test all(Array(y_d) .== 3.0f0)
```

```
Test Passed
```

Now let's benchmark this:

```julia
function bench_gpu4!(y, x)
    kernel = @cuda launch=false gpu_add3!(y, x)
    config = launch_configuration(kernel.fun)
    threads = min(length(y), config.threads)
    blocks = cld(length(y), threads)

    CUDA.@sync begin
        kernel(y, x; threads, blocks)
    end
end
```

```
bench_gpu4! (generic function with 1 method)
```

```julia
@btime bench_gpu4!($y_d, $x_d)
```

```
  70.826 μs (99 allocations: 3.44 KiB)
```

A comparable performance; slightly slower due to the use of the occupancy API, but that will not matter with more complex kernels.

### Printing
When debugging, it's not uncommon to want to print some values. This is achieved with `@cuprint`:

```julia
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
```

```
thread 1, block 16
thread 2, block 16
thread 3, block 16
thread 4, block 16
thread 5, block 16
thread 6, block 16
thread 7, block 16
thread 8, block 16
thread 9, block 16
thread 10, block 16
thread 11, block 16
thread 12, block 16
thread 13, block 16
thread 14, block 16
thread 15, block 16
thread 16, block 16
```

Note that the printed output is only generated when synchronizing the entire GPU with `synchronize()`. This is similar to `CUDA.@sync`, and is the counterpart of `cudaDeviceSynchronize` in CUDA C++.

### Error-handling

The final topic of this intro concerns the handling of errors. Note that the kernels above used `@inbounds`, but did not check whether `y` and `x` have the same length. If your kernel does not respect these bounds, you will run into nasty errors:

```
ERROR: CUDA error: an illegal memory access was encountered (code #700, ERROR_ILLEGAL_ADDRESS)
Stacktrace:
 [1] ...
```

If you remove the `@inbounds` annotation, instead you get

```
ERROR: a exception was thrown during kernel execution.
       Run Julia on debug level 2 for device stack traces.
```

As the error message mentions, a higher level of debug information will result in a more detailed report. Let's run the same code with with `-g2`:

```
ERROR: a exception was thrown during kernel execution.
Stacktrace:
 [1] throw_boundserror at abstractarray.jl:484
 [2] checkbounds at abstractarray.jl:449
 [3] setindex! at /home/tbesard/Julia/CUDA/src/device/array.jl:79
 [4] some_kernel at /tmp/tmpIMYANH:6
```

Warning

On older GPUs (with a compute capability below `sm_70`) these errors are fatal, and effectively kill the CUDA environment. On such GPUs, it's often a good idea to perform your "sanity checks" using code that runs on the CPU and only turn over the computation to the GPU once you've deemed it to be safe.

## Summary
Keep in mind that the high-level functionality of CUDA often means that you don't need to worry about writing kernels at such a low level. However, there are many cases where computations can be optimized using clever low-level manipulations. Hopefully, you now feel comfortable taking the plunge.

# Using custom structs
This tutorial shows how to use custom structs on the GPU. Our example will be a one dimensional interpolation. Lets start with the CPU version:

```julia
using CUDA

struct Interpolate{A}
    xs::A
    ys::A
end

function (itp::Interpolate)(x)
    i = searchsortedfirst(itp.xs, x)
    i = clamp(i, firstindex(itp.ys), lastindex(itp.ys))
    @inbounds itp.ys[i]
end

xs_cpu = [1.0, 2.0, 3.0]
ys_cpu = [10.0,20.0,30.0]
itp_cpu = Interpolate(xs_cpu, ys_cpu)
pts_cpu = [1.1,2.3]
result_cpu = itp_cpu.(pts_cpu)
```

```
2-element Vector{Float64}:
 20.0
 30.0
```

Ok the CPU code works, let's move our data to the GPU:

```julia
itp = Interpolate(CuArray(xs_cpu), CuArray(ys_cpu))
pts = CuArray(pts_cpu);
```

If we try to call our interpolate `itp.(pts)`, we get an error however:

```
...
KernelError: passing and using non-bitstype argument
...
```

Why does it throw an error? Our calculation involves a custom type `Interpolate{CuArray{Float64, 1}}`. At the end of the day all arguments of a CUDA kernel need to be bitstypes. However we have

```julia
isbitstype(typeof(itp))
```

```
false
```

How to fix this? The answer is, that there is a conversion mechanism, which adapts objects into CUDA compatible bitstypes. It is based on the [Adapt.jl](https://github.com/JuliaGPU/Adapt.jl) package and basic types like `CuArray` already participate in this mechanism. For custom types, we just need to add a conversion rule like so:

```julia
import Adapt
function Adapt.adapt_structure(to, itp::Interpolate)
    xs = Adapt.adapt_structure(to, itp.xs)
    ys = Adapt.adapt_structure(to, itp.ys)
    Interpolate(xs, ys)
end
```

Now our struct plays nicely with CUDA.jl:

```julia
result = itp.(pts)
```

```
2-element CuArray{Float64, 1, CUDA.Mem.DeviceBuffer}:
 20.0
 30.0
```

It works, we get the same result as on the CPU.

```julia
@assert CuArray(result_cpu) == result
```

Alternatively instead of defining `Adapt.adapt_structure` explictly, we could have done

```julia
Adapt.@adapt_structure Interpolate
```

which expands to the same code that we wrote manually.
# Troubleshooting

## UndefVarError: libcuda not defined

This means that CUDA.jl could not find a suitable CUDA driver. For more information, re-run with the `JULIA_DEBUG` environment variable set to `CUDA_Driver_jll`.

## UNKNOWN_ERROR(999)

If you encounter this error, there are several known issues that may be causing it:

- a mismatch between the CUDA driver and driver library: on Linux, look for clues in `dmesg`
- the CUDA driver is in a bad state: this can happen after resume. **Try rebooting**.

Generally though, it's impossible to say what's the reason for the error, but Julia is likely not to blame. Make sure your set-up works (e.g., try executing `nvidia-smi`, a CUDA C binary, etc), and if everything looks good file an issue.

# Overview
The CUDA.jl package provides three distinct, but related, interfaces for CUDA programming:

- the `CuArray` type: for programming with arrays;
- native kernel programming capabilities: for writing CUDA kernels in Julia;
- CUDA API wrappers: for low-level interactions with the CUDA libraries.

Much of the Julia CUDA programming stack can be used by just relying on the `CuArray` type, and using platform-agnostic programming patterns like `broadcast` and other array abstractions. Only once you hit a performance bottleneck, or some missing functionality, you might need to write a custom kernel or use the underlying CUDA APIs.

## The `CuArray` type

The `CuArray` type is an essential part of the tool chain. Primarily, it is used to manage GPU memory, and copy data from and back to the CPU:

```julia
a = CuArray{Int}(undef, 1024)

# essential memory operations, like copying, filling, reshaping, ...
b = copy(a)
fill!(b, 0)
@test b == CUDA.zeros(Int, 1024)

# automatic memory management
a = nothing
```

Beyond memory management, there are a whole range of array operations to process your data. This includes several higher-order operations that take other code as arguments, such as `map`, `reduce` or `broadcast`. With these, it is possible to perform kernel-like operations without actually writing your own GPU kernels:

```julia
a = CUDA.zeros(1024)
b = CUDA.ones(1024)
a.^2 .+ sin.(b)
```

When possible, these operations integrate with existing vendor libraries such as CUBLAS and CURAND. For example, multiplying matrices or generating random numbers will automatically dispatch to these high-quality libraries, if types are supported, and fall back to generic implementations otherwise.

For more details, refer to the section on [Array programming](https://cuda.juliagpu.org/stable/usage/array/#Array-programming).

## Kernel programming with `@cuda`

If an operation cannot be expressed with existing functionality for `CuArray`, or you need to squeeze every last drop of performance out of your GPU, you can always write a custom kernel. Kernels are functions that are executed in a massively parallel fashion, and are launched by using the `@cuda` macro:

```julia
a = CUDA.zeros(1024)

function kernel(a)
    i = threadIdx().x
    a[i] += 1
    return
end

@cuda threads=length(a) kernel(a)
```

These kernels give you all the flexibility and performance a GPU has to offer, within a familiar language. However, not all of Julia is supported: you (generally) cannot allocate memory, I/O is disallowed, and badly-typed code will not compile. As a general rule of thumb, keep kernels simple, and only incrementally port code while continuously verifying that it still compiles and executes as expected.

For more details, refer to the section on [Kernel programming](https://cuda.juliagpu.org/stable/development/kernel/#Kernel-programming).

## CUDA API wrappers
For advanced use of the CUDA, you can use the driver API wrappers in CUDA.jl. Common operations include synchronizing the GPU, inspecting its properties, using events, etc. These operations are low-level, but for your convenience wrapped using high-level constructs. For example:

```julia
CUDA.@elapsed begin
    # code that will be timed using CUDA events
end

# or

for device in CUDA.devices()
    @show capability(device)
end
```

If such high-level wrappers are missing, you can always access the underling C API (functions and structures prefixed with `cu`) without having to ever exit Julia:

```julia
version = Ref{Cint}()
CUDA.cuDriverGetVersion(version)
@show version[]
```