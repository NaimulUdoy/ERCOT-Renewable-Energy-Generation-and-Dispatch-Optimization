# ⚡ ERCOT Renewable Energy Generation & Dispatch Optimization

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GAMS](https://img.shields.io/badge/GAMS-Optimization-orange.svg)](https://www.gams.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive 365-day hourly production cost and renewable generation dispatch framework simulating the **ERCOT** (Electric Reliability Council of Texas) grid. This repository models multi-period optimal power dispatch, tracking thermal residual load, wind/solar curtailment, and daily operating cost comparisons before and after optimization.

---

## 📊 Key Results & Visualizations

### 1. System Demand vs. Thermal Residual Load
![System Demand](results/ercot_365day_merit_order_plots.png)

### 2. Annual Cost Comparison ($ Millions Saved)
* **Before Optimization (Proportional Dispatch):** `$388.87M`
* **After Optimization (Merit-Order LP):** `$194.08M`

---

## 🗂️ Repository Structure

* `models/` — GAMS mathematical programming scripts for economic dispatch and unit commitment.
* `scripts/` — Python automation tools (`plot_ercot_comparison.py`) for processing results and rendering high-resolution figures.
* `results/` — Generated plots, summary statistics, and csv exports.
* `data/` — Hourly profile inputs and load demand curves.

---

## 🚀 Getting Started

### Prerequisites
* **GAMS** (with a solver like CONOPT, CPLEX, or Gurobi)
* **Python 3.10+** with required libraries:
  ```bash
  pip install pandas numpy matplotlib seaborn
