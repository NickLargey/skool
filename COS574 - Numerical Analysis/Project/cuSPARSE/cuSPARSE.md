### Readings & Blogs:
- [Exploiting NVIDIA Ampere Structured Sparsity with cuSPARSELt](https://developer.nvidia.com/blog/exploiting-ampere-structured-sparsity-with-cusparselt/)
- [Accelerating Matrix Multiplication with Block Sparse Format and NVIDIA Tensor Cores](https://developer.nvidia.com/blog/accelerating-matrix-multiplication-with-block-sparse-format-and-nvidia-tensor-cores/
- [Just-In-Time Link-Time Optimization Adoption in cuSPARSE/cuFFT: Use Case Overview](https://www.nvidia.com/en-us/on-demand/session/gtcfall21-a31155/?playlistId=playList-ead11304-9931-4e91-9d5a-fb0e1ef27014)
- [Making the Most of Structured Sparsity in the NVIDIA Ampere Architecture](https://www.nvidia.com/en-us/on-demand/session/gtcspring21-s31552/)

The library routines provide the following functionalities:

- Operations between a **sparse vector** and a **dense vector**: sum, dot product, scatter, gather
- Operations between a **dense matrix** and a **sparse vector**: multiplication
- Operations between a **sparse matrix** and a **dense vector**: multiplication, triangular solver, tridiagonal solver, pentadiagonal solver
- Operations between a **sparse matrix** and a **dense matrix**: multiplication, triangular solver, tridiagonal solver, pentadiagonal solver
- Operations between a **sparse matrix** and a **sparse matrix**: sum, multiplication
- Operations between **dense matrices** with output a **sparse matrix**: multiplication
- **Sparse matrix preconditioners**: Incomplete Cholesky Factorization (level 0), Incomplete LU Factorization (level 0)
- Reordering and Conversion operations between different **sparse matrix storage formats**