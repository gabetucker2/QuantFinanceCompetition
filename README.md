# 2024 OSU Quantitative Finance Competition

## Overview

The **2024 OSU Quantitative Finance Competition** was a competition in which our team of five, *The Algebros*, secured the **Gold Medal** for achieving the best statistical analysis and Sharpe ratio–adjusted return out of 15 teams.

Our models increased our **$10k** portfolio budget (with 2x leveraged return) to **$124K** through day trading over a 10-year period in our simulations.

## Team Members

- Gabriel Tucker: [[GitHub](https://github.com/gabetucker2)] [[LinkedIn](https://www.linkedin.com/in/gabetucker2/)]
- Echo Li: [[GitHub](https://github.com/EcchoLi)]
- Nathan Bayer: [[GitHub](https://github.com/nathanbayer123)] [[LinkedIn](http://linkedin.com/in/nathan-bayer)]
- Evelyn Z.: [[GitHub](https://github.com/EvelynZZH11)]
- Ryan R.: [[GitHub](https://github.com/RyanRunxianDu)]

## Announcement post and photos

![Announcement Post](Images/announcementPost.jpg)

## Foreword

### Disclaimer

The only post hoc revisions made to our scripts were in order to make the scripts capable of running in a repo clone's local environment without any changes, in case someone else would like to run the scripts for themselves.  We also slightly modified the titles of our existing graphs for sake of clarity in this.

### Abandoned Work (prior to deadline)

- [**MultimodalSentimentStrategy**](AbandonedScripts/MultimodalAttempt): Initially, we focused on creating a unified system to run all our algorithms through a single Python environment for the sake of scalability and reducing boilerplate code between algorithms. However, we shifted away from this approach in favor of strategies that would produce more immediate results.

- [**ACTRAttempt**](AbandonedScripts/ACTRAttempt): This was an attempt at implement the py-ACTUP implementation of the ACT-R cognitive architecture, a supervised learning algorithm whose working memory module is a production system, in an isolated environment. We decided to abandon this approach due to how long it took to implement compared to other models.

## Submitted Work Timeline

## 📈 [**Candlesticks**](SubmittedScripts/Candlesticks): Surface-Level Analysis of Market Data

First, we decided to visualize the two datasets we were working with, using "candlestick" visualization method, so that we could have a baseline understanding of the market's behavior over the past decade and verify data integrity (which turned out to be useful, because one of the datasets we were using was incorrect).

![cldClosingPrices](Images/cldClosingPrices.png)  
![clfOpeningPrices](Images/clfOpeningPrices.png)  
![clfCandlesticks](Images/clfCandlesticks.png)  
![dalClosingPrices](Images/dalClosingPrices.png)  
![dalOpeningPrices](Images/dalOpeningPrices.png)  
![dalCandlesticks](Images/dalCandlesticks.png)

---

## 🧠 [**FeatureImportanceAnalysis**](SubmittedScripts/FeatureImportanceAnalysis): Hypothesis Testing & Parameter Diagnostics

## Intro

This code was used to perform feature importance analysis—a process for analyzing stock-related features' (i.e., parameters') predictive power for other causally-connected features. There were 5 features we included per dataset in our analysis:

* `Yesterday's closing price` (DAAdjCloseToday) *(in retrospect should have been better named)*
* `Today's closing price` (DACloseToday)
* `Today's highest price` (DAHighToday)
* `Today's lowest price` (DALowToday)
* `Today's trading volume` (DAVolumeToday)

We also only performed feature importance analysis on DAL stock feature importance because we were tasked with trading in Delta Airlines stocks, not crude oil stocks. So by performing feature importance on DAL features, we analyze how those features are affected by A) other available DAL features and B) available CL features.

It is also worth noting we originally attempted to create a modular framework for various feature importance analysis algorithms (available in our project code), but dropped this due to time constraints.

### SelectKBest

SelectKBest is the algorithm we initially decided on to perform feature importance analysis. The algorithm ranks features by their individual linear relationship with the target variable, using an F-statistic derived from univariate linear regression.

We used SelectKBest to quickly identify features with the strongest direct signal, without accounting for interactions or redundancy.

![Images/target_DAAdjCloseToday_feature_importance-1.png](Images/target_DAAdjCloseToday_feature_importance-1.png)
![Images/target_DACloseToday_feature_importance-1.png](Images/target_DACloseToday_feature_importance-1.png)
![Images/target_DAHighToday_feature_importance-1.png](Images/target_DAHighToday_feature_importance-1.png)
![Images/target_DALowToday_feature_importance-1.png](Images/target_DALowToday_feature_importance-1.png)
![Images/target_DAVolumeToday_feature_importance-1.png](Images/target_DAVolumeToday_feature_importance-1.png)

We were unsatisfied with these results since it revealed such negligible differences between all features except today's trading volume, so we decided to use an alternative feature importance analysis algorithm in hopes that it might yield something else interesting before analyzing our feature importance analysis outputs:

### RandomForest

Random Forest creates a set of decision trees that captures nonlinear dependencies and feature interactions. It evaluates feature importance based on how much each feature reduces prediction error.

We used Random Forest to uncover complex relationships that SelectKBest might miss, especially where combinations of features or nonlinearity are involved.

![Images/target_DAAdjCloseToday_RandomForest_feature_importance-1.png](Images/target_DAAdjCloseToday_RandomForest_feature_importance-1.png)
![Images/target_DACloseToday_RandomForest_feature_importance-1.png](Images/target_DACloseToday_RandomForest_feature_importance-1.png)
![Images/target_DAHighToday_RandomForest_feature_importance-1.png](Images/target_DAHighToday_RandomForest_feature_importance-1.png)
![Images/target_DALowToday_RandomForest_feature_importance-1.png](Images/target_DALowToday_RandomForest_feature_importance-1.png)
![Images/target_DAVolumeToday_RandomForest_feature_importance-1.png](Images/target_DAVolumeToday_RandomForest_feature_importance-1.png)

This seems to have doubled down on the intitial results, increasing the importance of DAOpenToday on corresponding features.

## Analyzing outputs



---

## 📊 MultipleLinearRegression: Baseline Modeling Framework

- [**MultipleLinearRegression**](SubmittedScripts/MultipleLinearRegression): This algorithm was used to calculate the coefficients for our **MarketSentimentStrategy**. It was integral in determining how different features interacted and contributed to market predictions.



---

## 🧭 MarketSentimentStrategy: Sentiment-Based Trading Logic

- [**MarketSentimentStrategy**](SubmittedScripts/MarketSentimentStrategy): A trading strategy based on market sentiment analysis, which achieved an average return of 20% (with leverage). This strategy was one of our key components, reflecting a solid understanding of market dynamics.

**Timeline**:
- Translated regression outputs into trade signal weights.
  - *Illustration: Flow diagram of sentiment signal to trade execution.*
- Backtested strategy across different market regimes.
  - *Illustration: Equity curve comparing strategy vs baseline.*

---

## 📉 BrownianStrategy: Stochastic Price Simulation

- [**BrownianStrategy**](SubmittedScripts/BrownianStrategy): A simulation strategy based on Geometric Brownian Motion (GBM) and ordinary differential equations (ODEs). This approach produced an average return of 10.2% (with leverage), outperforming the money market.

**Timeline**:
- Simulated price paths using GBM with historical volatility.
  - *Illustration: Multiple GBM sample paths plotted over time.*
- Applied Monte Carlo strategy testing over simulated trajectories.
  - *Illustration: Histogram of returns across simulation runs.*
