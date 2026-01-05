# Data Simulation Package

## Overview

The `src/treasury_sim/generators.py` module provides functions to generate realistic Treasury data for educational and demonstration purposes. All generators produce pandas DataFrames with patterns that mimic real-world financial data.

## Installation

The generators are included in the project. Import them as:

```python
import sys
sys.path.append('..')  # If running from notebooks/
from src.treasury_sim.generators import (
    generate_cash_flows,
    generate_daily_cash_position,
    generate_fx_rates,
    generate_fx_exposures,
    generate_payments,
    generate_commodity_prices,
    generate_counterparties,
    generate_bank_accounts,
    generate_trade_documents,
    set_seed
)

# Set seed for reproducibility
set_seed(42)
```

## Generator Functions

### 1. `generate_cash_flows()`

Generates daily cash flow transactions with realistic patterns.

```python
cash_flows = generate_cash_flows(
    days=365,                    # Number of days
    base_inflow=50_000_000,      # Base daily inflow
    base_outflow=45_000_000,     # Base daily outflow
    seed=42                      # Random seed
)
```

**Output Columns:**

| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Transaction date |
| category | string | INFLOW or OUTFLOW |
| subcategory | string | Revenue type, expense type |
| amount | float | Transaction amount (positive) |
| entity | string | Business unit |
| currency | string | TRY, USD, EUR |

**Patterns Included:**

- Weekly cycle (lower weekends)
- Month-end spikes (+40%)
- Quarterly peaks (+20%)
- Seasonal variation (summer peak)
- Random noise (±15%)

---

### 2. `generate_daily_cash_position()`

Generates daily bank balance positions across multiple accounts.

```python
positions = generate_daily_cash_position(
    days=365,           # Number of days
    n_accounts=5,       # Number of bank accounts
    seed=42
)
```

**Output Columns:**

| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Position date |
| account_id | string | Bank account identifier |
| bank | string | Bank name |
| currency | string | Account currency |
| opening_balance | float | Start of day balance |
| closing_balance | float | End of day balance |

---

### 3. `generate_fx_rates()`

Generates historical FX rate data for currency pairs.

```python
fx_rates = generate_fx_rates(
    days=365,
    currency_pairs=['USD/TRY', 'EUR/TRY', 'EUR/USD'],
    seed=42
)
```

**Output Columns:**

| Column | Type | Description |
|--------|------|-------------|
| timestamp | datetime | Rate timestamp |
| currency_pair | string | Currency pair |
| bid | float | Bid price |
| ask | float | Ask price |
| mid | float | Mid price |

**Patterns Included:**

- TRY depreciation trend (Turkish inflation)
- Volatility clustering
- Mean reversion (short-term)
- Bid-ask spread variation

---

### 4. `generate_fx_exposures()`

Generates open FX exposure positions by entity and currency.

```python
exposures = generate_fx_exposures(
    n_exposures=200,    # Number of positions
    seed=42
)
```

**Output Columns:**

| Column | Type | Description |
|--------|------|-------------|
| exposure_id | string | Unique identifier |
| entity | string | Business unit |
| currency | string | Exposure currency |
| exposure_type | string | RECEIVABLE, PAYABLE, etc. |
| amount_local | float | Amount in local currency |
| maturity_date | datetime | Settlement date |
| maturity_bucket | string | 30D, 60D, 90D, etc. |
| is_hedged | bool | Hedge status |
| hedge_ratio | float | Hedge coverage (0-1) |

---

### 5. `generate_payments()`

Generates payment transactions with fraud indicators.

```python
payments = generate_payments(
    days=90,            # Number of days
    daily_count=50,     # Payments per day
    anomaly_rate=0.02,  # Fraud rate (2%)
    seed=42
)
```

**Output Columns:**

| Column | Type | Description |
|--------|------|-------------|
| payment_id | string | Unique identifier |
| timestamp | datetime | Payment time |
| amount | float | Payment amount |
| currency | string | Payment currency |
| payment_type | string | WIRE, ACH, SWIFT |
| beneficiary_id | string | Recipient ID |
| beneficiary_country | string | Recipient country |
| is_anomaly | bool | Fraud label (ground truth) |
| anomaly_type | string | Type of anomaly |

**Anomaly Types Injected:**

| Type | Description | Frequency |
|------|-------------|-----------|
| large_amount | 10x normal | 0.5% |
| unusual_hour | Outside business hours | 0.5% |
| high_risk_country | Sanctioned jurisdictions | 0.3% |
| new_beneficiary | First-time recipient | 0.4% |
| round_amount | Exact millions | 0.3% |

---

### 6. `generate_commodity_prices()`

Generates commodity price data for oil and refined products.

```python
prices, pivot = generate_commodity_prices(
    days=730,           # 2 years
    seed=42
)

# prices: Long format DataFrame
# pivot: Wide format with date index
```

**Commodities:**

| Commodity | Unit | Base Price | Volatility |
|-----------|------|------------|------------|
| BRENT | $/barrel | $80 | 25% annual |
| WTI | $/barrel | $75 | 25% annual |
| GASOLINE | $/gallon | $2.50 | 20% annual |
| DIESEL | $/gallon | $3.00 | 20% annual |

**Patterns:**

