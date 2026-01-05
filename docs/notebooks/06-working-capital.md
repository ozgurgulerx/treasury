# 06 - Working Capital Optimization

## Business Context

Working capital management is critical for Oil & Gas refiners:

- **Receivables (AR)**: $500M-2B outstanding at any time
- **Payables (AP)**: Crude suppliers, contractors, utilities
- **Inventory**: Crude oil, refined products, spare parts
- **Cash Conversion Cycle**: Typically 30-90 days

!!! info "Working Capital Formula"
    **Net Working Capital = Current Assets - Current Liabilities**

    Where:
    - Current Assets = Cash + AR + Inventory
    - Current Liabilities = AP + Short-term Debt

**The Challenge:**

| Component | Typical Value | Optimization Target |
|-----------|---------------|---------------------|
| DSO | 35 days | 30 days (-$68M cash) |
| DPO | 28 days | 35 days (+$80M cash) |
| DIO | 25 days | 22 days (+$35M cash) |

## Notebook Overview

This notebook demonstrates working capital analytics, late payment prediction, and optimization strategies.

### What You'll Learn

1. **Working capital metrics** (DSO, DPO, DIO, CCC)
2. **Receivables aging analysis** and risk assessment
3. **Late payment prediction** with Random Forest
4. **Early payment discount optimization**
5. **Working capital forecasting**

## Data Design

### Simulated Datasets

```python
# Custom generators in the notebook
receivables = generate_receivables(n_invoices=500, seed=42)
payables = generate_payables(n_invoices=400, seed=42)
```

### Receivables Structure

| Column | Type | Description |
|--------|------|-------------|
| invoice_id | string | Unique identifier |
| customer | string | Customer name |
| credit_rating | string | AAA, AA, BBB, BB, B |
| invoice_date | datetime | Issue date |
| amount | float | Invoice amount |
| payment_terms | int | Days (15, 30, 45, 60) |
| due_date | datetime | Payment due date |
| status | string | OPEN, PAID, OVERDUE |
| days_late | int | Days past due (if paid) |

### Customer Profiles

| Customer Type | Rating | Late Prob | Typical Amount |
|---------------|--------|-----------|----------------|
| Major oil companies | AAA | 2% | $1-20M |
| Regional traders | AA | 4% | $0.5-5M |
| Local distributors | BBB | 10% | $100K-2M |
| Small dealers | BB/B | 15-20% | $10K-500K |

## Approach & Methodology

### Step 1: Working Capital Metrics

```python
def calculate_wc_metrics(receivables, payables):
    """
    Calculate key working capital KPIs.
    """
    # Days Sales Outstanding
    total_ar = receivables[receivables['status'] != 'PAID']['amount'].sum()
    dso = (total_ar / annual_revenue) * 365

    # Days Payable Outstanding
    total_ap = payables[payables['status'] != 'PAID']['amount'].sum()
    dpo = (total_ap / annual_cogs) * 365

    # Days Inventory Outstanding
    dio = (inventory_value / annual_cogs) * 365

    # Cash Conversion Cycle
    ccc = dso + dio - dpo

    return {'DSO': dso, 'DPO': dpo, 'DIO': dio, 'CCC': ccc}
```

**Metric Interpretation:**

| Metric | Formula | Good Value |
|--------|---------|------------|
| DSO | (AR / Revenue) × 365 | < 30 days |
| DPO | (AP / COGS) × 365 | > 30 days |
| DIO | (Inventory / COGS) × 365 | < 25 days |
| CCC | DSO + DIO - DPO | < 30 days |

### Step 2: Receivables Aging

```python
def get_aging_bucket(invoice):
    days_outstanding = (today - invoice['invoice_date']).days

    if days_outstanding <= 30:
        return '0-30'
    elif days_outstanding <= 60:
        return '31-60'
    elif days_outstanding <= 90:
        return '61-90'
    else:
        return '90+'
```

**Aging Risk Assessment:**

| Bucket | Risk Level | Collection Action |
|--------|------------|-------------------|
| 0-30 | Low | Standard process |
| 31-60 | Medium | Reminder calls |
| 61-90 | High | Collection team |
| 90+ | Very High | Legal/write-off review |

### Step 3: Late Payment Prediction

