# 05 - Trade Finance Automation

## Business Context

Oil & Gas refiners process hundreds of trade documents for crude imports:

- **Letters of Credit (LCs)**: Bank payment guarantees
- **Bills of Lading**: Shipping proof documents
- **Commercial Invoices**: Pricing and quantity details
- **Certificates**: Origin, quality, insurance

!!! danger "The Problem"
    **60-70% of LCs have discrepancies** on first presentation, causing:

    - Payment delays (3-5 days average)
    - Discrepancy fees ($150-500 each)
    - Operational burden (manual review)
    - Cargo demurrage costs

## Notebook Overview

This notebook demonstrates how Document AI and NLP can automate trade finance processing, reducing discrepancies and accelerating payments.

### What You'll Learn

1. **Trade document structure** and UCP 600 requirements
2. **OCR simulation** and field extraction
3. **Cross-document validation** logic
4. **Discrepancy detection** and resolution
5. **Processing time analytics**

## Data Design

### Simulated Dataset

```python
from src.treasury_sim.generators import generate_trade_documents

documents = generate_trade_documents(
    n_transactions=100,  # 100 LC sets
    seed=42
)
```

### Document Types Generated

| Document Type | Key Fields | Validation Rules |
|--------------|------------|------------------|
| **LC** | Amount, expiry, terms | Master document |
| **Invoice** | Amount, goods, quantity | Must not exceed LC |
| **Bill of Lading** | Vessel, ports, quantity | Must match LC terms |
| **Certificate of Origin** | Country, exporter | Must match LC |
| **Quality Certificate** | API gravity, sulfur | Must meet specs |
| **Insurance Certificate** | Coverage, voyage | Must cover shipment |

### Intentional Discrepancies

The generator injects realistic discrepancies:

| Discrepancy Type | Frequency | Severity |
|------------------|-----------|----------|
| Amount mismatch | 8% | High |
| Quantity variance | 12% | Medium |
| Description difference | 5% | High |
| Date issues | 3% | High |
| Party name mismatch | 7% | Medium |

## Approach & Methodology

### Step 1: Document Extraction (OCR Simulation)

```python
class DocumentExtractor:
    """
    Simulates OCR and field extraction.
    In production: Azure Form Recognizer, AWS Textract
    """

    def extract(self, document):
        extracted_fields = {}

        for field in self.field_definitions[document.type]:
            value = self._extract_field(document, field)
            confidence = self._calculate_confidence(field)

            extracted_fields[field] = {
                'value': value,
                'confidence': confidence
            }

        return extracted_fields
```

**Confidence Thresholds:**

| Confidence | Action | Example |
|------------|--------|---------|
| > 95% | Auto-accept | Clear printed numbers |
| 80-95% | Review flag | Handwritten amounts |
| < 80% | Manual entry | Poor scan quality |

### Step 2: Validation Rules Engine

```python
class DocumentValidator:
    """
    Validates documents against LC requirements (UCP 600).
    """

    def __init__(self):
        self.rules = [
            ('amount_match', self._check_amount_match),
            ('quantity_tolerance', self._check_quantity_tolerance),
            ('goods_description', self._check_goods_description),
            ('date_validity', self._check_date_validity),
            ('currency_match', self._check_currency_match)
        ]

    def _check_amount_match(self, docs):
        """Invoice amount must not exceed LC amount"""
        lc_amount = docs['LC']['amount']
        invoice_amount = docs['INVOICE']['amount']

        if invoice_amount > lc_amount:
            return {
                'rule': 'amount_match',
                'severity': 'HIGH',
                'message': f'Invoice exceeds LC by ${invoice_amount - lc_amount:,.0f}'
            }
        return None
```

**Key UCP 600 Rules:**

| Rule | Requirement | Tolerance |
|------|-------------|-----------|
| Amount | Invoice ≤ LC | 0% |
| Quantity | B/L = Invoice | ±5% |
| Description | Exact match | None |
| Dates | Within validity | None |
| Parties | Exact names | None |

### Step 3: Discrepancy Resolution

