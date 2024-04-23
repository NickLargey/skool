Q = [0.5 -0.5 0.5; 0.5 0.5 -0.5; 0.5 0.5 0.5; 0.5 -0.5 -0.5]
R = [2 3 2; 0 5 -2; 0 0 4]

A = Q * R

for j = 1:n
  Q[j] = A[j]
  for i = 1:j-1
    R[i, j] = Q[i] * A[j]
    Q[j] = Q[j] - R[i, j] * Q[i]
  end
  R[j, j] = len(Q[j])
  Q[j] = Q[j] / R[j, j]
end