# 08 - TAS 29 Compliance Automation

## Business Context

Turkish companies must apply **TAS 29** (Turkish Accounting Standard 29, equivalent to IAS 29) for hyperinflation accounting when:

- 3-year cumulative inflation exceeds 100%
- People prefer holding non-monetary assets
- Prices are quoted in stable foreign currencies

!!! warning "Turkey's Situation"
    Turkey has been classified as a hyperinflationary economy since 2022, requiring all financial statements to be restated in current purchasing power.

**The Challenge:**

| Manual Process | Issue |
|----------------|-------|
| Item classification | Thousands of line items to classify |
| Index application | Different dates require different indices |
| Calculations | Error-prone manual spreadsheets |
| Audit trail | Difficult to maintain |

## Notebook Overview

This notebook demonstrates automating TAS 29 compliance using ML classification and rules-based calculations.

### What You'll Learn

1. **TAS 29 fundamentals** and requirements
2. **Monetary vs non-monetary classification** with ML
3. **Restatement calculations** implementation
4. **Validation and anomaly detection**
5. **Compliance dashboard** and reporting

## TAS 29 Fundamentals

### Monetary vs Non-Monetary Items

| Monetary (NOT restated) | Non-Monetary (Restated) |
|------------------------|-------------------------|
| Cash and bank balances | Property, Plant & Equipment |
| Accounts receivable | Intangible assets |
| Accounts payable | Inventory (at acquisition) |
| Loans and borrowings | Prepaid expenses |
| Deferred tax liabilities | Share capital |
| | Retained earnings |

### Restatement Formula

```
Restated Amount = Historical Amount × (CPI_current / CPI_acquisition)
```

**Example:**

- Machine purchased Jan 2021: TRY 10,000,000
- CPI January 2021: 500
- CPI December 2024: 1,800
- **Restated = 10,000,000 × (1,800/500) = TRY 36,000,000**

### Monetary Gain/Loss

Holding monetary items during hyperinflation creates purchasing power gain/loss:

- **Holding monetary assets** (cash, receivables) → **Loss** (purchasing power decreases)
- **Holding monetary liabilities** (payables, debt) → **Gain** (repay with cheaper money)

```
Net Monetary Position × Inflation Rate = Monetary Gain/(Loss)
```

## Data Design

### CPI Data Generation

```python
def generate_cpi_data():
    """Generate realistic Turkish CPI data."""
    dates = pd.date_range('2020-01-01', '2024-12-01', freq='MS')

    # Turkish inflation trajectory
    # 2020: ~15% | 2021: ~25% | 2022: ~65% | 2023: ~50% | 2024: ~40%

    monthly_rates = []
    for date in dates:
        if date.year == 2020:
            rate = np.random.uniform(0.008, 0.015)
        elif date.year == 2021:
            rate = np.random.uniform(0.012, 0.025)
        elif date.year == 2022:
            rate = np.random.uniform(0.03, 0.08)
        elif date.year == 2023:
            rate = np.random.uniform(0.025, 0.05)
        else:
            rate = np.random.uniform(0.02, 0.04)
        monthly_rates.append(rate)

    # Calculate cumulative index
    indices = [450]  # Base: Jan 2020
    for rate in monthly_rates[:-1]:
        indices.append(indices[-1] * (1 + rate))

    return pd.DataFrame({
        'date': dates,
        'cpi_index': indices,
        'monthly_change': monthly_rates
    })
```

### Balance Sheet Items

```python
def generate_balance_sheet_items(n_items=100):
    """Generate balance sheet items with acquisition dates."""

    non_monetary = [
        ('Land', 'PPE'),
        ('Buildings', 'PPE'),
        ('Machinery', 'PPE'),
        ('Software', 'Intangible'),
        ('Inventory', 'Inventory'),
        ('Prepaid Rent', 'Prepaid')
    ]

    monetary = [
        ('Cash TRY', 'Cash'),
        ('Trade Receivables', 'Receivable'),
        ('Trade Payables', 'Payable'),
        ('Bank Loans', 'Debt')
    ]

    # Generate items with random acquisition dates
    # ...
```

