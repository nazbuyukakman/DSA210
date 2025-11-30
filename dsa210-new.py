# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# -----------------------------
# 1. Load & clean data
# -----------------------------
INPUT_CSV = "DSA210-dataset.csv"      
OUTPUT_CLEAN_CSV = "daily_clean.csv"

df = pd.read_csv(
    INPUT_CSV,
    header=None,
    names=["date", "sweets_consumed", "on_period"],
    usecols=[0, 1, 2],
    sep=None,
    engine="python"
)

# Parse dates
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
df = df.dropna(subset=["date"])

# Convert numeric fields
df["sweets_consumed"] = pd.to_numeric(df["sweets_consumed"], errors="coerce")
df["on_period"] = pd.to_numeric(df["on_period"], errors="coerce")
df = df.dropna(subset=["sweets_consumed", "on_period"])

df["sweets_consumed"] = df["sweets_consumed"].astype(int)
df["on_period"] = df["on_period"].astype(int)

df = df.sort_values("date").reset_index(drop=True)

df["period_status"] = df["on_period"].map({0: "Not on period", 1: "On period"})

df.to_csv(OUTPUT_CLEAN_CSV, index=False)
print(f"[INFO] Cleaned data saved to: {OUTPUT_CLEAN_CSV}\n")

# -----------------------------
# 2. Bar chart: mean sweets
# -----------------------------
mean_by_status = df.groupby("period_status")["sweets_consumed"].mean().reindex(
    ["Not on period", "On period"]
)

plt.figure(figsize=(6, 4))
plt.bar(mean_by_status.index, mean_by_status.values)
plt.ylabel("Average sweet consumption (0–1)")
plt.title("Average Sweet Consumption\nOn Period vs Not on Period")
for i, v in enumerate(mean_by_status.values):
    plt.text(i, v + 0.01, f"{v:.2f}", ha="center", va="bottom")
plt.ylim(0, 1.1)
plt.tight_layout()
plt.show()

# -----------------------------
# 3. Boxplot
# -----------------------------
off_period = df[df["on_period"] == 0]["sweets_consumed"].values
on_period = df[df["on_period"] == 1]["sweets_consumed"].values

plt.figure(figsize=(6, 4))
plt.boxplot([off_period, on_period])
plt.xticks([1, 2], ["Not on period", "On period"])
plt.ylabel("Sweet Consumption (0/1)")
plt.title("Sweet Consumption Distribution by Period Status")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.ylim(-0.1, 1.1)
plt.tight_layout()
plt.show()

# -----------------------------
# 4. Time series with shaded period days
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(
    df["date"],
    df["sweets_consumed"],
    marker="o",
    linestyle="-",
    label="Sweets consumed"
)

y_min = -0.05
y_max = 1.05

plt.fill_between(
    df["date"],
    y_min,
    y_max,
    where=(df["on_period"] == 1),
    alpha=0.25,
    label="On period"
)

plt.ylim(y_min, y_max)
plt.xlabel("Date")
plt.ylabel("Sweet Consumption (0/1)")
plt.title("Daily Sweet Consumption with Period Days Highlighted")
plt.xticks(rotation=45)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# -----------------------------
# 5. Rolling 7-day average
# -----------------------------
df_rolling = df.set_index("date").copy()
df_rolling["rolling_7d_mean"] = df_rolling["sweets_consumed"].rolling(window=7, min_periods=1).mean()

plt.figure(figsize=(10, 5))
plt.plot(
    df_rolling.index,
    df_rolling["rolling_7d_mean"],
    marker="o",
    linestyle="-",
    label="7-day rolling mean of sweets"
)

plt.fill_between(
    df_rolling.index,
    0,
    1.0,
    where=(df_rolling["on_period"] == 1),
    alpha=0.2,
    label="On period"
)

plt.ylim(0, 1.05)
plt.xlabel("Date")
plt.ylabel("Proportion of days with sweets (7-day mean)")
plt.title("7-day Rolling Average of Sweet Consumption\nwith Period Days Highlighted")
plt.xticks(rotation=45)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# -----------------------------
# 6. Stacked bar: sweets vs no sweets
# -----------------------------
crosstab = pd.crosstab(df["period_status"], df["sweets_consumed"])
for val in [0, 1]:
    if val not in crosstab.columns:
        crosstab[val] = 0
crosstab = crosstab[[0, 1]]

labels = crosstab.index.tolist()
no_sweets = crosstab[0].values
yes_sweets = crosstab[1].values

x = np.arange(len(labels))

plt.figure(figsize=(6, 4))
plt.bar(x, no_sweets, label="No sweets (0)")
plt.bar(x, yes_sweets, bottom=no_sweets, label="Sweets (1)")
plt.xticks(x, labels)
plt.ylabel("Number of days")
plt.title("Days with vs without Sweets\nBy Period Status")
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# 7. Hypothesis Test (manual Welch t-test, no SciPy)
# -----------------------------
def welch_t_test(x, y):
    """Manual Welch t-test (normal approximation)"""
    x = np.asarray(x, float)
    y = np.asarray(y, float)

    n1, n2 = len(x), len(y)
    mean1, mean2 = x.mean(), y.mean()
    var1, var2 = x.var(ddof=1), y.var(ddof=1)

    se = math.sqrt(var1 / n1 + var2 / n2)
    t_stat = 0 if se == 0 else (mean1 - mean2) / se

    # Standard normal CDF via erf
    def normal_cdf(z):
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))

    p_two_sided = 2 * (1 - normal_cdf(abs(t_stat)))
    p_one_sided = 1 - normal_cdf(t_stat) if t_stat > 0 else normal_cdf(t_stat)

    return t_stat, p_two_sided, p_one_sided

t_stat, p_two, p_one = welch_t_test(on_period, off_period)
alpha = 0.05

print("\n=== HYPOTHESIS TEST RESULTS ===")
print(f"Mean sweets ON period:  {on_period.mean():.3f}")
print(f"Mean sweets OFF period: {off_period.mean():.3f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"One-sided p-value (H1: mean_on > mean_off): {p_one:.4f}")

if p_one < alpha:
    print("\nDecision: REJECT the null hypothesis (H₀).")
    print("Conclusion: There is statistical evidence that sweet consumption is HIGHER on period days.")
else:
    print("\nDecision: FAIL TO REJECT the null hypothesis (H₀).")
    print("Conclusion: The data does NOT provide enough evidence that sweet consumption is higher on period days.")
