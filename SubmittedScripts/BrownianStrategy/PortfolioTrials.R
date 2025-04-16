# load the dataset
data = read.csv("~/SOA/Time Series Data.csv")

# create a black-scholes function to estimate future stock price
calcBS = function(S0, r, sigma, t){
  return(S0*exp((r - (sigma**2)/2)*t + sigma*rnorm(1,0,t)))
}

# create an empty list to store the values from the trials
trials = numeric()

# define our moving average recursively, starting at 0
S = 0

# this for loop runs through each trial
for (j in 1:1000){
  # creating empty lists
  port_values =  c(10000)
  a1_list = numeric()
  a2_list = numeric()
  # this for loop runs the algorithm on all of the past dates
  for (i in 1:(nrow(data)-1)){
    # setting parameters
    S0 = data[i,3]
    C0 = data[i,2]
    r = log(1.0527)
    sigma1 = 0.027947
    sigma2 = 0.026567
    t = 1/252
    # defining the objective function to maximize, which is our expected future portfolio value equation
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
    
    # calculate the actual portfolio value based on our algorithm's decision
    port_val = (port_values[length(port_values)] - a1*S0 - a2*C0)*exp(r*t) + a1*S1 + a2*S2
    # store the portfolio values in the list
    port_values <- c(port_values, port_val)
  }
  trial = port_values[length(port_values)-1]
  # update our moving average
  S = S + trial
  trials <- c(trials, S/j)
}

# calculate our final estimate, which is the average across all trials
final_value_estimate = trials[length(trials)] 

# plot the moving average vs trial number
plot(trials, xlab = "Trial Number", ylab = "Portfolio Value Estimate", type = "l")
