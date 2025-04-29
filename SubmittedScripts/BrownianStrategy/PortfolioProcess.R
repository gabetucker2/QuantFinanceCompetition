# load the dataset
data <- read.csv("../../TrainingData/ManualCSVs/BrownianData.csv")

# create a Black-Scholes function to estimate future stock price
calcBS <- function(S0, r, sigma, t) {
  return(S0 * exp((r - (sigma^2) / 2) * t + sigma * rnorm(1, 0, t)))
}

# initialize portfolio value
port_values <- c(10000)
a1_list <- numeric()
a2_list <- numeric()

# run the algorithm at each time step
for (i in 1:(nrow(data) - 1)) {
  # set parameters
  S0 <- data$Close.x[i]  # Asset 1
  C0 <- data$Close.y[i]  # Asset 2
  r <- log(1.0527)
  sigma1 <- 0.027947
  sigma2 <- 0.026567
  t <- 1/252
  
  # define objective function to maximize: expected future portfolio value
  f <- function(x) {
    return((port_values[length(port_values)] - x[1]*S0 - x[2]*C0) * exp(r*t) +
             x[1]*calcBS(S0, r, sigma1, t) +
             x[2]*calcBS(C0, r, sigma2, t))
  }
  
  # optimization
  result <- optim(par = c(0, 0), fn = f, method = "L-BFGS-B")
  a1 <- result$par[1]
  a2 <- result$par[2]
  
  # scale allocations to achieve 2x leverage
  exposure_now <- abs(a1 * S0) + abs(a2 * C0)
  desired_exposure <- 2 * port_values[length(port_values)]  # 2x leverage
  scaling_factor <- desired_exposure / exposure_now
  
  a1 <- a1 * scaling_factor
  a2 <- a2 * scaling_factor
  
  a1_list <- c(a1_list, a1)
  a2_list <- c(a2_list, a2)
  
  # update real portfolio value
  S1 <- data$Close.x[i + 1]
  S2 <- data$Close.y[i + 1]
  
  next_port_val <- (port_values[length(port_values)] - a1*S0 - a2*C0) * exp(r*t) +
    a1*S1 + a2*S2
  port_values <- c(port_values, next_port_val)
}

# plot the portfolio value over time
plot(port_values, xlab = "Time Step", ylab = "Portfolio Value", type = "l")
