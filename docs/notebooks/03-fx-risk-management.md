# 03 - FX Risk Management

## Business Context

Oil & Gas companies face significant foreign exchange exposure:

- **Crude purchases**: Denominated in USD globally
- **Product sales**: Local currency (TRY in Turkey)
- **Result**: Structural USD short position

For a Turkish refiner:
- Buy crude in USD → Pay more TRY when USD strengthens
- Sell products in TRY → Revenue fixed in local currency
- **Net exposure**: USD payables exceed USD receivables

!!! warning "The Risk"
    10% USD/TRY movement on $500M monthly crude purchases = **$50M P&L impact**

## Notebook Overview

This notebook demonstrates FX risk quantification, hedge optimization using Monte Carlo simulation, and exposure management strategies.

### What You'll Learn

1. **FX exposure aggregation** across entities
2. **Volatility analysis** and VaR calculation
3. **Monte Carlo simulation** for hedge optimization
4. **Hedge effectiveness** measurement (IFRS 9)
5. **FX risk dashboard** design

## Data Design

### Simulated Datasets

```python
from src.treasury_sim.generators import generate_fx_rates, generate_fx_exposures

# Historical FX rates
fx_rates = generate_fx_rates(
    days=365,
    currency_pairs=['USD/TRY', 'EUR/TRY', 'EUR/USD'],
    seed=42
)

# Open FX exposures
exposures = generate_fx_exposures(
    n_exposures=200,
    seed=42
)
```

### FX Rate Patterns

| Pattern | Implementation | Rationale |
|---------|----------------|-----------|
| **Trend** | Gradual TRY depreciation | Turkish inflation |
| **Volatility clustering** | GARCH-like behavior | Market stress periods |
| **Mean reversion** | Short-term | Technical trading |
| **Jumps** | Occasional large moves | Central bank actions |

### Exposure Categories

| Type | Sign | Example |
|------|------|---------|
| RECEIVABLE | + | USD sales to export customers |
| PAYABLE | - | USD crude purchases |
| FORECAST_REVENUE | + | Expected USD income |
| FORECAST_COST | - | Planned USD spending |

## Approach & Methodology

### Step 1: Exposure Analysis

```python
# Aggregate exposures by currency and maturity
exposure_summary = exposures.groupby(['currency', 'maturity_bucket']).agg({
    'amount_local': 'sum',
    'is_hedged': 'mean'
})
```

**Key Metrics:**

| Metric | Formula | Purpose |
|--------|---------|---------|
| Net Exposure | Receivables - Payables | Total risk position |
| Hedge Ratio | Hedged / Total | Coverage level |
| Open Exposure | Net × (1 - Hedge Ratio) | Unprotected risk |

### Step 2: Volatility Analysis

```python
# Calculate returns and volatility
fx_returns = fx_rates.pct_change()
annual_vol = fx_returns.std() * np.sqrt(252)

# Value at Risk (95% confidence)
var_95 = fx_returns.quantile(0.05)
```

**Volatility Metrics:**

| Metric | USD/TRY | EUR/TRY | Interpretation |
|--------|---------|---------|----------------|
| Daily Vol | 1.2% | 1.1% | Average daily move |
| Annual Vol | 19% | 17% | Yearly uncertainty |
| VaR (95%) | -2.1% | -1.9% | Worst daily loss (95% conf) |

### Step 3: Monte Carlo Simulation

Simulate thousands of FX scenarios to find optimal hedge ratio:

```python
def monte_carlo_hedge_analysis(exposure, fx_start, volatility,
                                hedge_ratios, n_simulations=10000):
    """
    Simulate P&L for different hedge ratios.
    """
    results = []

    for hr in hedge_ratios:
        # Simulate FX movements
        fx_changes = np.random.normal(0, volatility, n_simulations)
        fx_end = fx_start * (1 + fx_changes)

        # Calculate P&L
        unhedged_pnl = exposure * fx_changes
        hedge_pnl = -exposure * hr * fx_changes
        net_pnl = unhedged_pnl + hedge_pnl

        results.append({
            'hedge_ratio': hr,
            'mean_pnl': net_pnl.mean(),
            'std_pnl': net_pnl.std(),
            'var_95': np.percentile(net_pnl, 5)
        })

    return pd.DataFrame(results)
```

