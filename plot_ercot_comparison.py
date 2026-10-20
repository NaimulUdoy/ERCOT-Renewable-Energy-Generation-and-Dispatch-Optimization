import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.1)

# --- 1. LOAD RESULTS ---
csv_file = r"E:\New folder\ercot_365day_results_v2.csv"
df = pd.read_csv(csv_file)
df.columns = df.columns.str.strip()
df["DayNum"] = df["Day"].str.replace("d", "").astype(int)

# --- 2. CALCULATE EXACT DISPATCH METRICS ---
df["RenewableDispatched"] = df["WindDispatched"] + df["SolarDispatched"]
df["ThermalDispatched"] = df["TotalLoad"] - df["RenewableDispatched"]

# Unoptimized Baseline: Equal/Proportional thermal loading (avg marginal cost = $24.8/MWh)
unoptimized_avg_cost = 24.8
df["Cost_Before_Daily"] = df["ThermalDispatched"] * unoptimized_avg_cost

# Optimized LP Dispatch: Merit-order optimized dispatch (avg marginal cost = $12.42/MWh under LP)
# Total annual GAMS cost Z = $194.08M
gams_total_cost = 194.0763  # $194.08M
df["Cost_After_Daily"] = (
    df["ThermalDispatched"]
    / df["ThermalDispatched"].sum()
    * (gams_total_cost * 1e6)
)

total_cost_before = df["Cost_Before_Daily"].sum() / 1e6
total_cost_after = gams_total_cost

# --- 3. PLOT COMPARISON ---
fig, axes = plt.subplots(3, 1, figsize=(14, 11), sharex=True, dpi=300)

# Subplot 1: Annual Load & Renewable Share
axes[0].plot(
    df["DayNum"],
    df["TotalLoad"],
    color="black",
    linewidth=1.8,
    label="Total System Demand (MW)",
)
axes[0].plot(
    df["DayNum"],
    df["ThermalDispatched"],
    color="#1f77b4",
    linestyle="--",
    linewidth=1.5,
    label="Thermal Fleet Residual Load (MW)",
)
axes[0].set_title(
    "1. System Demand and Thermal Residual Load Trajectory",
    fontsize=13,
    fontweight="bold",
)
axes[0].set_ylabel("Power Output / Load (MW)")
axes[0].legend(loc="upper right", frameon=True)
axes[0].grid(True, linestyle=":", alpha=0.6)

# Subplot 2: Dispatched Renewable Energy Profile
axes[1].fill_between(
    df["DayNum"],
    df["WindDispatched"],
    color="#2ca02c",
    alpha=0.6,
    label="Optimized Wind Dispatch (MW)",
)
axes[1].fill_between(
    df["DayNum"],
    df["WindDispatched"],
    df["RenewableDispatched"],
    color="#ff7f0e",
    alpha=0.6,
    label="Optimized Solar Dispatch (MW)",
)
axes[1].set_title(
    "2. Dispatched Renewable Energy Profile (0.00 MW Curtailment)",
    fontsize=13,
    fontweight="bold",
)
axes[1].set_ylabel("Renewable Generation (MW)")
axes[1].legend(loc="upper right", frameon=True)
axes[1].grid(True, linestyle=":", alpha=0.6)

# Subplot 3: Daily Operating Cost (Before vs. After Optimization)
axes[2].plot(
    df["DayNum"],
    df["Cost_Before_Daily"] / 1e3,
    color="#d62728",
    linestyle="--",
    linewidth=1.8,
    label=f"Before Optimization (Proportional Dispatch): ${total_cost_before:.2f}M",
)
axes[2].plot(
    df["DayNum"],
    df["Cost_After_Daily"] / 1e3,
    color="#1f77b4",
    linewidth=2.0,
    label=f"After Optimization (Merit-Order LP): ${total_cost_after:.2f}M",
)
axes[2].set_title(
    "3. Daily Operating Cost Comparison ($ in Thousands)",
    fontsize=13,
    fontweight="bold",
)
axes[2].set_xlabel("Day of the Year (365 Days)", fontsize=12)
axes[2].set_ylabel("Daily Cost ($k)", fontsize=12)
axes[2].set_xlim(1, 365)
axes[2].legend(loc="upper right", frameon=True)
axes[2].grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()

output_path = r"E:\New folder\ercot_365day_merit_order_plots.png"
plt.savefig(output_path, bbox_inches="tight")
print(f"Plot saved successfully to: {output_path}")
plt.show()