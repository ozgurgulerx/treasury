"""
Treasury Data Generators
========================

Functions to generate realistic synthetic treasury data for development and testing.

Each generator creates pandas DataFrames with realistic patterns, seasonality,
and anomalies that mirror real-world treasury operations.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
import random
import string


def set_seed(seed: int = 42):
    """Set random seed for reproducibility."""
    np.random.seed(seed)
    random.seed(seed)


# =============================================================================
# CASH FLOW DATA GENERATORS
# =============================================================================

def generate_cash_flows(
    days: int = 365,
    n_accounts: int = 5,
    base_date: Optional[datetime] = None,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate realistic cash flow transaction data.

    Simulates:
    - Daily inflows (receivables, interest, refunds)
    - Daily outflows (suppliers, salaries, taxes, utilities)
    - Seasonality (month-end spikes, quarterly patterns)
    - Currency mix (USD, EUR, TRY)

    Parameters:
    -----------
    days : int
        Number of days to generate
    n_accounts : int
        Number of bank accounts
    base_date : datetime, optional
        Start date (defaults to today minus days)
    seed : int
        Random seed for reproducibility

    Returns:
    --------
    pd.DataFrame with columns:
        date, account_id, transaction_id, type, amount, currency,
        category, counterparty, description, is_recurring
    """
    set_seed(seed)

    if base_date is None:
        base_date = datetime.now() - timedelta(days=days)

    data = []
    transaction_id = 1000

    # Define account currencies
    account_currencies = {
        f'ACC_{i:03d}': np.random.choice(['USD', 'EUR', 'TRY'], p=[0.4, 0.3, 0.3])
        for i in range(n_accounts)
    }

    for day_offset in range(days):
        current_date = base_date + timedelta(days=day_offset)
        day_of_month = current_date.day
        day_of_week = current_date.weekday()
        month = current_date.month

        # Skip weekends for most transactions
        is_weekend = day_of_week >= 5

        for account_idx in range(n_accounts):
            account_id = f'ACC_{account_idx:03d}'
            currency = account_currencies[account_id]

            # Month-end effect (more transactions)
            month_end_multiplier = 2.0 if day_of_month >= 25 else 1.0

            # Quarter-end effect
            quarter_end_multiplier = 1.5 if month in [3, 6, 9, 12] and day_of_month >= 20 else 1.0

            # INFLOWS
            if not is_weekend:
                # Customer receivables (larger, less frequent)
                if np.random.random() < 0.3 * month_end_multiplier:
                    amount = np.random.lognormal(mean=12, sigma=1.5)  # ~$150K avg
                    data.append({
                        'date': current_date,
                        'account_id': account_id,
                        'transaction_id': f'TXN_{transaction_id:08d}',
                        'type': 'INFLOW',
                        'amount': round(amount, 2),
                        'currency': currency,
                        'category': 'RECEIVABLE',
                        'counterparty': f'CUST_{np.random.randint(1, 50):03d}',
                        'description': f'Customer payment - Invoice',
                        'is_recurring': False
                    })
                    transaction_id += 1

                # Interest income (small, regular)
                if day_of_month == 1:
                    amount = np.random.uniform(5000, 50000)
                    data.append({
                        'date': current_date,
                        'account_id': account_id,
                        'transaction_id': f'TXN_{transaction_id:08d}',
                        'type': 'INFLOW',
                        'amount': round(amount, 2),
                        'currency': currency,
                        'category': 'INTEREST',
                        'counterparty': 'BANK_INTEREST',
                        'description': 'Monthly interest income',
                        'is_recurring': True
                    })
                    transaction_id += 1

            # OUTFLOWS
            if not is_weekend:
                # Supplier payments (multiple per day)
                n_supplier_payments = int(np.random.poisson(3) * month_end_multiplier)
                for _ in range(n_supplier_payments):
                    amount = np.random.lognormal(mean=10, sigma=1.2)  # ~$20K avg
                    data.append({
                        'date': current_date,
                        'account_id': account_id,
                        'transaction_id': f'TXN_{transaction_id:08d}',
                        'type': 'OUTFLOW',
                        'amount': -round(amount, 2),
                        'currency': currency,
                        'category': 'SUPPLIER',
                        'counterparty': f'SUPP_{np.random.randint(1, 200):03d}',
                        'description': 'Supplier payment',
                        'is_recurring': False
                    })
                    transaction_id += 1

                # Salary payments (end of month)
                if day_of_month == 28:
                    amount = np.random.uniform(500000, 2000000)
                    data.append({
                        'date': current_date,
                        'account_id': account_id,
                        'transaction_id': f'TXN_{transaction_id:08d}',
                        'type': 'OUTFLOW',
                        'amount': -round(amount, 2),
                        'currency': currency,
                        'category': 'SALARY',
                        'counterparty': 'PAYROLL',
                        'description': 'Monthly payroll',
                        'is_recurring': True
                    })
                    transaction_id += 1

                # Tax payments (quarterly)
                if month in [1, 4, 7, 10] and day_of_month == 15:
                    amount = np.random.uniform(100000, 500000) * quarter_end_multiplier
                    data.append({
                        'date': current_date,
                        'account_id': account_id,
                        'transaction_id': f'TXN_{transaction_id:08d}',
                        'type': 'OUTFLOW',
                        'amount': -round(amount, 2),
                        'currency': currency,
                        'category': 'TAX',
                        'counterparty': 'TAX_AUTHORITY',
                        'description': 'Quarterly tax payment',
                        'is_recurring': True
                    })
                    transaction_id += 1

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date').reset_index(drop=True)


