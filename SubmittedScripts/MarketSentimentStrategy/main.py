import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
import statistics

df = pd.read_csv('../../TrainingData/ManualCSVs/combined.csv')

# Use only rows 1351 and beyond because MLR uses 0 through 1350
df = df.iloc[1350:].reset_index(drop=True)

dsv = 0.8
ALPHA = 0.51582 * dsv
BETA1 = -0.04540 * dsv
BETA2 = 0.05334 * dsv
BETA3 = 0.03338 * dsv

lossSellPercent = 0.02
leverage = True
leverageMultiplier = 2
startMoney = 10000
years = 10
days_per_year = 252
num_trials = 1000

# Storage
final_money_list = []
growth_factors = []
all_money_over_time = []

# Simulation
for trial in range(num_trials):
    workingMoney = startMoney
    moneyOverTime = [workingMoney]

    for year in range(years):
        sampled_indices = random.sample(range(len(df)), days_per_year)
        for idx in sampled_indices:
            row = df.iloc[idx]

            open_da = row['OpenDA']
            high_da = row['HighDA']
            low_da = row['LowDA']
            close_da = row['CloseDA']
            ldd = row['LDD']
            ldds = row['LDDS']
            l2dds = row['L2DDS']

            buyPrice = open_da
            stopPrice = buyPrice * (1 - lossSellPercent)
            shares = workingMoney / buyPrice

            deltaToHighest = ALPHA + BETA1 * ldd + BETA2 * ldds + BETA3 * l2dds
            highestEstimate = open_da + deltaToHighest

            if high_da >= highestEstimate:
                sellPrice = highestEstimate
            elif low_da < stopPrice:
                sellPrice = stopPrice
            else:
                sellPrice = close_da

            deltaShare = sellPrice - buyPrice
            if leverage:
                workingMoney += deltaShare * shares * leverageMultiplier
            else:
                workingMoney += deltaShare * shares

            moneyOverTime.append(workingMoney)

    final_money_list.append(workingMoney)
    growth_factors.append(workingMoney / startMoney)
    all_money_over_time.append(moneyOverTime)

# Printing and plotting information

average_final_money = np.mean(final_money_list)
median_final_money = np.median(final_money_list)
std_final_money = np.std(final_money_list)
min_final_money = np.min(final_money_list)
max_final_money = np.max(final_money_list)
geometric_mean_growth = statistics.geometric_mean(growth_factors)
compounded_projection = startMoney * geometric_mean_growth

summary = {
    "Median Final Money": median_final_money,
    "Geometric Mean Growth Factor": geometric_mean_growth,
    "Compounded 10-Year Projection": compounded_projection
}

print("\nSummary Statistics for 10-Year Simulation (100 Trials):")
for key, value in summary.items():
    print(f"{key}: {value:,.2f}")

plt.figure(figsize=(12, 6))
for trialMoney in all_money_over_time:
    plt.plot(trialMoney, alpha=0.3)
plt.xlabel('Day')
plt.ylabel('Money')
plt.title(f'{num_trials} Simulated 10-Year Trials')
plt.show()