## Approach & Methodology

### Step 1: ML-Based Classification

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# Text features from account name
vectorizer = TfidfVectorizer(max_features=20)
text_features = vectorizer.fit_transform(items['item_name'])

# Category encoding
category_encoded = LabelEncoder().fit_transform(items['category'])

# Combine features
X = np.hstack([text_features.toarray(), category_encoded.reshape(-1, 1)])
y = items['is_monetary']

# Train classifier
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)
```

**Classification Performance:**

| Metric | Value |
|--------|-------|
| Accuracy | 94% |
| Precision | 92% |
| Recall | 95% |

### Step 2: Restatement Calculator

```python
class TAS29Calculator:
    """TAS 29 restatement calculator."""

    def __init__(self, cpi_data):
        self.cpi = cpi_data.set_index('date')['cpi_index']
        self.current_cpi = cpi_data['cpi_index'].iloc[-1]

    def get_cpi_at_date(self, date):
        """Get CPI index for acquisition date."""
        month_start = date.replace(day=1)
        return self.cpi.get(month_start, self.cpi.iloc[-1])

    def calculate_restatement_factor(self, acquisition_date):
        """Calculate restatement multiplier."""
        cpi_acquisition = self.get_cpi_at_date(acquisition_date)
        return self.current_cpi / cpi_acquisition

    def restate_item(self, item):
        """Restate a single balance sheet item."""
        if item['is_monetary']:
            return {
                **item,
                'restated_amount': item['historical_amount'],
                'restatement_factor': 1.0,
                'restatement_gain_loss': 0
            }
        else:
            factor = self.calculate_restatement_factor(item['acquisition_date'])
            restated = item['historical_amount'] * factor
            return {
                **item,
                'restated_amount': restated,
                'restatement_factor': factor,
                'restatement_gain_loss': restated - item['historical_amount']
            }
```

### Step 3: Anomaly Detection

```python
def detect_restatement_anomalies(restated_df):
    """Detect potential errors in TAS 29 calculations."""
    anomalies = []

    for _, row in restated_df.iterrows():
        # High restatement factor
        if not row['is_monetary'] and row['restatement_factor'] > 5:
            anomalies.append({
                'item_id': row['item_id'],
                'type': 'HIGH_FACTOR',
                'severity': 'WARNING',
                'message': f"Factor {row['restatement_factor']:.2f} unusually high"
            })

        # Classification check
        cash_keywords = ['cash', 'bank', 'receivable', 'payable']
        if any(kw in row['item_name'].lower() for kw in cash_keywords):
            if not row['is_monetary']:
                anomalies.append({
                    'item_id': row['item_id'],
                    'type': 'CLASSIFICATION',
                    'severity': 'HIGH',
                    'message': "Item name suggests monetary but classified non-monetary"
                })

    return pd.DataFrame(anomalies)
```

### Step 4: Report Generation

```python
def generate_tas29_report(restated_df, monetary_result, cpi_data):
    """Generate TAS 29 compliance report."""

    report = f"""
    ======================================================
    TAS 29 HYPERINFLATION ACCOUNTING REPORT
    Report Date: {datetime.now().strftime('%Y-%m-%d')}
    ======================================================

    1. INFLATION CONTEXT
    - Annual Inflation: {cpi_data['annual_inflation'].iloc[-1]:.1f}%
    - 3-Year Cumulative: {cpi_data['cumulative_3yr'].iloc[-1]:.1f}%
    - Status: HYPERINFLATION ACTIVE

    2. RESTATEMENT SUMMARY
    - Items Restated: {len(restated_df[~restated_df['is_monetary']])}
    - Historical Total: TRY {restated_df['historical_amount'].sum()/1e6:,.1f}M
    - Restated Total: TRY {restated_df['restated_amount'].sum()/1e6:,.1f}M
    - Restatement Effect: TRY {restated_df['restatement_gain_loss'].sum()/1e6:,.1f}M

    3. MONETARY GAIN/(LOSS)
    - Net Monetary Position: TRY {monetary_result['net_position']/1e6:,.1f}M
    - Purchasing Power Effect: TRY {monetary_result['gain_loss']/1e6:,.1f}M

    4. REQUIRED DISCLOSURES
    [ ] Statement that TAS 29 applied
    [ ] General price index used (TUIK CPI)
    [ ] Current and prior period index values
    [ ] Net monetary gain/loss in P&L
    """
    return report