def generate_daily_cash_position(
    days: int = 365,
    n_accounts: int = 5,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate daily cash position (balance) data.

    Returns aggregated end-of-day balances per account with opening/closing.
    """
    set_seed(seed)

    base_date = datetime.now() - timedelta(days=days)
    data = []

    # Initialize account balances
    balances = {f'ACC_{i:03d}': np.random.uniform(1_000_000, 10_000_000)
                for i in range(n_accounts)}
    currencies = {f'ACC_{i:03d}': np.random.choice(['USD', 'EUR', 'TRY'])
                  for i in range(n_accounts)}

    for day_offset in range(days):
        current_date = base_date + timedelta(days=day_offset)

        for account_id in balances.keys():
            opening = balances[account_id]

            # Simulate daily movement
            daily_inflow = np.random.lognormal(11, 1) if np.random.random() > 0.3 else 0
            daily_outflow = np.random.lognormal(10.5, 1.2)

            # Add seasonality
            if current_date.day >= 25:  # Month-end
                daily_outflow *= 1.5

            net_change = daily_inflow - daily_outflow
            closing = max(0, opening + net_change)

            data.append({
                'date': current_date,
                'account_id': account_id,
                'currency': currencies[account_id],
                'opening_balance': round(opening, 2),
                'inflows': round(daily_inflow, 2),
                'outflows': round(daily_outflow, 2),
                'closing_balance': round(closing, 2)
            })

            balances[account_id] = closing

    return pd.DataFrame(data)


# =============================================================================
# FX DATA GENERATORS
# =============================================================================

def generate_fx_rates(
    days: int = 365,
    currency_pairs: List[str] = None,
    freq: str = 'D',
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate realistic FX rate time series with volatility clustering.

    Simulates:
    - Random walk with drift
    - Volatility clustering (GARCH-like)
    - Correlation between pairs
    - Bid-ask spreads

    Parameters:
    -----------
    days : int
        Number of days
    currency_pairs : list
        Currency pairs to generate (default: USD/TRY, EUR/TRY, EUR/USD)
    freq : str
        Frequency ('D' for daily, 'H' for hourly)
    seed : int
        Random seed

    Returns:
    --------
    pd.DataFrame with columns:
        timestamp, currency_pair, bid, ask, mid, daily_change_pct
    """
    set_seed(seed)

    if currency_pairs is None:
        currency_pairs = ['USD/TRY', 'EUR/TRY', 'EUR/USD', 'GBP/USD']

    # Base rates and volatilities
    base_rates = {
        'USD/TRY': 34.0,
        'EUR/TRY': 37.0,
        'EUR/USD': 1.08,
        'GBP/USD': 1.27,
        'USD/JPY': 150.0
    }

    volatilities = {
        'USD/TRY': 0.015,   # High volatility emerging market
        'EUR/TRY': 0.016,
        'EUR/USD': 0.005,   # Low volatility major pair
        'GBP/USD': 0.006,
        'USD/JPY': 0.007
    }

    spreads = {
        'USD/TRY': 0.002,
        'EUR/TRY': 0.0025,
        'EUR/USD': 0.0001,
        'GBP/USD': 0.00015,
        'USD/JPY': 0.0002
    }

    base_date = datetime.now() - timedelta(days=days)
    periods = days if freq == 'D' else days * 24

    data = []

    for pair in currency_pairs:
        rate = base_rates.get(pair, 1.0)
        vol = volatilities.get(pair, 0.01)
        spread = spreads.get(pair, 0.001)

        prev_rate = rate

        for i in range(periods):
            if freq == 'D':
                timestamp = base_date + timedelta(days=i)
            else:
                timestamp = base_date + timedelta(hours=i)

            # Volatility clustering
            if i > 0:
                vol_multiplier = 1 + 0.5 * abs(np.random.normal(0, 1))
            else:
                vol_multiplier = 1

            # Random walk
            daily_return = np.random.normal(0.0001, vol * vol_multiplier)
            rate = prev_rate * (1 + daily_return)

            # Add mean reversion for extreme moves
            if abs(rate / base_rates.get(pair, 1.0) - 1) > 0.1:
                rate = rate * 0.99 + base_rates.get(pair, 1.0) * 0.01

            mid = rate
            bid = mid * (1 - spread/2)
            ask = mid * (1 + spread/2)

            daily_change = (rate - prev_rate) / prev_rate * 100 if prev_rate else 0

            data.append({
                'timestamp': timestamp,
                'currency_pair': pair,
                'bid': round(bid, 6),
                'ask': round(ask, 6),
                'mid': round(mid, 6),
                'daily_change_pct': round(daily_change, 4)
            })

            prev_rate = rate

    return pd.DataFrame(data)


def generate_fx_exposures(
    n_exposures: int = 100,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate FX exposure data (forecasted cash flows by currency).
    """
    set_seed(seed)

    data = []
    base_date = datetime.now()

    currencies = ['USD', 'EUR', 'GBP', 'TRY']
    exposure_types = ['RECEIVABLE', 'PAYABLE', 'FORECAST_REVENUE', 'FORECAST_COST']
    entities = [f'ENTITY_{i:02d}' for i in range(1, 6)]

    for i in range(n_exposures):
        maturity_days = np.random.choice([30, 60, 90, 180, 365])
        currency = np.random.choice(currencies, p=[0.4, 0.3, 0.1, 0.2])

        # USD payables (crude purchases) dominate
        if currency == 'USD':
            exp_type = np.random.choice(exposure_types, p=[0.2, 0.6, 0.1, 0.1])
        else:
            exp_type = np.random.choice(exposure_types, p=[0.5, 0.2, 0.2, 0.1])

        if exp_type in ['PAYABLE', 'FORECAST_COST']:
            amount = -np.random.lognormal(15, 1)  # Negative for payables
        else:
            amount = np.random.lognormal(14, 1.2)

        data.append({
            'exposure_id': f'EXP_{i+1:05d}',
            'entity': np.random.choice(entities),
            'currency': currency,
            'exposure_type': exp_type,
            'amount_local': round(amount, 2),
            'maturity_date': base_date + timedelta(days=int(maturity_days)),
            'maturity_bucket': f'{maturity_days}D',
            'is_hedged': np.random.random() > 0.6,
            'hedge_ratio': np.random.uniform(0.5, 1.0) if np.random.random() > 0.6 else 0
        })

    return pd.DataFrame(data)


# =============================================================================
# PAYMENT DATA GENERATORS
# =============================================================================

def generate_payments(
    days: int = 90,
    daily_count: int = 50,
    anomaly_rate: float = 0.02,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate payment transaction data with labeled anomalies.

    Anomaly types:
    - Unusual amount (10x normal)
    - Unusual time (outside business hours)
    - New beneficiary
    - High-risk country
    - Round amount

    Parameters:
    -----------
    days : int
        Number of days
    daily_count : int
        Average payments per day
    anomaly_rate : float
        Proportion of anomalous payments
    seed : int
        Random seed

    Returns:
    --------
    pd.DataFrame with fraud labels and anomaly reasons
    """
    set_seed(seed)

    data = []
    base_date = datetime.now() - timedelta(days=days)

    # Normal beneficiary pool
    beneficiaries = [
        {'name': f'SUPPLIER_{i:03d}', 'country': np.random.choice(['TR', 'US', 'DE', 'GB', 'NL']),
         'account': f'IBAN{i:010d}', 'avg_amount': np.random.lognormal(10, 1)}
        for i in range(200)
    ]

    high_risk_countries = ['RU', 'IR', 'KP', 'SY', 'VE']

    for day_offset in range(days):
        current_date = base_date + timedelta(days=day_offset)

        # Skip weekends
        if current_date.weekday() >= 5:
            continue

        n_payments = np.random.poisson(daily_count)

        for i in range(n_payments):
            is_anomaly = np.random.random() < anomaly_rate
            anomaly_reasons = []

            # Select beneficiary
            if is_anomaly and np.random.random() < 0.3:
                # New/unknown beneficiary
                beneficiary = {
                    'name': f'NEW_VENDOR_{"".join(random.choices(string.ascii_uppercase, k=5))}',
                    'country': np.random.choice(high_risk_countries + ['TR', 'US']),
                    'account': f'IBAN_NEW_{np.random.randint(1000000, 9999999)}',
                    'avg_amount': 50000
                }
                anomaly_reasons.append('NEW_BENEFICIARY')
            else:
                beneficiary = random.choice(beneficiaries)

            # Generate amount
            if is_anomaly and np.random.random() < 0.4:
                amount = beneficiary['avg_amount'] * np.random.uniform(5, 20)
                anomaly_reasons.append('UNUSUAL_AMOUNT')
            else:
                amount = beneficiary['avg_amount'] * np.random.lognormal(0, 0.5)

            # Round amount anomaly
            if is_anomaly and np.random.random() < 0.3:
                amount = round(amount, -4)  # Round to nearest 10000
                if 'UNUSUAL_AMOUNT' not in anomaly_reasons:
                    anomaly_reasons.append('ROUND_AMOUNT')

            # High-risk country
            if beneficiary['country'] in high_risk_countries:
                anomaly_reasons.append('HIGH_RISK_COUNTRY')
                is_anomaly = True

            # Generate timestamp
            if is_anomaly and np.random.random() < 0.2:
                hour = np.random.choice([2, 3, 4, 22, 23])
                anomaly_reasons.append('UNUSUAL_TIME')
            else:
                hour = np.random.randint(9, 18)

            timestamp = current_date.replace(hour=hour, minute=np.random.randint(0, 60))

            data.append({
                'payment_id': f'PAY_{day_offset:03d}_{i:04d}',
                'timestamp': timestamp,
                'amount': round(amount, 2),
                'currency': np.random.choice(['USD', 'EUR', 'TRY'], p=[0.5, 0.3, 0.2]),
                'beneficiary_name': beneficiary['name'],
                'beneficiary_account': beneficiary['account'],
                'beneficiary_country': beneficiary['country'],
                'payment_type': np.random.choice(['SUPPLIER', 'SALARY', 'TAX', 'TRANSFER']),
                'initiated_by': f'USER_{np.random.randint(1, 20):02d}',
                'is_anomaly': is_anomaly,
                'anomaly_reasons': '|'.join(anomaly_reasons) if anomaly_reasons else None,
                'anomaly_score': len(anomaly_reasons) / 5 if anomaly_reasons else 0
            })

    return pd.DataFrame(data)


# =============================================================================
# COMMODITY DATA GENERATORS
# =============================================================================

def generate_commodity_prices(
    days: int = 365,
    commodities: List[str] = None,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate commodity price time series (crude oil, products).

    Simulates:
    - Correlated price movements (Brent, WTI, products)
    - Crack spreads
    - Seasonality (driving season, winter heating)
    - Volatility regimes
    """
    set_seed(seed)

    if commodities is None:
        commodities = ['BRENT', 'WTI', 'GASOLINE', 'DIESEL', 'JET_FUEL']

    base_prices = {
        'BRENT': 80.0,
        'WTI': 75.0,
        'GASOLINE': 2.50,  # per gallon
        'DIESEL': 2.80,
        'JET_FUEL': 2.60
    }

    volatilities = {
        'BRENT': 0.02,
        'WTI': 0.022,
        'GASOLINE': 0.025,
        'DIESEL': 0.023,
        'JET_FUEL': 0.024
    }

    base_date = datetime.now() - timedelta(days=days)
    data = []

    # Track prices for correlation
    prices = {c: base_prices[c] for c in commodities}

    for day_offset in range(days):
        current_date = base_date + timedelta(days=day_offset)
        month = current_date.month

        # Common shock (affects all commodities)
        common_shock = np.random.normal(0, 0.01)

        # Seasonality
        if month in [6, 7, 8]:  # Driving season
            gasoline_seasonal = 0.001
        else:
            gasoline_seasonal = -0.0005

        if month in [11, 12, 1, 2]:  # Winter heating
            diesel_seasonal = 0.0008
        else:
            diesel_seasonal = -0.0003

        for commodity in commodities:
            vol = volatilities[commodity]
            idiosyncratic = np.random.normal(0, vol)

            # Add seasonal effects
            seasonal = 0
            if commodity == 'GASOLINE':
                seasonal = gasoline_seasonal
            elif commodity in ['DIESEL', 'JET_FUEL']:
                seasonal = diesel_seasonal

            # Update price
            daily_return = common_shock * 0.7 + idiosyncratic * 0.3 + seasonal
            prices[commodity] = prices[commodity] * (1 + daily_return)

            # Mean reversion
            base = base_prices[commodity]
            if abs(prices[commodity] / base - 1) > 0.3:
                prices[commodity] = prices[commodity] * 0.98 + base * 0.02

            data.append({
                'date': current_date,
                'commodity': commodity,
                'close': round(prices[commodity], 4),
                'open': round(prices[commodity] * (1 + np.random.uniform(-0.01, 0.01)), 4),
                'high': round(prices[commodity] * (1 + abs(np.random.normal(0, 0.015))), 4),
                'low': round(prices[commodity] * (1 - abs(np.random.normal(0, 0.015))), 4),
                'volume': int(np.random.lognormal(15, 1))
            })

    df = pd.DataFrame(data)

    # Calculate crack spreads
    df_pivot = df.pivot(index='date', columns='commodity', values='close')
    if 'BRENT' in df_pivot.columns and 'GASOLINE' in df_pivot.columns:
        df_pivot['GASOLINE_CRACK'] = df_pivot['GASOLINE'] * 42 - df_pivot['BRENT']  # 42 gal/barrel
    if 'BRENT' in df_pivot.columns and 'DIESEL' in df_pivot.columns:
        df_pivot['DIESEL_CRACK'] = df_pivot['DIESEL'] * 42 - df_pivot['BRENT']

    return df, df_pivot


# =============================================================================
# SUPPORTING DATA GENERATORS
# =============================================================================

def generate_counterparties(n: int = 100, seed: int = 42) -> pd.DataFrame:
    """Generate counterparty master data."""
    set_seed(seed)

    countries = ['TR', 'US', 'DE', 'GB', 'NL', 'FR', 'IT', 'ES', 'AE', 'SG']
    types = ['CUSTOMER', 'SUPPLIER', 'BANK', 'INTERCOMPANY']

    data = []
    for i in range(n):
        cp_type = np.random.choice(types, p=[0.3, 0.5, 0.1, 0.1])
        data.append({
            'counterparty_id': f'CP_{i+1:05d}',
            'name': f'{cp_type[:4]}_{i+1:03d}_LLC',
            'type': cp_type,
            'country': np.random.choice(countries),
            'credit_rating': np.random.choice(['AAA', 'AA', 'A', 'BBB', 'BB', 'B'],
                                              p=[0.05, 0.1, 0.25, 0.35, 0.15, 0.1]),
            'credit_limit': round(np.random.lognormal(14, 1), -3),
            'payment_terms': np.random.choice([30, 45, 60, 90]),
            'is_active': np.random.random() > 0.1
        })

    return pd.DataFrame(data)


def generate_bank_accounts(n: int = 10, seed: int = 42) -> pd.DataFrame:
    """Generate bank account master data."""
    set_seed(seed)

    banks = ['HSBC', 'Citi', 'JPMorgan', 'Deutsche', 'Barclays', 'Garanti', 'Akbank']
    currencies = ['USD', 'EUR', 'TRY', 'GBP']

    data = []
    for i in range(n):
        data.append({
            'account_id': f'ACC_{i:03d}',
            'bank': np.random.choice(banks),
            'currency': np.random.choice(currencies),
            'account_number': f'{"".join(random.choices(string.digits, k=16))}',
            'iban': f'TR{"".join(random.choices(string.digits, k=24))}',
            'account_type': np.random.choice(['OPERATING', 'PAYROLL', 'TAX', 'INVESTMENT']),
            'entity': f'ENTITY_{np.random.randint(1, 5):02d}',
            'is_active': True
        })

    return pd.DataFrame(data)


# =============================================================================
# DOCUMENT DATA GENERATORS
# =============================================================================

def generate_trade_documents(n: int = 50, seed: int = 42) -> pd.DataFrame:
    """Generate trade finance document metadata."""
    set_seed(seed)

    doc_types = ['LC', 'BILL_OF_LADING', 'COMMERCIAL_INVOICE', 'CERTIFICATE_OF_ORIGIN']
    statuses = ['DRAFT', 'SUBMITTED', 'APPROVED', 'DISCREPANT', 'PAID']

    data = []
    base_date = datetime.now() - timedelta(days=180)

    for i in range(n):
        doc_type = np.random.choice(doc_types, p=[0.3, 0.25, 0.3, 0.15])
        days_offset = np.random.randint(0, 180)

        data.append({
            'document_id': f'DOC_{i+1:05d}',
            'document_type': doc_type,
            'reference_number': f'REF_{np.random.randint(100000, 999999)}',
            'counterparty': f'SUPP_{np.random.randint(1, 50):03d}',
            'amount': round(np.random.lognormal(14, 1), 2),
            'currency': np.random.choice(['USD', 'EUR']),
            'issue_date': base_date + timedelta(days=days_offset),
            'expiry_date': base_date + timedelta(days=days_offset + np.random.randint(30, 180)),
            'status': np.random.choice(statuses, p=[0.1, 0.2, 0.4, 0.15, 0.15]),
            'has_discrepancy': np.random.random() < 0.15,
            'vessel_name': f'MV {"".join(random.choices(string.ascii_uppercase, k=8))}' if doc_type == 'BILL_OF_LADING' else None
        })

    return pd.DataFrame(data)
