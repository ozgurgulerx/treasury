# Data Sources & Simulation Strategy

This document outlines the data sources required for Treasury AI solutions, their formats, storage recommendations, and strategies for simulating test datasets.

## Data Sources Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TREASURY DATA ECOSYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INTERNAL SYSTEMS                     EXTERNAL SOURCES                       │
│  ┌──────────────────────┐            ┌──────────────────────┐               │
│  │ SAP ERP              │            │ Market Data          │               │
│  │ • GL Entries         │            │ • FX Rates           │               │
│  │ • AP/AR              │            │ • Commodity Prices   │               │
│  │ • Bank Master        │            │ • Interest Rates     │               │
│  │ • Payment Files      │            │                      │               │
│  └──────────────────────┘            └──────────────────────┘               │
│                                                                              │
│  ┌──────────────────────┐            ┌──────────────────────┐               │
│  │ Treasury Mgmt System │            │ Bloomberg/Reuters    │               │
│  │ • Cash Positions     │            │ • Real-time Quotes   │               │
│  │ • FX Trades          │            │ • News/Sentiment     │               │
│  │ • Hedging Positions  │            │ • Analytics          │               │
│  └──────────────────────┘            └──────────────────────┘               │
│                                                                              │
│  ┌──────────────────────┐            ┌──────────────────────┐               │
│  │ Banking Systems      │            │ Regulatory           │               │
│  │ • Bank Statements    │            │ • Sanctions Lists    │               │
│  │ • SWIFT Messages     │            │ • Compliance Data    │               │
│  │ • Payment Status     │            │ • CPI/Inflation      │               │
│  └──────────────────────┘            └──────────────────────┘               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Detailed Data Source Catalog

### 1. Cash Flow Data

| Data Source | Format | Frequency | Volume | Storage |
|-------------|--------|-----------|--------|---------|
| Bank Statements | MT940/CAMT.053 | Daily | ~100 files/day | OneLake Bronze |
| SAP GL Entries | IDoc/CSV | Real-time/Batch | ~10K records/day | OneLake Bronze |
| Payment Files | PAIN.001/CSV | Real-time | ~5K records/day | OneLake Bronze |
| Cash Forecasts | Excel/CSV | Weekly | ~50 rows | OneLake Gold |

**Simulation Strategy:**
```python
# Cash Flow Data Generator
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_cash_flows(days=365, accounts=10):
    """Generate realistic cash flow data for simulation"""
    data = []
    base_date = datetime.now() - timedelta(days=days)

    for day in range(days):
        current_date = base_date + timedelta(days=day)
        for account in range(accounts):
            # Inflows (receivables - larger, less frequent)
            if np.random.random() > 0.7:
                data.append({
                    'date': current_date,
                    'account_id': f'ACC_{account:03d}',
                    'type': 'INFLOW',
                    'amount': np.random.uniform(100000, 5000000),
                    'currency': np.random.choice(['USD', 'EUR', 'TRY'], p=[0.6, 0.3, 0.1]),
                    'category': np.random.choice(['RECEIVABLE', 'INTEREST', 'REFUND']),
                    'counterparty': f'CUST_{np.random.randint(1, 100):03d}'
                })

            # Outflows (payables - smaller, more frequent)
            for _ in range(np.random.randint(1, 5)):
                data.append({
                    'date': current_date,
                    'account_id': f'ACC_{account:03d}',
                    'type': 'OUTFLOW',
                    'amount': -np.random.uniform(10000, 500000),
                    'currency': np.random.choice(['USD', 'EUR', 'TRY'], p=[0.5, 0.3, 0.2]),
                    'category': np.random.choice(['SUPPLIER', 'SALARY', 'TAX', 'UTILITY']),
                    'counterparty': f'SUPP_{np.random.randint(1, 200):03d}'
                })

    return pd.DataFrame(data)
```

### 2. FX Exposure Data

| Data Source | Format | Frequency | Volume | Storage |
|-------------|--------|-----------|--------|---------|
| FX Rates | JSON/CSV | Real-time | ~1K records/hour | Real-Time Intelligence |
| FX Positions | SAP/TMS Export | Daily | ~500 records | OneLake Silver |
| FX Forwards | SWIFT MT300 | On-trade | ~50 records/day | OneLake Bronze |
| FX Forecasts | Excel | Monthly | ~100 rows | OneLake Gold |

