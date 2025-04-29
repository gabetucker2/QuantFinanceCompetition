# load the dataset
data <- read.csv("../../TrainingData/ManualCSVs/BrownianData.csv")

# create a Black-Scholes function to estimate future stock price
calcBS <- function(S0, r, sigma, t) {
  return(S0 * exp((r - (sigma^2) / 2) * t + sigma * rnorm(1, 0, t)))
}

# create a vector to store final portfolio values from each trial
final_portfolio_values <- numeric()

# run 1000 Monte Carlo trials
for (j in 1:1000) {
  # initialize portfolio value
  port_values <- c(10000)
  
  # loop through each date
  for (i in 1:(nrow(data) - 1)) {
    # parameters
    S0 <- data$Close.x[i]  # Asset 1
    C0 <- data$Close.y[i]  # Asset 2
    r <- log(1.0527)
    sigma1 <- 0.027947
    sigma2 <- 0.026567
    t <- 1/252
    
    # define objective: maximize expected future portfolio value
    f <- function(x) {
      cash_after_purchase <- port_values[length(port_values)] - x[1]*S0 - x[2]*C0
      
      # if cash is NaN or Inf or absurd, penalize heavily
      if (!is.finite(cash_after_purchase)) return(Inf)
      
      expected_value <- cash_after_purchase * exp(r*t) +
        x[1]*calcBS(S0, r, sigma1, t) +
        x[2]*calcBS(C0, r, sigma2, t)
      
      if (!is.finite(expected_value)) return(Inf)
      
      return(-expected_value)  # IMPORTANT: optim minimizes by default
    }
    
    # perform optimization
    result <- optim(par = c(0, 0), fn = f, method = "L-BFGS-B")
    a1 <- result$par[1]
    a2 <- result$par[2]
    
    # apply 2x leverage scaling
    exposure_now <- abs(a1 * S0) + abs(a2 * C0)
    desired_exposure <- 2 * port_values[length(port_values)]  # 2x leverage
    scaling_factor <- desired_exposure / exposure_now
    
    a1 <- a1 * scaling_factor
    a2 <- a2 * scaling_factor
    
    # update portfolio with real next-day prices
    S1 <- data$Close.x[i + 1]
    S2 <- data$Close.y[i + 1]
    
    next_port_value <- (port_values[length(port_values)] - a1*S0 - a2*C0) * exp(r*t) +
      a1*S1 + a2*S2
    port_values <- c(port_values, next_port_value)
  }
  
  # store final portfolio value from this trial
  final_portfolio_values <- c(final_portfolio_values, port_values[length(port_values)])
}

# compute overall average across trials
average_final_value <- mean(final_portfolio_values)
average_return_percent <- ((average_final_value / 10000) - 1) * 100

# output the results
cat("Average final portfolio value across all trials:", round(average_final_value, 2), "\n")
cat("Average return relative to starting capital:", round(average_return_percent, 2), "%\n")

# plot the final portfolio values over trials
plot(final_portfolio_values, type = "l", xlab = "Trial Number", ylab = "Final Portfolio Value")