- Mean reversion
- Seasonality (gasoline summer peak)
- Brent-WTI spread
- Crack spread dynamics

---

### 7. `generate_counterparties()`

Generates counterparty master data with credit ratings.

```python
counterparties = generate_counterparties(
    n_counterparties=50,
    seed=42
)
```

**Output Columns:**

| Column | Type | Description |
|--------|------|-------------|
| counterparty_id | string | Unique identifier |
| name | string | Company name |
| type | string | SUPPLIER, CUSTOMER, BANK |
| country | string | Headquarters country |
| credit_rating | string | AAA, AA, BBB, etc. |
| credit_limit | float | Maximum exposure |
| payment_terms | int | Standard payment days |

---

### 8. `generate_bank_accounts()`

Generates bank account master data and balances.

```python
accounts = generate_bank_accounts(
    n_accounts=10,
    seed=42
)
```

**Output Columns:**

| Column | Type | Description |
|--------|------|-------------|
| account_id | string | Account identifier |
| bank | string | Bank name |
| account_type | string | OPERATING, COLLECTION, etc. |
| currency | string | Account currency |
| balance | float | Current balance |
| credit_line | float | Available credit |

---

### 9. `generate_trade_documents()`

Generates trade finance documents (LCs, invoices, B/Ls).

```python
documents = generate_trade_documents(
    n_transactions=100,  # Number of LC sets
    seed=42
)
```

**Output Columns:**

| Column | Type | Description |
|--------|------|-------------|
| document_id | string | Document identifier |
| transaction_id | string | LC transaction reference |
| document_type | string | LC, INVOICE, BILL_OF_LADING, etc. |
| amount | float | Document amount |
| currency | string | Document currency |
| goods_description | string | Goods description |
| quantity | float | Quantity (if applicable) |
| has_discrepancy | bool | Discrepancy flag |
| discrepancy_type | string | Type of discrepancy |

**Document Types:**

- LC (Letter of Credit)
- INVOICE (Commercial Invoice)
- BILL_OF_LADING
- CERTIFICATE_OF_ORIGIN
- QUALITY_CERTIFICATE
- INSURANCE_CERTIFICATE

---

## Utility Functions

### `set_seed(seed)`

Set random seed for reproducibility across all generators.

```python
from src.treasury_sim.generators import set_seed

set_seed(42)  # All subsequent calls will be reproducible
```

---

## Design Principles

### 1. Realistic Patterns

All generators include business-realistic patterns:

```python
# Month-end effect in cash flows
if day_of_month >= 28:
    amount *= 1.4  # 40% increase

# Credit rating affects payment behavior
late_probability = {
    'AAA': 0.02,
    'AA': 0.04,
    'BBB': 0.08,
    'BB': 0.15,
    'B': 0.20
}
```

### 2. Configurable Parameters

Each generator accepts parameters to customize output:

```python
# Adjust base values
cash_flows = generate_cash_flows(
    base_inflow=100_000_000,  # Larger company
    base_outflow=95_000_000
)

# Adjust anomaly rate
payments = generate_payments(
    anomaly_rate=0.05  # Higher fraud rate for testing
)
```

### 3. Reproducibility

Use `set_seed()` for consistent results:

```python
set_seed(42)
df1 = generate_cash_flows(days=30)

set_seed(42)
df2 = generate_cash_flows(days=30)

assert df1.equals(df2)  # Identical outputs
```

### 4. Pandas Integration

All generators return pandas DataFrames for easy analysis:

```python
cash_flows = generate_cash_flows(days=365)

# Standard pandas operations work
daily = cash_flows.groupby('date')['amount'].sum()
monthly = cash_flows.resample('M', on='date')['amount'].sum()
```

---

## Example: Full Data Pipeline

```python
from src.treasury_sim.generators import *

set_seed(42)

# Generate all required data
cash_flows = generate_cash_flows(days=365)
fx_rates = generate_fx_rates(days=365)
exposures = generate_fx_exposures(n_exposures=200)
payments = generate_payments(days=90)
commodities, _ = generate_commodity_prices(days=730)
counterparties = generate_counterparties(n_counterparties=50)
accounts = generate_bank_accounts(n_accounts=10)
documents = generate_trade_documents(n_transactions=100)

print(f"Cash Flows: {len(cash_flows):,} records")
print(f"FX Rates: {len(fx_rates):,} records")
print(f"Exposures: {len(exposures):,} positions")
print(f"Payments: {len(payments):,} transactions")
print(f"Commodities: {len(commodities):,} prices")
print(f"Counterparties: {len(counterparties):,} records")
print(f"Accounts: {len(accounts):,} records")
print(f"Documents: {len(documents):,} documents")
```

---

## Extending Generators

To add custom patterns, modify the generators in `src/treasury_sim/generators.py`:

```python
def generate_custom_data(days=365, custom_param=1.0, seed=42):
    """
    Custom data generator template.
    """
    np.random.seed(seed)

    data = []
    base_date = datetime(2024, 1, 1)

    for i in range(days):
        date = base_date + timedelta(days=i)

        # Add your custom logic here
        value = np.random.normal(100, 10) * custom_param

        data.append({
            'date': date,
            'value': value
        })

    return pd.DataFrame(data)
```

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
