import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

# Load post-training data
df = pd.read_csv('../../TrainingData/ManualCSVs/combined.csv')
df = df.iloc[1350:].reset_index(drop=True)

# Constants
dsv = 0.8
ALPHA = 0.51582 * dsv
BETA1 = -0.04540 * dsv
BETA2 = 0.05334 * dsv
BETA3 = 0.03338 * dsv

days_per_year = 252

# Variables

stop_loss_values = [1e-6, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 0.025, 0.05, 0.075, 0.1, 0.9]
leverage = True

alpha_decay = 0.95
alpha_decay_freq = 30
slip_factor = 0.4

leverageMultiplier = 2
if leverage == False: leverageMultiplier = 1
startMoney = 10000
num_trials = 300

print(f"Leverage Multiplier: {leverageMultiplier}")
print(f"Starting Money: ${startMoney:,.2f}")
print(f"1-year trials per epoch: {num_trials}")

# percentDaysToSell = 0.1

# # Compute realistic stop loss based
# min_stop_loss = (df['OpenDA'] - df['LowDA']) / df['OpenDA']
# realistic_floor = min_stop_loss.quantile(percentDaysToSell)
# print(f"Acceptable drawdown below open: {realistic_floor:.4%} or {realistic_floor:.4} will trigger approx {percentDaysToSell*100}% of the time")

stop_loss_results = {}
average_return_rates = []
recent_losses = []

def estimate_fill_probability(predicted_target, open_price):
    distance = (predicted_target - open_price) / open_price

    # Protect against negative or zero distance
    if distance <= 0:
        return 0.0

    # Parameters for exponential decay
    base_prob = 0.6   # Max probability for near-target fills
    decay_rate = 60.0  # Controls steepness of decay

    prob = base_prob * np.exp(-decay_rate * distance)

    return max(min(prob, base_prob), 0.01)  # Clamp between 1% and base_prob