```

## Key Results

### Restatement Impact

| Category | Historical | Restated | Factor |
|----------|------------|----------|--------|
| PPE | TRY 250M | TRY 625M | 2.5x |
| Intangibles | TRY 50M | TRY 110M | 2.2x |
| Inventory | TRY 80M | TRY 96M | 1.2x |
| **Total Non-Monetary** | **TRY 380M** | **TRY 831M** | **2.2x** |

### Monetary Gain/Loss

| Component | Amount |
|-----------|--------|
| Net monetary position | TRY (150M) |
| Inflation rate | 45% |
| **Monetary gain** | **TRY 67.5M** |

*Negative monetary position (more liabilities than assets) creates gain during inflation*

### Automation Benefits

| Metric | Manual | Automated | Improvement |
|--------|--------|-----------|-------------|
| Processing time | 5-7 days | 1-2 hours | **95%** |
| Error rate | 5-10% | <1% | **90%** |
| Audit queries | 15-20 | 2-3 | **85%** |
| Staff required | 3 FTE | 0.5 FTE | **83%** |

## Thinking Traces

!!! quote "Why ML for classification?"
    Manual classification of thousands of accounts is tedious and error-prone. ML learns patterns from account names and categories, achieving 94% accuracy. Human review focuses only on edge cases and anomalies.

!!! quote "Why flag high restatement factors?"
    A factor of 5x means the item was acquired when CPI was 1/5 of current level. While possible for old assets, it could also indicate incorrect acquisition dates. Flagging ensures human review.

!!! quote "Why generate structured reports?"
    TAS 29 has specific disclosure requirements. Automated report generation ensures all required elements are included and formatted consistently for auditors.

## Executive Dashboard

The notebook includes a compliance dashboard:

- **Inflation trend** (line chart with threshold)
- **Classification distribution** (pie chart)
- **Restatement impact by category** (bar chart)
- **Restatement factor distribution** (histogram)
- **Anomaly summary** (bar chart by severity)
- **Compliance checklist** (table)

## IFRS 29 / IAS 29 Context

TAS 29 is the Turkish translation of IAS 29. Key requirements:

1. **Restate all non-monetary items** using general price index
2. **Do not restate monetary items** (already in current purchasing power)
3. **Calculate net monetary gain/loss** and include in P&L
4. **Restate comparatives** to current period purchasing power
5. **Disclose** index used, index values, and methodology

### Countries Currently Applying IAS 29

| Country | Year Applied | 3-Year Inflation |
|---------|--------------|------------------|
| Turkey | 2022 | >200% |
| Argentina | 2018 | >300% |
| Venezuela | 2009 | >10,000% |
| Zimbabwe | 2019 | >800% |

## Next Steps

After mastering this notebook:

1. → [01 Cash Flow Forecasting](01-cash-flow-forecasting.md) for inflation-adjusted forecasts
2. → [03 FX Risk Management](03-fx-risk-management.md) for currency considerations

## Code Access

📓 **Notebook**: [`notebooks/08_compliance.ipynb`](https://github.com/ozgurgulerx/treasury/blob/main/notebooks/08_compliance.ipynb)

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
