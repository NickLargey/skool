# 1.2.2
A = [2 -4; 3 -5; 7 0]
B = [-5 1 4; 4 6 8; 10 5 0]
C = [-8 0; 2 -3; -1 4]

D = A + 3 * B * C


# 1.2.5
X = rand(-1:1, 3, 2)

# 1.2.6
x = 0:0.1:1

# 1.2.13
x = rand(-10:10, 10)
c = [(x .>= -1) .& (x .<= 1)]

# 1.2.16
x = rand((1:10), 10)
function findmax(x)
  xmax = (1, x[1])
  for i = 2:10
    if x[i] > xmax[2]
      xmax = (i, x[i])
    end
  end
  println(xmax)
end

