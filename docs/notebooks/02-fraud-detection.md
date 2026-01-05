# 02 - Fraud Detection

## Business Context

Payment fraud is a critical risk for Treasury operations. Oil & Gas companies are particularly vulnerable due to:

- **High-value transactions**: Single payments can exceed $100M
- **Complex supply chains**: Multiple intermediaries and jurisdictions
- **Time pressure**: Crude cargoes require rapid payment
- **Sophisticated attackers**: Business Email Compromise (BEC) targeting energy sector

!!! danger "The Risk"
    Average BEC fraud loss in energy sector: **$5.3M per incident** (FBI IC3 Report)

## Notebook Overview

This notebook builds a hybrid fraud detection system combining rule-based heuristics with machine learning anomaly detection.

### What You'll Learn

1. **Payment data patterns** and fraud indicators
2. **Rule-based detection** with business logic
3. **Isolation Forest** for anomaly detection
4. **Hybrid scoring** combining both approaches
5. **Alert management** dashboard design

## Data Design

### Simulated Dataset

The `generate_payments()` function creates payment data with intentional anomalies:

```python
from src.treasury_sim.generators import generate_payments

payments = generate_payments(
    days=90,              # 3 months history
    daily_count=50,       # ~50 payments/day
    anomaly_rate=0.02,    # 2% anomalous
    seed=42
)
```

### Injected Anomaly Types

| Anomaly Type | Simulation Method | Real-World Example |
|--------------|-------------------|-------------------|
| **Large amount** | 10x normal | Inflated invoice |
| **Unusual time** | Outside 9-5 | After-hours fraud |
| **New beneficiary** | Random new account | Account takeover |
| **Round amount** | Exact millions | Fictitious payment |
| **High-risk country** | Sanctioned jurisdictions | Sanctions evasion |

### Data Structure

| Column | Type | Description |
|--------|------|-------------|
| `payment_id` | string | Unique identifier |
| `timestamp` | datetime | Payment initiation time |
| `amount` | float | Payment amount |
| `currency` | string | Payment currency |
| `beneficiary_id` | string | Recipient identifier |
| `beneficiary_country` | string | Recipient country |
| `payment_type` | string | WIRE, ACH, SWIFT |
| `is_anomaly` | bool | Ground truth label |
| `anomaly_type` | string | Type of anomaly (if any) |

## Approach & Methodology

### Step 1: Rule-Based Detection

Business rules encode domain expertise:

```python
class FraudRuleEngine:
    def __init__(self):
        self.rules = [
            ('large_amount', self._check_large_amount),
            ('unusual_hour', self._check_unusual_hour),
            ('high_risk_country', self._check_high_risk_country),
            ('new_beneficiary', self._check_new_beneficiary),
            ('round_amount', self._check_round_amount)
        ]
```

**Rule Definitions:**

| Rule | Threshold | Score |
|------|-----------|-------|
| Large Amount | > $5M or > 3σ from mean | 30 |
| Unusual Hour | Before 7am or after 7pm | 20 |
| High-Risk Country | Sanctioned list | 40 |
| New Beneficiary | First-time recipient | 15 |
| Round Amount | Exact millions | 10 |

### Step 2: Isolation Forest

Isolation Forest detects anomalies by measuring how easily a point can be isolated:

```python
from sklearn.ensemble import IsolationForest

# Feature engineering
features = ['amount_log', 'hour', 'day_of_week',
            'beneficiary_frequency', 'amount_vs_avg']

model = IsolationForest(
    n_estimators=100,
    contamination=0.02,  # Expected anomaly rate
    random_state=42
)

# Train on historical data
model.fit(X_train)

# Score new payments (-1 = anomaly, 1 = normal)
anomaly_scores = model.decision_function(X_test)
```

**Why Isolation Forest?**

- **Unsupervised**: No labeled fraud data required
- **Efficient**: O(n log n) complexity
- **Interpretable**: Anomaly score is intuitive
- **Robust**: Works well with high-dimensional data

### Step 3: Hybrid Scoring

Combine rule-based and ML scores:

```python
def calculate_hybrid_score(payment, rule_score, ml_score):
    """
    Combine rule-based and ML scores with weighted average.

    - Rule score: 0-100 (sum of triggered rules)
    - ML score: -1 to 1 (Isolation Forest decision function)
    """
    # Normalize ML score to 0-100
    ml_normalized = (1 - ml_score) * 50  # More negative = higher risk

    # Weighted combination
    hybrid = 0.4 * rule_score + 0.6 * ml_normalized

    return min(hybrid, 100)
```

**Alert Thresholds:**

| Score Range | Alert Level | Action |
|-------------|-------------|--------|
| 0-30 | Low | Auto-approve |
| 31-60 | Medium | Queue for review |
| 61-80 | High | Immediate review |
| 81-100 | Critical | Block + escalate |

### Step 4: Performance Evaluation

**Confusion Matrix Analysis:**

```
                    Predicted
                 Normal  | Anomaly
Actual  Normal  |  TN    |   FP   |  → False Positive Rate
        Anomaly |  FN    |   TP   |  → Detection Rate
```

**Key Metrics:**

| Metric | Formula | Target |
|--------|---------|--------|
| Precision | TP / (TP + FP) | > 80% |
| Recall | TP / (TP + FN) | > 95% |
| F1 Score | 2 × (P × R) / (P + R) | > 85% |

## Key Results

### Detection Performance

| Method | Precision | Recall | F1 Score |
|--------|-----------|--------|----------|
| Rules Only | 72% | 85% | 78% |
| ML Only | 68% | 92% | 78% |
| **Hybrid** | **81%** | **94%** | **87%** |

### Feature Importance (Isolation Forest)

| Feature | Importance | Interpretation |
|---------|------------|----------------|
| amount_log | 0.35 | Unusual amounts most predictive |
| beneficiary_frequency | 0.25 | New beneficiaries suspicious |
| hour | 0.18 | Time of day matters |
| amount_vs_avg | 0.15 | Deviation from pattern |
| day_of_week | 0.07 | Weekend payments unusual |

## Thinking Traces

!!! quote "Why hybrid over pure ML?"
    Pure ML models can miss obvious fraud patterns that simple rules catch easily (e.g., payments to sanctioned countries). Conversely, rules alone miss novel fraud patterns. The hybrid approach captures both known patterns (rules) and unknown anomalies (ML).

!!! quote "Why 0.02 contamination?"
    Industry benchmarks suggest 1-3% of corporate payments have fraud indicators. Setting contamination to 2% balances sensitivity with false positive management. Too low = miss fraud; too high = alert fatigue.

!!! quote "Why weighted 40/60 for hybrid?"
    Rules encode certain knowledge (sanctioned countries are always high risk). ML captures uncertain patterns. We weight ML higher (60%) because it adapts to new patterns, but rules (40%) provide a floor of protection against known threats.

## Executive Dashboard

The notebook includes an alert management dashboard showing:

- **Alert volume** by severity level
- **Detection rate** trend over time
- **False positive rate** monitoring
- **Top triggered rules** analysis
- **Payment flow** sankey diagram

## Business Application

### Integration Points

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Payment    │───▶│   Fraud     │───▶│   Alert     │
│  Initiation │    │   Engine    │    │   Queue     │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                  │
                          ▼                  ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  Auto       │    │  Manual     │
                   │  Approve    │    │  Review     │
                   └─────────────┘    └─────────────┘
```

### Operational Workflow

1. **Real-time scoring**: < 100ms per payment
2. **Queue management**: Priority by risk score
3. **Analyst review**: Context-rich alert cards
4. **Feedback loop**: Analyst decisions retrain model

## Next Steps

After mastering this notebook:

1. → [03 FX Risk Management](03-fx-risk-management.md) to manage currency exposure
2. → [05 Trade Finance](05-trade-finance.md) for document-level fraud detection

## Code Access

📓 **Notebook**: [`notebooks/02_fraud_detection.ipynb`](https://github.com/ozgurgulerx/treasury/blob/main/notebooks/02_fraud_detection.ipynb)

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