**Simulation Strategy:**
```python
def generate_fx_rates(currencies=['USD/TRY', 'EUR/TRY', 'EUR/USD'], hours=720):
    """Generate realistic FX rate time series with volatility"""
    data = []
    base_rates = {'USD/TRY': 34.0, 'EUR/TRY': 37.0, 'EUR/USD': 1.08}

    for currency in currencies:
        rate = base_rates[currency]
        for hour in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-hour)
            # Random walk with drift and volatility
            rate *= (1 + np.random.normal(0.0001, 0.005))
            data.append({
                'timestamp': timestamp,
                'currency_pair': currency,
                'bid': rate * 0.999,
                'ask': rate * 1.001,
                'mid': rate
            })

    return pd.DataFrame(data)
```

### 3. Payment Transaction Data

| Data Source | Format | Frequency | Volume | Storage |
|-------------|--------|-----------|--------|---------|
| Payments | PAIN.001/XML | Real-time | ~2K records/day | OneLake Bronze |
| Payment Status | PAIN.002/XML | Real-time | ~2K records/day | OneLake Bronze |
| Vendor Master | SAP IDoc | Daily | ~5K records | OneLake Silver |
| Sanctions List | CSV | Weekly | ~50K records | OneLake Silver |

**Simulation Strategy:**
```python
def generate_payments(days=90, daily_count=100):
    """Generate payment transactions with anomaly flags"""
    data = []

    for day in range(days):
        current_date = datetime.now() - timedelta(days=days-day)

        for i in range(daily_count):
            is_anomaly = np.random.random() > 0.98  # 2% anomaly rate

            payment = {
                'payment_id': f'PAY_{day:03d}_{i:04d}',
                'date': current_date,
                'amount': np.random.uniform(1000, 100000),
                'currency': np.random.choice(['USD', 'EUR', 'TRY']),
                'beneficiary_name': f'VENDOR_{np.random.randint(1, 500):03d}',
                'beneficiary_account': f'IBAN_{np.random.randint(10000000, 99999999)}',
                'beneficiary_country': np.random.choice(['TR', 'US', 'DE', 'GB']),
                'payment_type': np.random.choice(['SUPPLIER', 'SALARY', 'TAX']),
                'is_anomaly': is_anomaly
            }

            # Inject anomaly characteristics
            if is_anomaly:
                payment['amount'] *= np.random.uniform(2, 10)  # Unusual amount
                if np.random.random() > 0.5:
                    payment['beneficiary_country'] = 'XX'  # Unknown country

            data.append(payment)

    return pd.DataFrame(data)
```

### 4. Commodity Price Data

| Data Source | Format | Frequency | Volume | Storage |
|-------------|--------|-----------|--------|---------|
| Crude Prices (Brent, WTI) | JSON/CSV | Real-time | ~1K records/hour | Real-Time Intelligence |
| Product Prices | CSV | Daily | ~50 records | OneLake Silver |
| Crack Spreads | Calculated | Daily | ~10 records | OneLake Gold |
| Forward Curves | Bloomberg | Daily | ~100 records | OneLake Silver |

**Simulation Strategy:**
```python
def generate_commodity_prices(days=365):
    """Generate crude and product price time series"""
    data = []
    brent_price = 80.0
    wti_price = 75.0

    for day in range(days):
        current_date = datetime.now() - timedelta(days=days-day)

        # Correlated random walks
        shock = np.random.normal(0, 0.02)
        brent_price *= (1 + shock + np.random.normal(0, 0.005))
        wti_price *= (1 + shock * 0.9 + np.random.normal(0, 0.005))

        data.append({
            'date': current_date,
            'brent_close': brent_price,
            'wti_close': wti_price,
            'brent_wti_spread': brent_price - wti_price,
            'gasoline_crack': np.random.uniform(15, 35),
            'diesel_crack': np.random.uniform(20, 40)
        })

    return pd.DataFrame(data)
```

### 5. Trade Finance Documents

| Data Source | Format | Frequency | Volume | Storage |
|-------------|--------|-----------|--------|---------|
| Letters of Credit | PDF/SWIFT MT700 | On-demand | ~20/week | OneLake Bronze + Blob |
| Bills of Lading | PDF | On-shipment | ~50/week | Blob Storage |
| Commercial Invoices | PDF/XML | On-trade | ~100/week | OneLake Bronze |
| Vessel Tracking | AIS JSON | Real-time | Continuous | Real-Time Intelligence |