for lossSellPercent in stop_loss_values:
    trial_annual_balances = np.zeros(days_per_year + 1)
    all_final_moneys = []
    trial_stats = []

    print(f"\n=== Epoch with stop-loss: {lossSellPercent:.4f} ===")

    for trial in range(num_trials):
        if len(df) < days_per_year:
            continue
        start_idx = random.randint(0, len(df) - days_per_year)
        trial_df = df.iloc[start_idx:start_idx + days_per_year].reset_index(drop=True)

        workingMoney = startMoney
        moneyOverTime = [workingMoney]
        total_trades = 0
        above_buy_count = 0
        below_buy_count = 0
        equal_buy_count = 0
        delta_sum = 0.0
        deltas = []

        total_stop_hits = 0
        total_entries = 0

        for idx in range(len(trial_df)):
            if idx % alpha_decay_freq == 0:
                ALPHA *= alpha_decay

            row = trial_df.iloc[idx]
            open_da = row['OpenDA']
            high_da = row['HighDA']
            low_da = row['LowDA']
            close_da = row['CloseDA']
            ldd = row['LDD']
            ldds = row['LDDS']
            l2dds = row['L2DDS']

            if lossSellPercent > 0.05 and np.random.rand() < 0.01:
                catastrophic_loss = workingMoney * np.random.uniform(0.3, 0.7)
                workingMoney -= catastrophic_loss

            buyPrice = open_da
            stopPrice = buyPrice - np.random.normal(0.5, 1.5) * (high_da - low_da)

            capital_fraction = min(1.0, 10000 / workingMoney)
            penalty_factor = max(0.25, 1.0 - 0.15 * sum(1 for l in recent_losses if l < -0.01))
            capital_fraction *= penalty_factor
            shares = workingMoney * capital_fraction / buyPrice

            delta_raw = ALPHA + BETA1 * ldd + BETA2 * ldds + BETA3 * l2dds
            intraday_vol = (high_da - low_da) / open_da
            vol_penalty = np.exp(-6 * intraday_vol)
            decayed_delta = delta_raw * vol_penalty
            highestEstimate = open_da + min(decayed_delta, open_da * 0.02)

            delta_up = highestEstimate - open_da
            delta_down = open_da - stopPrice
            prob_stop_first = delta_down / (delta_up + delta_down + 1e-8)

            stop_hit = low_da <= stopPrice + buyPrice * 0.0015
            if lossSellPercent < 0.001 and np.random.rand() < 0.25:
                stop_hit = False
            target_hit = high_da >= highestEstimate

            if stop_hit:
                total_stop_hits += 1
            total_entries += 1

            fill_prob = estimate_fill_probability(highestEstimate, open_da)

            def scaled_slip():
                daily_vol = max((high_da - low_da) / open_da, 0.002)
                slip = np.random.normal(0.004, 0.002) + daily_vol * slip_factor
                return min(slip, 0.03)

            if stop_hit and target_hit:
                if np.random.rand() < prob_stop_first:
                    slip = scaled_slip()
                    sellPrice = stopPrice * (1 - slip)
                else:
                    if np.random.rand() < fill_prob:
                        slip = scaled_slip()
                        sellPrice = highestEstimate * (1 - slip)
                    else:
                        sellPrice = (open_da + close_da + high_da) / 3
            elif stop_hit:
                slip = scaled_slip()
                sellPrice = stopPrice * (1 - slip)
            elif target_hit:
                if np.random.rand() < fill_prob:
                    slip = scaled_slip()
                    sellPrice = highestEstimate * (1 - slip)
                else:
                    sellPrice = (open_da + close_da + high_da) / 3
            else:
                sellPrice = (open_da + close_da + high_da) / 3

            deltaShare = sellPrice - buyPrice
            pnl = deltaShare * shares * (leverageMultiplier if leverage else 1)

            if stop_hit:
                recent_losses.append(deltaShare)
                if len(recent_losses) > 5:
                    recent_losses.pop(0)

            fee_scaling = 1 + 5 * intraday_vol
            trade_fee_rate = 0.0001 * fee_scaling
            gross_trade_value = shares * (buyPrice + sellPrice)
            total_fees = (gross_trade_value * trade_fee_rate) / 2

            workingMoney += pnl - total_fees
            moneyOverTime.append(workingMoney)
            deltas.append(deltaShare)
            total_trades += 1

            if sellPrice > buyPrice:
                above_buy_count += 1
            elif sellPrice < buyPrice:
                below_buy_count += 1
            else:
                equal_buy_count += 1

        finalMoney = workingMoney
        growthFactor = finalMoney / startMoney
        avg_delta = np.mean(deltas)
        std_delta = np.std(deltas)
        above_pct = 100 * above_buy_count / total_trades
        below_pct = 100 * below_buy_count / total_trades
        equal_pct = 100 * equal_buy_count / total_trades
        avg_high_low_dev = (trial_df['HighDA'] - trial_df['LowDA']).mean()
        avg_high_low_dev_pct = 100 * avg_high_low_dev / trial_df['OpenDA'].mean()

        all_final_moneys.append(finalMoney)
        trial_annual_balances += np.array(moneyOverTime)
        trial_stats.append({
            "Final Money": finalMoney,
            "Growth Factor": growthFactor,
            "Avg delta": avg_delta,
            "Std delta": std_delta,
            "% Above Buy": above_pct,
            "% Below Buy": below_pct,
            "% Equal Buy": equal_pct,
            "High-Low Dev": avg_high_low_dev,
            "High-Low Dev %": avg_high_low_dev_pct
        })

        # Final per-trial metrics
        finalMoney = workingMoney
        growthFactor = finalMoney / startMoney
        avg_delta = np.mean(deltas)
        std_delta = np.std(deltas)
        above_pct = 100 * above_buy_count / total_trades
        below_pct = 100 * below_buy_count / total_trades
        equal_pct = 100 * equal_buy_count / total_trades
        avg_high_low_dev = (trial_df['HighDA'] - trial_df['LowDA']).mean()
        avg_high_low_dev_pct = 100 * avg_high_low_dev / trial_df['OpenDA'].mean()

        all_final_moneys.append(finalMoney)
        trial_annual_balances += np.array(moneyOverTime)
        trial_stats.append({
            "Final Money": finalMoney,
            "Growth Factor": growthFactor,
            "Avg delta": avg_delta,
            "Std delta": std_delta,
            "% Above Buy": above_pct,
            "% Below Buy": below_pct,
            "% Equal Buy": equal_pct,
            "High-Low Dev": avg_high_low_dev,
            "High-Low Dev %": avg_high_low_dev_pct
        })

    # Summary stats for this stop-loss
    mean_final = np.mean([t["Final Money"] for t in trial_stats])
    median_final = np.median([t["Final Money"] for t in trial_stats])
    min_final = np.min([t["Final Money"] for t in trial_stats])
    max_final = np.max([t["Final Money"] for t in trial_stats])
    std_final = np.std([t["Final Money"] for t in trial_stats])
    mean_growth = np.mean([t["Growth Factor"] for t in trial_stats])
    mean_avg_delta = np.mean([t["Avg delta"] for t in trial_stats])
    mean_std_delta = np.mean([t["Std delta"] for t in trial_stats])
    mean_above = np.mean([t["% Above Buy"] for t in trial_stats])
    mean_below = np.mean([t["% Below Buy"] for t in trial_stats])
    mean_equal = np.mean([t["% Equal Buy"] for t in trial_stats])
    stop_hit_rate = total_stop_hits / total_entries
    mean_hl_dev = np.mean([t["High-Low Dev"] for t in trial_stats])
    mean_hl_dev_pct = np.mean([t["High-Low Dev %"] for t in trial_stats])
    annualized_return = mean_growth - 1
    log_returns = np.log([t["Growth Factor"] for t in trial_stats])
    geometric_growth = np.exp(np.mean(log_returns))
    projected_10yr_growth = geometric_growth ** 10
    projected_10yr_money = startMoney * projected_10yr_growth

    # Per-epoch summary
    print(f"Median Final Money: {median_final:,.2f}")
    print(f"Min Final Money: {min_final:,.2f}")
    print(f"Max Final Money: {max_final:,.2f}")
    print(f"Std Dev Final Money: {std_final:,.2f}")
    print(f"Mean Growth Factor: {mean_growth:.4f}")
    print(f"Mean Avg delta: {mean_avg_delta:.4f}")
    print(f"Mean Std Dev delta: {mean_std_delta:.4f}")
    print(f"Mean % Above Buy: {mean_above:.2f}%")
    print(f"Mean % Below Buy: {mean_below:.2f}%")
    print(f"Stop-Loss Hit Rate: {stop_hit_rate:.2%}")
    print(f"Mean High-Low Dev: {mean_hl_dev:.4f} ({mean_hl_dev_pct:.2f}%)")
    print(f"Geometric Growth: {geometric_growth:.2f}")
    print(f"Projected Final Money After 10 Years: {projected_10yr_money:,.2f}")

    stop_loss_results[lossSellPercent] = {
        "mean_balance_per_day": trial_annual_balances / num_trials,
        "final_money_distribution": all_final_moneys,
        "summary": {
            "mean_final": mean_final,
            "std_final": std_final,
            "mean_growth": mean_growth,
            "annualized_return": annualized_return,
            "projected_10yr_money": projected_10yr_money,
        }
    }

    # Append per-epoch average return
    avg_return_rate = np.mean([t["Growth Factor"] for t in trial_stats]) - 1
    average_return_rates.append(avg_return_rate)

    # Plot per-trial average working money
    avg_money_over_time = trial_annual_balances / num_trials
    plt.figure(figsize=(10, 4))
    plt.plot(avg_money_over_time)
    plt.xlabel("Days")
    plt.ylabel("Average Working Money")
    plt.title(f"Avg. Working Money Over Time (Stop-Loss = {lossSellPercent})")
    plt.grid(True)
    plt.tight_layout()

plt.figure(figsize=(10, 6))
plt.semilogx(stop_loss_values, average_return_rates, marker='o')
plt.xlabel("Stop-Loss Percentage")
plt.ylabel("Average Annual Return Rate")
plt.title("Average Return Rate per Stop-Loss Epoch")
plt.grid(True)
plt.tight_layout()

plt.show()
