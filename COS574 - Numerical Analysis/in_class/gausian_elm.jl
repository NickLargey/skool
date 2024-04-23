# Pg. 86 Algorithm 3.1.6
using Random
A = rand(-10.0:10.0, 5, 5)
b = rand(-10.0:10.0, 5)

function gaussian_elim(A, b)
  n = size(A, 1)
  M = [A b]
  for j = 1:n-1
    pivot = argmax(abs.(M[j:end, j])) + j - 1
    M[[j, pivot], :] = M[[pivot, j], :]
    for i = j+1:n
      factor = M[i, j] / M[j, j]
      M[i, :] -= factor * M[j, :]
    end
  end
  x = zeros(n)
  for i = n:-1:1
    x[i] = (M[i, end] - M[i, i+1:n]' * x[i+1:n]) / M[i, i]
  end
  return M[:,1:end-1],A,x
end


M, A, x = gaussian_elim(A, b)

display(M)
display(A)
display(x)