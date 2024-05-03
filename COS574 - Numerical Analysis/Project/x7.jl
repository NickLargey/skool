using LinearAlgebra
using MatrixMarket
using Random

# 5.1.2
function Jacobi(A, b, tol)
  j_t = time()
  iter = 0
  x = zeros(size(b,1))
  n = size(A,1)
  x_new = zeros(size(b,1))
  t = tol
  while n > t && iter < 50 
    t = tol*norm(x, Inf)
    x_new .= Diagonal(A)\(-(tril(A,-1)+triu(A,1))*x + b)
    n = norm(x_new - x, Inf)
    x .= x_new
    iter += 1
  end
  J_elap = time()-j_t
  return x, iter, J_elap
end


# 5.1.4
A = [4 1 -1;
     2 7 1;
     1 -3 12]

b = [19; 3; 31]

jacobi_x, jacobi_iter, j_time = Jacobi(A, b, 1e-6)
display(jacobi_x)
display(jacobi_iter)


# 5.1.6
function GaussSeidel(A, b, tol)
  gst = time()
  iter = 0
  x = zeros(size(b,1))
  n = size(A,1)
  x_new = zeros(size(b,1))
  t = tol

  while n > t && iter < 50 
    t = tol*norm(x, Inf)
    x_new .= (Diagonal(A) +tril(A,-1))\(-triu(A,1)*x + b)
    n = norm(x_new - x, Inf)
    x .= x_new
    iter += 1
  end
  gs_elap = time()-gst
  return x, iter, gs_elap
end

GS_x, GS_iter, gs_time = GaussSeidel(A, b, 1e-6)
display(GS_x) 
display(GS_iter)
println("Jacobi time: ", j_time, " Gauss-Seidel time: ", gs_time)
"""
The tic() and toc() methods have been depreciated in Julia. It is now suggested to use the time() function.
When I ran it on both the Jacobi and Gauss-Seidel functions, Gauss-Seidel performed about 10x faster. 
"""

# 5.1.9
function SOR(A, b, w, tol)
  SORt = time()
  iter = 0
  x = zeros(size(b,1))
  n = size(A,1)
  x_new = zeros(size(b,1))
  t = tol

  while n > t && iter < 50 
    t = tol*norm(x, Inf)
    x_new .= (Diagonal(A) + (w*tril(A,-1))) \ (((1-w)*Diagonal(A)-(w*triu(A,1)))*x + (w*b))
    n = norm(x_new - x, Inf)
    x .= x_new
    iter += 1
  end
  SOR_elap = time()-SORt
  return x, iter, SOR_elap
end

SOR_x, SOR_iter, SOR_t = SOR(A, b, .5, 1e-6)

display(SOR_x)
display(SOR_iter)
println(SOR_t)

"""
time() for SOR seems to be having trouble displaying acurate measurements, but the most likely I saw
was about another 10x speed up from Gauss-Seidel. 
"""

# 5.2.4 # Doesn't work....
function steepestdescent(A, b, x0, tol)
  iter = 0
  r = size(A,1) 
  t = tol*norm(r, Inf)
  n = size(A,1)
  x = x0
  alpha = size(A,1)
  while n > t && iter < 50 
    t = tol*norm(r, Inf)
    r .= b - (A*x)
    alpha .= (r.*transpose(r))\((A*r).*transpose(r))   
    x_new .= x + alpha*r
    n = norm(x - r, Inf)
    x .= x_new
    iter += 1
  end
  return x, iter

end

SD_x, SD_iter = steepestdescent(A, b, b, 1e-6)
display(SD_x, SD_iter)



M = MatrixMarket.mmread("can___24.mtx")
b = rand(-10.0:10.0, size(M,1))
jacobi_x, jacobi_iter, j_time = Jacobi(M, b, 1e-6)
GS_x, GS_iter, gs_time = GaussSeidel(M, b, 1e-6)
SOR_x, SOR_iter, SOR_t = SOR(M, b, .5, 1e-6)

println("Jacobi x: ", jacobi_x, "\nGS x: ", GS_x, "\nSOR x: ", SOR_x)
println("Jacobi iterations: ", jacobi_iter, "\nGS iterations: ", GS_iter, "\nSOR x: ", SOR_iter)
println("Jacobi time: ", j_time, "\nGS time: ", gs_time, "\nSOR time: ", SOR_t)