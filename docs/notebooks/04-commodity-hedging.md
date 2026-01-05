# 04 - Commodity Price Hedging

## Business Context

Oil & Gas refiners face dual commodity exposure:

- **Input**: Crude oil purchases (Brent, WTI)
- **Output**: Refined products (gasoline, diesel, jet fuel)
- **Margin**: The "crack spread" = Product price - Crude price

!!! info "What is a Crack Spread?"
    The term comes from the refining process of "cracking" crude oil molecules into lighter products. The **3-2-1 crack spread** assumes 3 barrels of crude yields 2 barrels of gasoline + 1 barrel of diesel.

**The Risk:**

| Scenario | Crude Price | Product Price | Margin Impact |
|----------|-------------|---------------|---------------|
| Crude spike | ↑ $10 | ↑ $5 | **Margin squeeze** |
| Demand drop | ↓ $5 | ↓ $10 | **Margin squeeze** |
| Normal | Stable | Stable | Healthy margin |

## Notebook Overview

This notebook demonstrates commodity price forecasting with ARIMA, crack spread analysis, and hedge recommendation systems.

### What You'll Learn

1. **Commodity price patterns** and volatility
2. **Crack spread calculation** and monitoring
3. **ARIMA forecasting** for price direction
4. **Hedge timing recommendations**
5. **Executive dashboard** for hedging decisions

## Data Design

### Simulated Dataset

```python
from src.treasury_sim.generators import generate_commodity_prices

commodities, commodity_pivot = generate_commodity_prices(
    days=730,  # 2 years
    seed=42
)
```

### Commodities Included

| Commodity | Unit | Typical Range | Volatility |
|-----------|------|---------------|------------|
| Brent Crude | $/barrel | $70-100 | High |
| WTI Crude | $/barrel | $65-95 | High |
| Gasoline | $/gallon | $2.00-3.50 | Medium |
| Diesel | $/gallon | $2.50-4.00 | Medium |

### Price Patterns

- **Mean reversion**: Prices tend toward long-run average
- **Volatility clustering**: High-vol periods persist
- **Seasonality**: Gasoline peaks in summer (driving season)
- **Correlation**: Brent-WTI spread, crack spread dynamics

## Approach & Methodology

### Step 1: Crack Spread Calculation

```python
# Convert to per-barrel basis (42 gallons per barrel)
commodity_pivot['GASOLINE_BBL'] = commodity_pivot['GASOLINE'] * 42
commodity_pivot['DIESEL_BBL'] = commodity_pivot['DIESEL'] * 42

# 3-2-1 Crack Spread
commodity_pivot['CRACK_321'] = (
    (2 * commodity_pivot['GASOLINE_BBL'] +
     1 * commodity_pivot['DIESEL_BBL']) / 3
    - commodity_pivot['BRENT']
)
```

**Interpretation:**

| Crack Spread | Meaning | Action |
|--------------|---------|--------|
| > $20/bbl | Excellent margin | Lock in with futures |
| $10-20/bbl | Normal margin | Monitor |
| < $10/bbl | Margin pressure | Consider production cuts |

### Step 2: ARIMA Forecasting

ARIMA (AutoRegressive Integrated Moving Average) for price direction:

```python
from statsmodels.tsa.arima.model import ARIMA

# Fit ARIMA(5,1,2) model
model = ARIMA(train_prices, order=(5, 1, 2))
fitted = model.fit()

# Forecast 30 days
forecast = fitted.forecast(steps=30)
```

**Model Selection:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| p = 5 | AR(5) | Use last 5 days' prices |
| d = 1 | I(1) | First difference (remove trend) |
| q = 2 | MA(2) | Use last 2 days' errors |

### Step 3: Hedge Recommendation Engine

```python
def generate_hedge_recommendation(price_data, current_hedge_ratio=0.5):
    """
    Generate hedge recommendations based on:
    - Price vs 30-day average
    - Volatility level
    - Crack spread health
    """
    latest = price_data.iloc[-1]
    avg_30d = price_data.iloc[-30:].mean()
    vol_30d = price_data.iloc[-30:].pct_change().std() * np.sqrt(252)

    # Recommendation logic
    if latest['BRENT'] > avg_30d['BRENT'] * 1.05:
        crude_rec = "INCREASE HEDGE - Prices above 30D average"
        target_ratio = min(current_hedge_ratio + 0.2, 1.0)
    elif latest['BRENT'] < avg_30d['BRENT'] * 0.95:
        crude_rec = "REDUCE HEDGE - Prices below 30D average"
        target_ratio = max(current_hedge_ratio - 0.1, 0.3)
    else:
        crude_rec = "MAINTAIN - Prices near average"
        target_ratio = current_hedge_ratio

    return {
        'crude_recommendation': crude_rec,
        'target_hedge_ratio': target_ratio,
        'volatility': vol_30d,
        'crack_spread': latest['CRACK_321']
    }
```