**Optimization Objective:**

Minimize Value at Risk (VaR) while considering:

- Hedge costs (forward points)
- Operational constraints
- Accounting treatment (IFRS 9)

### Step 4: Hedge Effectiveness

IFRS 9 requires hedge effectiveness between 80-125%:

```python
def calculate_hedge_effectiveness(exposure_pnl, hedge_pnl):
    """
    Hedge effectiveness = |Hedge P&L / Exposure P&L|
    Must be between 80% and 125% for hedge accounting.
    """
    effectiveness = abs(hedge_pnl / exposure_pnl) * 100
    qualifies = 80 <= effectiveness <= 125
    return effectiveness, qualifies
```

## Key Results

### Optimal Hedge Ratio

| Hedge Ratio | VaR (95%) | Std Dev | Recommendation |
|-------------|-----------|---------|----------------|
| 0% | -$8.2M | $4.1M | Too risky |
| 50% | -$4.1M | $2.1M | Moderate |
| 75% | -$2.1M | $1.0M | **Optimal** |
| 100% | -$0.5M | $0.3M | Over-hedged (costly) |

**Finding**: 75% hedge ratio minimizes VaR while maintaining flexibility for favorable moves.

### Hedge Effectiveness Analysis

```
Scenario: USD strengthens 5%
├── Exposure P&L: -$25M (loss on USD payables)
├── Hedge P&L: +$18.75M (gain on forwards at 75% ratio)
├── Net P&L: -$6.25M
└── Effectiveness: 75% ✓ (qualifies for hedge accounting)
```

## Thinking Traces

!!! quote "Why Monte Carlo over analytical VaR?"
    Analytical VaR assumes normal distribution, but FX returns have fat tails (more extreme moves than normal). Monte Carlo can simulate any distribution, including the heavy tails observed in USD/TRY during crisis periods.

!!! quote "Why not 100% hedge?"
    Full hedging eliminates both downside AND upside. For a refiner with natural TRY revenue, keeping some exposure allows benefiting from TRY strength. Also, forward points (hedge cost) can be significant for EM currencies.

!!! quote "Why 75% optimal?"
    Balances risk reduction (VaR drops 75%) with upside participation and hedge costs. This ratio also typically qualifies for hedge accounting under IFRS 9.

## Executive Dashboard

The notebook includes a comprehensive FX risk dashboard:

- **Net exposure by currency** (pie chart)
- **USD/TRY rate YTD** (line chart with MA)
- **Exposure maturity profile** (bar chart)
- **Hedge coverage by currency** (bar chart with target line)
- **Rolling VaR trend** (line chart)
- **P&L waterfall** (attribution chart)

## Business Application

### FX Risk Management Workflow

```
┌─────────────────┐
│ Exposure        │
│ Aggregation     │──┐
└─────────────────┘  │
                     ▼
┌─────────────────┐  ┌─────────────────┐
│ Market Data     │──▶  Risk          │
│ (FX rates, vol) │  │  Calculation   │
└─────────────────┘  └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Hedge           │
                     │ Recommendation  │
                     └────────┬────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     ┌─────────────────┐             ┌─────────────────┐
     │ Forward         │             │ Option          │
     │ Execution       │             │ Execution       │
     └─────────────────┘             └─────────────────┘
```

### Natural Hedge Consideration

For Oil & Gas, consider the oil-USD correlation:

- Oil prices and USD often move together
- TRY weakening may coincide with oil price rises
- Natural hedge exists in the commodity-currency relationship

## Next Steps

After mastering this notebook:

1. → [04 Commodity Hedging](04-commodity-hedging.md) for oil price risk
2. → [06 Working Capital](06-working-capital.md) for AR/AP in foreign currency

## Code Access

📓 **Notebook**: [`notebooks/03_fx_risk_management.ipynb`](https://github.com/ozgurgulerx/treasury/blob/main/notebooks/03_fx_risk_management.ipynb)

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
