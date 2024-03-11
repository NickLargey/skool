a_x = 0.5
a_x_hat = 0.75

a_x_2 = 1327.5
a_x_hat_2 = 1328

a_err_rel = abs((a_x - a_x_hat) / a_x)
a2_err_rel = abs((a_x_2 - a_x_hat_2) / a_x_2)


println(a_err_rel)
println(a2_err_rel)