### Step 4: Backtest Strategy

Test the recommendation engine on historical data:

```python
def backtest_strategy(prices, initial_hedge=0.5):
    """
    Simulate hedge decisions and calculate P&L impact.
    """
    hedge_ratio = initial_hedge
    total_cost = 0
    hedge_cost = 0

    for i in range(30, len(prices)):
        # Get recommendation
        rec = generate_hedge_recommendation(prices.iloc[:i], hedge_ratio)
        hedge_ratio = rec['target_hedge_ratio']

        # Calculate next day's P&L
        price_change = prices.iloc[i]['BRENT'] - prices.iloc[i-1]['BRENT']
        unhedged_impact = price_change * (1 - hedge_ratio)

        total_cost += abs(unhedged_impact)

    return total_cost
```

## Key Results

### ARIMA Forecast Performance

| Metric | Value | Interpretation |
|--------|-------|----------------|
| MAE | $2.15 | Average error ~$2/bbl |
| RMSE | $3.42 | Larger errors penalized |
| MAPE | 2.8% | ~3% percentage error |

**Note**: Commodity forecasting is notoriously difficult. ARIMA provides directional guidance, not precise predictions.

### Crack Spread Statistics

| Metric | Value |
|--------|-------|
| Mean | $15.23/bbl |
| Std Dev | $4.87/bbl |
| Min | $3.12/bbl |
| Max | $28.45/bbl |

### Hedge Strategy Backtest

| Strategy | Cost Reduction | Notes |
|----------|----------------|-------|
| No hedge | Baseline | Full exposure |
| Fixed 50% | 45% | Simple approach |
| **Dynamic** | **62%** | Recommendation engine |
| Full hedge | 95% | High cost, no upside |

## Thinking Traces

!!! quote "Why ARIMA over more complex models?"
    For commodity prices, simple models often perform as well as complex ones because markets are efficient. ARIMA captures autocorrelation without overfitting. More complex models (LSTM, etc.) may capture noise rather than signal.

!!! quote "Why not use ARIMA for trading signals?"
    Forecasting accuracy of 2-3% is useful for risk management (hedge timing) but NOT for speculative trading. Transaction costs and bid-ask spreads would eliminate any edge. Use for risk management, not speculation.

!!! quote "Why dynamic hedging?"
    Static hedging (always 50%) ignores market conditions. When prices are above average, hedging more locks in better prices. When prices are below average, hedging less allows buying cheaper later. This simple rule adds value over static approaches.

## Executive Dashboard

The notebook includes a hedging decision dashboard:

- **Brent price with 30-day MA** (trend signal)
- **3-2-1 Crack spread** (margin health)
- **Rolling 30-day volatility** (risk level)
- **Price-crack correlation** (relationship analysis)

## Business Application

### Hedging Instruments

| Instrument | Use Case | Pros | Cons |
|------------|----------|------|------|
| **Futures** | Lock price | Simple, liquid | No upside |
| **Swaps** | Fixed-for-float | Customizable | Counterparty risk |
| **Options** | Protection + upside | Flexibility | Premium cost |
| **Collars** | Bounded range | Low/zero cost | Capped upside |

### Hedge Accounting (IFRS 9)

To qualify for hedge accounting:

1. **Documentation**: Formal hedge designation
2. **Effectiveness**: 80-125% offset
3. **Probability**: Hedged item highly probable
4. **Measurability**: Fair value determinable

## Next Steps

After mastering this notebook:

1. → [05 Trade Finance](05-trade-finance.md) for crude purchase documentation
2. → [03 FX Risk Management](03-fx-risk-management.md) for USD exposure from crude

## Code Access

📓 **Notebook**: [`notebooks/04_commodity_hedging.ipynb`](https://github.com/ozgurgulerx/treasury/blob/main/notebooks/04_commodity_hedging.ipynb)

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
