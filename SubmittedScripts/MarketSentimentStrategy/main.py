import pandas as pd
import matplotlib.pyplot as plt
import random

# Read the CSV file into a DataFrame
df = pd.read_csv('data.csv', delimiter='\t')

dsv = 0.8

ALPHA = 0.51582  * dsv
BETA1 = -0.04540 * dsv
BETA2 = 0.05334  * dsv
BETA3 = 0.03338  * dsv

trainSet = 1300
df = df.iloc[trainSet:]

epochs = 1

lossSellPercent = 0.02

buyPrices = []
sellPrices = []

deltaMoney = 0

leverage = True
leverageMultiplier = 2

workingFinalPrice = 0

startMoney = 10000

daysToSelect = 252 # 1 trading year per epoch

moneyOverTime = []

for e in range(epochs):

    workingMoney = startMoney
    moneyOverTime = [workingMoney] # track money over time

    sampled_indices = random.sample(range(len(df)), daysToSelect)
    for idx in sampled_indices: # probablistic

    # startDay = 0
    # for idx in range(startDay, 252*2): # first 252
        
        row = df.iloc[idx]  # Get the row corresponding to the index

        open_cl = row['OpenCL']
        high_cl = row['HighCL']
        low_cl = row['LowCL']
        close_cl = row['CloseCL']
        open_da = row['OpenDA']
        high_da = row['HighDA']
        low_da = row['LowDA']
        close_da = row['CloseDA']
        ldd = row['LDD']
        ldds = row['LDDS']
        l2dds = row['L2DDS']
        
        buyPrice = open_da
        stopPrice = buyPrice * (1-lossSellPercent)
        shares = workingMoney / buyPrice

        deltaToHighest = ALPHA + BETA1*ldd + BETA2*ldds + BETA3*l2dds
        highestEstimate = open_da + deltaToHighest

        sellPrice = 0
        if high_da >= highestEstimate:
            sellPrice = highestEstimate
        elif low_da < stopPrice:
            sellPrice = stopPrice
        else:
            sellPrice = close_da

        deltaShare = sellPrice - buyPrice

        if leverage:
            workingMoney += deltaShare*shares*leverageMultiplier
        else:
            workingMoney += deltaShare*shares
        moneyOverTime.append(workingMoney)

    workingFinalPrice += moneyOverTime[-1]

averageFinalMoney = workingFinalPrice / epochs

print(f"Days: {daysToSelect}")
print(f"Leverage: {leverage}")
print(f"Simulations: {epochs}")
print(f"Average final money: {averageFinalMoney}")
print(f"Money gained: {averageFinalMoney - startMoney}")
print(f"% money increase: {((averageFinalMoney/startMoney)-1)*100}%")

plt.plot(moneyOverTime)
plt.xlabel('Time step')
plt.ylabel('Money')
plt.title('Random Days from the 5 Years After Training')
plt.show()