## Storage Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        STORAGE ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     MICROSOFT FABRIC - OneLake                        │   │
│  │                                                                       │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ BRONZE LAYER (Raw)                                              │  │   │
│  │  │ Format: Delta Lake (Parquet)                                    │  │   │
│  │  │ Retention: 7 years                                              │  │   │
│  │  │ Contents:                                                       │  │   │
│  │  │   • raw_bank_statements     • raw_fx_rates                     │  │   │
│  │  │   • raw_sap_gl_entries      • raw_payments                     │  │   │
│  │  │   • raw_swift_messages      • raw_commodity_prices             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                       │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ SILVER LAYER (Cleaned & Conformed)                              │  │   │
│  │  │ Format: Delta Lake (Parquet)                                    │  │   │
│  │  │ Retention: 5 years                                              │  │   │
│  │  │ Contents:                                                       │  │   │
│  │  │   • cash_transactions       • fx_positions                     │  │   │
│  │  │   • payment_history         • counterparty_master              │  │   │
│  │  │   • commodity_prices        • trade_finance_docs               │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                       │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ GOLD LAYER (Business-Ready)                                     │  │   │
│  │  │ Format: Delta Lake (Parquet)                                    │  │   │
│  │  │ Retention: 3 years                                              │  │   │
│  │  │ Contents:                                                       │  │   │
│  │  │   • daily_cash_position     • cash_forecast                    │  │   │
│  │  │   • fx_exposure_summary     • risk_metrics                     │  │   │
│  │  │   • payment_analytics       • kpis                             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │ REAL-TIME INTELLIGENCE (KQL Database)                              │     │
│  │ • fx_rates_stream         • payment_events_stream                 │     │
│  │ • commodity_prices_stream • alerts_stream                         │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │ AZURE BLOB STORAGE (Documents)                                     │     │
│  │ • LC Documents (PDF)      • Bills of Lading (PDF)                 │     │
│  │ • Policy Documents        • Reports Archive                       │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │ AZURE AI SEARCH (Vector Index)                                     │     │
│  │ • Policy document embeddings                                      │     │
│  │ • Historical query embeddings                                     │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Simulation Master Script

```python
"""
Treasury Data Simulation Master Script
Generates all required datasets for development and testing
"""

import os
import pandas as pd
from datetime import datetime

# Configuration
OUTPUT_DIR = "./simulated_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate all datasets
print("Generating Treasury simulation data...")

# 1. Cash Flows
cash_flows = generate_cash_flows(days=365, accounts=10)
cash_flows.to_parquet(f"{OUTPUT_DIR}/cash_flows.parquet")
print(f"  - Cash flows: {len(cash_flows)} records")

# 2. FX Rates
fx_rates = generate_fx_rates(hours=720)
fx_rates.to_parquet(f"{OUTPUT_DIR}/fx_rates.parquet")
print(f"  - FX rates: {len(fx_rates)} records")

# 3. Payments
payments = generate_payments(days=90, daily_count=100)
payments.to_parquet(f"{OUTPUT_DIR}/payments.parquet")
print(f"  - Payments: {len(payments)} records")

# 4. Commodity Prices
commodities = generate_commodity_prices(days=365)
commodities.to_parquet(f"{OUTPUT_DIR}/commodity_prices.parquet")
print(f"  - Commodity prices: {len(commodities)} records")

# 5. Generate summary statistics
print("\nData Summary:")
print(f"  Total cash flow volume: ${cash_flows['amount'].sum():,.0f}")
print(f"  Anomaly rate in payments: {payments['is_anomaly'].mean()*100:.1f}%")
print(f"  FX rate range USD/TRY: {fx_rates[fx_rates['currency_pair']=='USD/TRY']['mid'].min():.2f} - {fx_rates[fx_rates['currency_pair']=='USD/TRY']['mid'].max():.2f}")

print("\nSimulation complete!")
```

## Data Quality Checklist

| Check | Bronze | Silver | Gold |
|-------|--------|--------|------|
| Schema validation | Required | Required | Required |
| Null handling | Log only | Replace/Filter | No nulls |
| Duplicates | Log only | Remove | No duplicates |
| Date validation | Check format | Validate range | Validated |
| Amount validation | Check numeric | Check sign/range | Validated |
| Referential integrity | Not checked | Soft check | Enforced |

## Prototype Space

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROTOTYPE: Data Simulation                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Status: [ ] Not Started  [ ] In Progress  [ ] Complete                     │
│                                                                              │
│  Components:                                                                 │
│  [ ] Create Python simulation package                                       │
│  [ ] Generate 1 year of cash flow data                                      │
│  [ ] Generate FX rate time series                                           │
│  [ ] Generate payment data with anomalies                                   │
│  [ ] Generate commodity price data                                          │
│  [ ] Load to Fabric OneLake (Bronze layer)                                  │
│  [ ] Create Silver layer transformations                                    │
│  [ ] Create Gold layer aggregations                                         │
│                                                                              │
│  Notes:                                                                      │
│  _________________________________________________________________________  │
│  _________________________________________________________________________  │
│  _________________________________________________________________________  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```