```python
from sklearn.ensemble import RandomForestClassifier

# Features
features = [
    'amount_log',      # Invoice size
    'payment_terms',   # Contract terms
    'rating_numeric',  # Credit rating
    'month',           # Seasonality
    'is_month_end'     # Timing
]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict probability of late payment
late_probability = model.predict_proba(X_new)[:, 1]
```

**Model Performance:**

| Metric | Value |
|--------|-------|
| Accuracy | 78% |
| Precision | 72% |
| Recall | 85% |
| AUC-ROC | 0.82 |

### Step 4: Early Payment Discount Analysis

```python
def calculate_discount_apr(discount_pct, discount_days, payment_terms):
    """
    Calculate APR equivalent of early payment discount.

    Example: 2/10 net 30 (2% discount if paid in 10 days)
    APR = (2 / 98) × (365 / 20) = 37.2%
    """
    days_saved = payment_terms - discount_days
    apr = (discount_pct / (100 - discount_pct)) * (365 / days_saved) * 100
    return apr
```

**Decision Rule:**

```
If Discount APR > Cost of Capital → Take discount
If Discount APR < Cost of Capital → Pay at due date
```

| Discount Terms | APR Equivalent | Decision (8% CoC) |
|----------------|----------------|-------------------|
| 2/10 net 30 | 37.2% | Take discount |
| 1/10 net 30 | 18.4% | Take discount |
| 1/10 net 60 | 7.3% | Pay at due date |

## Key Results

### Working Capital Snapshot

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| DSO | 35 days | 30 days | 5 days |
| DPO | 28 days | 35 days | 7 days |
| DIO | 26 days | 22 days | 4 days |
| **CCC** | **33 days** | **17 days** | **16 days** |

### Collection Optimization

| Customer Segment | Current DSO | With ML Targeting | Improvement |
|------------------|-------------|-------------------|-------------|
| AAA/AA | 28 days | 27 days | 1 day |
| BBB | 38 days | 33 days | 5 days |
| BB/B | 52 days | 42 days | 10 days |

### Discount Capture

| Current State | Optimized |
|--------------|-----------|
| 20% discounts captured | 80% captured |
| $100K annual savings | **$500K savings** |

## Thinking Traces

!!! quote "Why Random Forest for late payment prediction?"
    Random Forest handles mixed data types (numeric amounts, categorical ratings) well, provides feature importance for interpretability, and is robust to outliers. The ensemble approach reduces overfitting compared to single decision trees.

!!! quote "Why is credit rating the top predictor?"
    Credit ratings encode historical payment behavior and financial health. A BBB-rated company has inherently different payment patterns than AAA. The model learns to weight this heavily, which aligns with business intuition.

!!! quote "Why focus on BB/B customers for collection?"
    The ML model shows these segments have the highest late payment probability (15-20%). Targeting collection efforts here has the highest ROI. AAA customers rarely pay late, so efforts there are wasted.

## Executive Dashboard

The notebook includes a working capital dashboard:

- **Cash Conversion Cycle waterfall** (DSO + DIO - DPO)
- **AR aging distribution** (pie chart by bucket)
- **Collection performance by rating** (bar chart)
- **Net Working Capital gauge** (vs target)
- **Payables by category** (supplier mix)
- **DSO trend** (line chart with target)

## Business Application

### Collection Prioritization

```
High Priority (Contact this week):
├── High late probability (>60%)
├── Large amount (>$500K)
└── Approaching due date (<7 days)

Medium Priority (Monitor):
├── Medium probability (30-60%)
└── Standard amounts

Low Priority (Auto-process):
├── Low probability (<30%)
└── AAA/AA customers
```

### Working Capital Levers

| Lever | Action | Impact |
|-------|--------|--------|
| **Reduce DSO** | Earlier invoicing, faster collection | ↓ Cash tied in AR |
| **Increase DPO** | Negotiate longer terms | ↑ Free cash |
| **Reduce DIO** | JIT inventory, demand forecasting | ↓ Cash tied in inventory |
| **Capture discounts** | Pay early when APR > CoC | ↓ Total cost |

## Next Steps

After mastering this notebook:

1. → [01 Cash Flow Forecasting](01-cash-flow-forecasting.md) for liquidity planning
2. → [07 Treasury Copilot](07-treasury-copilot.md) for self-service analytics

## Code Access

📓 **Notebook**: [`notebooks/06_working_capital.ipynb`](https://github.com/ozgurgulerx/treasury/blob/main/notebooks/06_working_capital.ipynb)

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