```python
class DiscrepancyResolver:
    """
    AI-powered resolution recommendations.
    """

    resolution_patterns = {
        'amount_match': {
            'action': 'REQUEST_AMENDMENT',
            'template': 'Request LC amendment to ${amount}',
            'avg_days': 3,
            'cost': 350
        },
        'quantity_tolerance': {
            'action': 'NEGOTIATE_TOLERANCE',
            'template': 'Request acceptance under +/- 5% clause',
            'avg_days': 1,
            'cost': 150
        }
        # ... more patterns
    }

    def recommend(self, discrepancy):
        pattern = self.resolution_patterns[discrepancy['rule']]
        return {
            'action': pattern['action'],
            'estimated_days': pattern['avg_days'],
            'estimated_cost': pattern['cost']
        }
```

### Step 4: Processing Time Analysis

Compare manual vs AI-assisted processing:

| Process Step | Manual | AI-Assisted | Savings |
|--------------|--------|-------------|---------|
| Document receipt | 8 hours | 0.5 hours | 94% |
| OCR/digitization | 3 hours | 3 minutes | 98% |
| Field extraction | 2 hours | 10 seconds | 99% |
| Cross-validation | 3 hours | 10 seconds | 99% |
| Discrepancy ID | 1.5 hours | Instant | 99% |
| **Total** | **18.5 hours** | **~1 hour** | **95%** |

## Key Results

### Validation Performance

| Metric | Value |
|--------|-------|
| Total transactions | 100 |
| First-pass compliant | 42% |
| With discrepancies | 58% |
| Auto-resolvable | 35% |

### Discrepancy Distribution

| Type | Count | Severity |
|------|-------|----------|
| Amount mismatch | 15 | High |
| Quantity variance | 22 | Medium |
| Goods description | 8 | High |
| Date issues | 5 | High |
| Currency mismatch | 8 | Medium |

### Cost Impact

| Metric | Manual | AI-Assisted |
|--------|--------|-------------|
| Cost per document | $50 | $12 |
| Discrepancy cost | $350 avg | $150 avg |
| Total cost (100 docs) | $5,000 | $1,200 |
| **Annual savings** | - | **$152K** |

## Thinking Traces

!!! quote "Why rules + ML, not just ML?"
    Trade finance has strict legal requirements (UCP 600). Rules ensure compliance with these non-negotiable standards. ML helps with fuzzy matching (goods descriptions) and confidence scoring, but rules provide the compliance backbone.

!!! quote "Why simulate OCR instead of using real OCR?"
    1. Real OCR APIs have costs and rate limits
    2. We control the data patterns for educational purposes
    3. The validation and resolution logic is the focus
    4. Production deployment would swap in Azure Form Recognizer

!!! quote "Why is 60-70% discrepancy rate realistic?"
    Industry studies (ICC Trade Finance Survey) consistently show 60-70% first-presentation rejection rates. Common causes: typos, date errors, description mismatches. AI can catch these before submission.

## Executive Dashboard

The notebook includes an operations dashboard:

- **Document volume by type** (pie chart)
- **Compliance rate gauge** (target: 50%+)
- **Processing funnel** (received → approved)
- **Discrepancy trend** (declining with AI)
- **Cost savings** (monthly trend)
- **SLA performance** (% within target time)

## Business Application

### Integration Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Document       │────▶│  AI Processing  │────▶│  Trade Finance  │
│  Ingestion      │     │  Engine         │     │  System (TMS)   │
│  (Email/Portal) │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
           ┌─────────────────┐       ┌─────────────────┐
           │  Auto-Approve   │       │  Discrepancy    │
           │  Queue          │       │  Workbench      │
           └─────────────────┘       └─────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| OCR | Azure Form Recognizer | Document digitization |
| NER | Custom BERT model | Field extraction |
| Validation | Rules engine | UCP 600 compliance |
| Matching | Fuzzy matching | Description comparison |
| Workflow | Power Automate | Process orchestration |

## Next Steps

After mastering this notebook:

1. → [06 Working Capital](06-working-capital.md) for AR/AP from trade
2. → [02 Fraud Detection](02-fraud-detection.md) for payment security

## Code Access

📓 **Notebook**: [`notebooks/05_trade_finance.ipynb`](https://github.com/ozgurgulerx/treasury/blob/main/notebooks/05_trade_finance.ipynb)

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
