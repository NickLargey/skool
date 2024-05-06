using LinearAlgebra
function iterativeRefinement(A, b, tol)
  x = A \ b 
  while true
      r = b - A * x
      if norm(r) / norm(b) < tol
          println("Converged")
          return x
      end
      e = A \ r
      x = x + e
  end
end

function cond_mat()|
  itr = 0
  while itr < 20
    e = .1
    while e > 0
      A = [1 1+e; 1-e 1]
      L, U = lu(A)      
      itr += 1
      e *= .1
    end
    print(itr)
  end
end  

cond_mat()