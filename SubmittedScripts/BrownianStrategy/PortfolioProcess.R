data = read.csv("~/SOA/Time Series Data.csv")

# create a black-scholes function to estimate future stock price
calcBS = function(S0, r, sigma, t){
 return(S0*exp((r - (sigma**2)/2)*t + sigma*rnorm(1,0,t)))
}

# create empty lists to store our values
port_values =  c(10000)
a1_list = numeric()
a2_list = numeric()

# create the for loop to run the algorithm at each time step
for (i in 1:(nrow(data)-1)){
  # setting our parameters
  S0 = data[i,3]
  C0 = data[i,2]
  r = log(1.0527)
  sigma1 = 0.027947
  sigma2 = 0.026567
  t = 1/252
  # create our objective function to maximize, which is just the epxected future value of our portfolio
  f = function(x){
    S0 = data[i,3]
    C0 = data[i,2]
    r = log(1.0527)
    sigma = 0.1
    t = 1/252
    return((port_values[length(port_values)] - x[1]*S0 - x[2]*C0)*exp(r*t) + x[1]*calcBS(S0, r, sigma1, t) + x[2]*calcBS(C0, r, sigma2, t))
  }
  # performing the optimization calculation
  result <- optim(par = c(0,0), fn = f, method = "L-BFGS-B")
  a1 = result$par[1]
  a2 = result$par[2]
  a1_list <- c(a1_list, a1)
  a2_list <- c(a2_list, a2)
  S1 = data[i+1,3]
  S2 = data[i+1,2]
  
  # calculate the actual portfolio values based on our algorithm's decisions
  port_val = (port_values[length(port_values)] - a1*S0 - a2*C0)*exp(r*t) + a1*S1 + a2*S2
  # adding the portfolio values to our list
  port_values <- c(port_values, port_val)
}

# plot the portfolio value vs time step
plot(port_values, xlab = "Time Step", ylab = "Portfolio Value", type = "l")
