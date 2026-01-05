# 01 - Cash Flow Forecasting

## Business Context

Cash flow forecasting is the cornerstone of Treasury operations. For Oil & Gas companies, accurate forecasting is critical due to:

- **Large transaction values**: Single crude cargo can exceed $50M
- **Volatile commodity prices**: Daily price swings affect cash needs
- **Long payment cycles**: 30-90 day terms create timing gaps
- **Seasonal patterns**: Refining margins vary by season

!!! warning "The Challenge"
    A 5% forecasting error on $1B monthly cash flow = $50M liquidity gap

## Notebook Overview

This notebook demonstrates how to build a production-quality cash flow forecasting system using Facebook's Prophet algorithm, with comparisons to baseline methods.

### What You'll Learn

1. **Exploratory Data Analysis** for Treasury time series
2. **Feature engineering** for cash flow patterns
3. **Prophet model** configuration and tuning
4. **Baseline comparisons** (naive, moving average)
5. **Forecast evaluation** metrics and visualization

## Data Design

### Simulated Dataset

The `generate_cash_flows()` function creates realistic cash flow data with:

```python
from src.treasury_sim.generators import generate_cash_flows

cash_flows = generate_cash_flows(
    days=365,           # 1 year of history
    base_inflow=50_000_000,    # $50M daily base
    base_outflow=45_000_000,   # $45M daily base
    seed=42
)
```

### Data Patterns Included

| Pattern | Implementation | Business Rationale |
|---------|----------------|-------------------|
| **Weekly cycle** | Lower weekends | Banks closed |
| **Month-end spike** | +40% on days 28-31 | Payment runs |
| **Quarterly peaks** | +20% end of Q | Tax, dividends |
| **Seasonality** | Summer peak | Driving season demand |
| **Random noise** | ±15% variation | Normal volatility |
| **Trend** | Slight upward | Business growth |

### Sample Data Structure

| Column | Type | Description |
|--------|------|-------------|
| `date` | datetime | Transaction date |
| `category` | string | INFLOW or OUTFLOW |
| `subcategory` | string | Revenue type, expense type |
| `amount` | float | Transaction amount (positive) |
| `entity` | string | Business unit |
| `currency` | string | TRY, USD, EUR |

## Approach & Methodology

### Step 1: Exploratory Data Analysis

```python
# Aggregate to daily net cash flow
daily_cf = cash_flows.groupby(['date', 'category'])['amount'].sum().unstack()
daily_cf['net'] = daily_cf['INFLOW'] - daily_cf['OUTFLOW']
```

**Key Visualizations:**

- Time series decomposition (trend, seasonal, residual)
- Distribution analysis by day of week
- Month-end vs mid-month patterns
- Autocorrelation plots

### Step 2: Baseline Models

Before using advanced ML, we establish baselines:

| Model | Formula | Use Case |
|-------|---------|----------|
| **Naive** | $\hat{y}_t = y_{t-1}$ | Random walk assumption |
| **7-Day MA** | $\hat{y}_t = \frac{1}{7}\sum_{i=1}^{7} y_{t-i}$ | Weekly patterns |
| **30-Day MA** | $\hat{y}_t = \frac{1}{30}\sum_{i=1}^{30} y_{t-i}$ | Monthly patterns |

### Step 3: Prophet Model

Prophet is ideal for Treasury forecasting because it handles:

- **Multiple seasonalities** (weekly, monthly, yearly)
- **Holiday effects** (payment dates, bank holidays)
- **Trend changes** (business events)
- **Missing data** (weekends, holidays)

```python
from prophet import Prophet

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='multiplicative'  # Better for financial data
)

# Add month-end regressor
df['is_month_end'] = df['ds'].dt.day >= 28
model.add_regressor('is_month_end')

model.fit(train_df)
```

### Step 4: Evaluation

**Metrics Used:**

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| MAE | $\frac{1}{n}\sum|y - \hat{y}|$ | Average error in $ |
| RMSE | $\sqrt{\frac{1}{n}\sum(y - \hat{y})^2}$ | Penalizes large errors |
| MAPE | $\frac{100}{n}\sum|\frac{y - \hat{y}}{y}|$ | Percentage error |

## Key Results

### Model Comparison

| Model | MAE ($M) | MAPE (%) | Notes |
|-------|----------|----------|-------|
| Naive | 8.2 | 15.3 | Poor for patterns |
| 7-Day MA | 5.1 | 9.8 | Captures weekly |
| 30-Day MA | 6.3 | 11.2 | Too smooth |
| **Prophet** | **3.2** | **6.1** | Best overall |

### Business Application

The notebook shows how to use forecasts for:

1. **Liquidity Buffer Sizing**: Forecast + 2σ confidence interval
2. **Funding Decisions**: When to draw credit lines
3. **Investment Planning**: Excess cash deployment
4. **FX Timing**: Currency conversion scheduling

## Thinking Traces

!!! quote "Why Prophet over ARIMA?"
    Prophet handles missing data gracefully (weekends), supports multiple seasonalities natively, and provides intuitive uncertainty intervals. For Treasury, where interpretability matters, Prophet's additive components (trend + seasonality + holidays) are easier to explain to stakeholders than ARIMA's differencing approach.

!!! quote "Why multiplicative seasonality?"
    Cash flow volatility scales with volume. A $100M day has more absolute variation than a $50M day. Multiplicative mode (seasonal effect = base × factor) captures this better than additive mode (seasonal effect = base + constant).

## Executive Dashboard

The notebook concludes with a comprehensive Plotly dashboard showing:

- **30-day forecast** with confidence intervals
- **Model performance comparison** chart
- **Seasonality decomposition** plots
- **Forecast accuracy** gauge

## Next Steps

After mastering this notebook:

1. → [02 Fraud Detection](02-fraud-detection.md) to secure payment flows
2. → [03 FX Risk Management](03-fx-risk-management.md) to forecast currency needs

## Code Access

📓 **Notebook**: [`notebooks/01_cash_flow_forecasting.ipynb`](https://github.com/ozgurgulerx/treasury/blob/main/notebooks/01_cash_flow_forecasting.ipynb)

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
