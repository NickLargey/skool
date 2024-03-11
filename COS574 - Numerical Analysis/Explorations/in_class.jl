gcd(a,b) = (a:-1:1)[(a .% (a:-1:1) .== 0) .& (b .% (a:-1:1) .== 0)][1]
gcd(18, 24)

function m()
  k = rand(1:100, 10)
  return k[k .% 2 .==0]
end

code_native(m)

## SigDigs ##
round(100*pi, sigdigits=5, base=10)

# 1000(pi)(e) 
A = round(100*pi, sigdigits=5, base=10)
B = round(10 * exp(1), sigdigits=5)

answer = round(A * B, sigdigits=5)

