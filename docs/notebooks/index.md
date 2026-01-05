# Educational Notebooks

## Overview

This collection of Jupyter notebooks provides hands-on, educational demonstrations of AI/ML applications for Treasury operations in the Oil & Gas sector. Each notebook is designed to be self-contained, with detailed explanations, thinking traces, and executive dashboards.

!!! info "Educational Purpose"
    These notebooks use **simulated data** that mimics real-world patterns. They are designed for learning and demonstration purposes, showcasing how AI/ML techniques can be applied to Treasury challenges.

## Notebook Collection

| # | Notebook | Primary Technique | Business Value |
|---|----------|-------------------|----------------|
| 01 | [Cash Flow Forecasting](01-cash-flow-forecasting.md) | Prophet, Time Series | Liquidity planning, funding optimization |
| 02 | [Fraud Detection](02-fraud-detection.md) | Isolation Forest + Rules | Payment security, loss prevention |
| 03 | [FX Risk Management](03-fx-risk-management.md) | Monte Carlo Simulation | Hedge optimization, exposure control |
| 04 | [Commodity Hedging](04-commodity-hedging.md) | ARIMA Forecasting | Margin protection, hedge timing |
| 05 | [Trade Finance](05-trade-finance.md) | Document AI, NER | Processing efficiency, compliance |
| 06 | [Working Capital](06-working-capital.md) | Random Forest | Collection optimization, DSO reduction |
| 07 | [Treasury Copilot](07-treasury-copilot.md) | RAG, LLM | Self-service analytics, policy Q&A |
| 08 | [Compliance (TAS 29)](08-compliance.md) | ML Classification | Hyperinflation accounting automation |

## Architecture

```
treasury/
├── notebooks/                    # Jupyter notebooks
│   ├── 01_cash_flow_forecasting.ipynb
│   ├── 02_fraud_detection.ipynb
│   ├── 03_fx_risk_management.ipynb
│   ├── 04_commodity_hedging.ipynb
│   ├── 05_trade_finance.ipynb
│   ├── 06_working_capital.ipynb
│   ├── 07_treasury_copilot.ipynb
│   └── 08_compliance.ipynb
│
└── src/treasury_sim/            # Data simulation package
    ├── __init__.py
    └── generators.py            # 9 data generators
```

## Design Principles

### 1. Thinking Traces
Each notebook includes **"Thinking Trace"** sections that explain:

- Why we chose a particular approach
- What business questions we're answering
- Trade-offs between different methods
- Limitations and considerations

### 2. Progressive Complexity
Notebooks start with simple concepts and gradually introduce complexity:

```
Basic EDA → Baseline Models → Advanced ML → Business Application
```

### 3. Executive Dashboards
Every notebook concludes with a **Plotly-based dashboard** suitable for presenting to business stakeholders, combining multiple visualizations into a cohesive view.

### 4. Realistic Data Patterns
The simulated data includes real-world patterns:

- **Seasonality**: Month-end spikes, quarterly patterns
- **Anomalies**: Fraud indicators, unusual transactions
- **Correlations**: Oil-USD relationships, crack spreads
- **Business Rules**: Payment terms, credit ratings

## Getting Started

### Prerequisites

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Notebooks

```bash
# Start Jupyter
jupyter notebook notebooks/

# Or use JupyterLab
jupyter lab notebooks/
```

### Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | ≥2.0.0 | Data manipulation |
| numpy | ≥1.24.0 | Numerical computing |
| plotly | ≥5.15.0 | Interactive visualizations |
| scikit-learn | ≥1.3.0 | ML algorithms |
| statsmodels | ≥0.14.0 | Statistical models (ARIMA) |
| prophet | ≥1.1.0 | Time series forecasting |

## Data Simulation Package

The `src/treasury_sim/generators.py` module provides functions to generate realistic Treasury data:

| Generator | Output | Use Case |
|-----------|--------|----------|
| `generate_cash_flows()` | Daily cash movements | Cash forecasting |
| `generate_daily_cash_position()` | Bank balances | Liquidity analysis |
| `generate_fx_rates()` | Currency pairs | FX risk |
| `generate_fx_exposures()` | Open positions | Hedge planning |
| `generate_payments()` | Payment transactions | Fraud detection |
| `generate_commodity_prices()` | Oil/product prices | Hedging |
| `generate_counterparties()` | Customer/supplier data | Credit analysis |
| `generate_bank_accounts()` | Account structure | Cash pooling |
| `generate_trade_documents()` | LC/invoice data | Trade finance |

[Learn more about the Data Generators →](data-generators.md)

## Learning Path

We recommend following the notebooks in order for a progressive learning experience:

```mermaid
graph LR
    A[01 Cash Flow] --> B[02 Fraud]
    B --> C[03 FX Risk]
    C --> D[04 Commodity]
    D --> E[05 Trade Finance]
    E --> F[06 Working Capital]
    F --> G[07 Copilot]
    G --> H[08 Compliance]
```

However, each notebook is self-contained and can be explored independently based on your interest area.

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
