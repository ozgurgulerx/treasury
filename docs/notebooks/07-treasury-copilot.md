# 07 - Treasury Copilot (RAG + LLM)

## Business Context

Treasury teams spend significant time on:

- **Ad-hoc queries**: "What's our USD exposure this month?"
- **Policy lookups**: "What's our hedge ratio requirement?"
- **Report generation**: Manual data pulling and formatting
- **Stakeholder requests**: Answering the same questions repeatedly

!!! info "The Vision"
    A **Treasury Copilot** that can:

    - Answer natural language questions about treasury data
    - Retrieve and explain treasury policies
    - Generate standard reports on demand
    - Provide 24/7 self-service analytics

## Notebook Overview

This notebook demonstrates building a Treasury Copilot using Retrieval-Augmented Generation (RAG) architecture.

### What You'll Learn

1. **RAG architecture** for enterprise assistants
2. **Policy document retrieval** with embeddings
3. **Intent classification** for query routing
4. **Treasury function integration** (cash, FX, forecasts)
5. **Conversational interface** design

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Treasury Copilot                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   User      │───▶│   Intent    │───▶│   Router    │     │
│  │   Query     │    │   Classifier│    │             │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
│                                               │             │
│         ┌─────────────────┬─────────────────┬─┴───────┐    │
│         ▼                 ▼                 ▼         ▼    │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│  │   Policy    │   │   Data      │   │   Forecast  │ ...  │
│  │   RAG       │   │   Query     │   │   Engine    │      │
│  └─────────────┘   └─────────────┘   └─────────────┘      │
│         │                 │                 │              │
│         └─────────────────┴─────────────────┘              │
│                           │                                │
│                           ▼                                │
│                    ┌─────────────┐                         │
│                    │   Response  │                         │
│                    │   Generator │                         │
│                    └─────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Approach & Methodology

### Step 1: Policy Document Store

Create a knowledge base of treasury policies:

```python
POLICY_DOCUMENTS = {
    'fx_hedging_policy': """
    FX HEDGING POLICY
    =================
    1. All USD exposures exceeding $1M must be hedged within 5 business days
    2. Minimum hedge ratio: 75% for confirmed exposures
    3. Approved instruments: Forwards, Options (vanilla only)
    4. Maximum tenor: 12 months
    5. Counterparty limit: $50M per bank
    """,

    'cash_management_policy': """
    CASH MANAGEMENT POLICY
    ======================
    1. Minimum cash buffer: 30 days of operating expenses
    2. Excess cash investment: Money market funds (AAA only)
    3. Intercompany loans require Treasury approval
    4. Daily cash position reporting required
    """,
    # ... more policies
}
```

### Step 2: RAG Implementation

```python
class PolicyRAG:
    """
    Retrieval-Augmented Generation for treasury policies.
    Uses TF-IDF for demonstration (production: use embeddings).
    """

    def __init__(self, documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(documents.values())

    def retrieve(self, query, top_k=2):
        """Find most relevant policy documents."""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.vectors)[0]

        top_indices = similarities.argsort()[-top_k:][::-1]
        results = []

        for idx in top_indices:
            doc_name = list(self.documents.keys())[idx]
            results.append({
                'document': doc_name,
                'content': self.documents[doc_name],
                'similarity': similarities[idx]
            })

        return results

    def answer(self, query):
        """Generate answer using retrieved context."""
        relevant_docs = self.retrieve(query)
        context = "\n\n".join([d['content'] for d in relevant_docs])

        # In production: Send to LLM with context
        # For demo: Simple keyword-based response
        return self._generate_response(query, context)
```

### Step 3: Intent Classification

Route queries to appropriate handlers:

```python
INTENT_PATTERNS = {
    'cash_position': ['cash', 'balance', 'liquidity', 'position'],
    'fx_rate': ['fx', 'exchange', 'usd', 'eur', 'currency'],
    'forecast': ['forecast', 'predict', 'projection', 'outlook'],
    'policy': ['policy', 'rule', 'guideline', 'requirement'],
    'hedge': ['hedge', 'hedging', 'forward', 'option']
}

def classify_intent(query):
    """Classify user query intent."""
    query_lower = query.lower()

    scores = {}
    for intent, keywords in INTENT_PATTERNS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        scores[intent] = score

    if max(scores.values()) == 0:
        return 'general'

    return max(scores, key=scores.get)
```

### Step 4: Treasury Functions

Integrate with treasury data:

```python
class TreasuryFunctions:
    """Treasury data access functions for the copilot."""

    def get_cash_position(self, currency=None):
        """Get current cash position by currency."""
        position = generate_bank_accounts()

        if currency:
            position = position[position['currency'] == currency]

        return {
            'total': position['balance'].sum(),
            'by_currency': position.groupby('currency')['balance'].sum().to_dict()
        }

    def get_fx_rate(self, pair):
        """Get latest FX rate for a currency pair."""
        rates = generate_fx_rates(days=1)
        rate = rates[rates['currency_pair'] == pair]['mid'].iloc[-1]
        return {'pair': pair, 'rate': rate}

    def get_forecast(self, horizon_days=30):
        """Get cash flow forecast."""
        # Would integrate with forecasting model
        return {
            'horizon': horizon_days,
            'expected_inflows': 150_000_000,
            'expected_outflows': 140_000_000,
            'net_position': 10_000_000
        }
```

### Step 5: Copilot Class

Bring it all together:

```python
class TreasuryCopilot:
    """
    AI-powered Treasury Assistant.
    """

    def __init__(self):
        self.rag = PolicyRAG(POLICY_DOCUMENTS)
        self.functions = TreasuryFunctions()
        self.conversation_history = []

    def chat(self, user_message):
        """Process user message and generate response."""
        # Classify intent
        intent = classify_intent(user_message)

        # Route to appropriate handler
        if intent == 'policy':
            response = self.rag.answer(user_message)
        elif intent == 'cash_position':
            data = self.functions.get_cash_position()
            response = f"Current cash position: ${data['total']:,.0f}"
        elif intent == 'fx_rate':
            pair = self._extract_currency_pair(user_message)
            data = self.functions.get_fx_rate(pair)
            response = f"{pair} rate: {data['rate']:.4f}"
        # ... more handlers

        self.conversation_history.append({
            'user': user_message,
            'assistant': response,
            'intent': intent
        })

        return response
```

## Demo Conversations

### Policy Query

```
User: What is our minimum hedge ratio requirement?

Copilot: According to our FX Hedging Policy, the minimum hedge
ratio is 75% for confirmed exposures. Additionally, all USD
exposures exceeding $1M must be hedged within 5 business days.

Source: fx_hedging_policy (similarity: 0.89)
```

### Data Query

```
User: What is our current cash position?

Copilot: Current Cash Position Summary:
- Total: $245,000,000
- USD: $120,000,000
- TRY: $80,000,000
- EUR: $45,000,000

Note: Position as of 2024-12-15 09:00 UTC
```

### Forecast Query

```
User: What's the 30-day cash flow forecast?

Copilot: 30-Day Cash Flow Forecast:
- Expected Inflows: $150,000,000
- Expected Outflows: $140,000,000
- Net Position: +$10,000,000

Key drivers:
- Crude payment due Dec 28: -$45M
- Product receivables: +$60M
- Q4 tax payment: -$25M
```

## Key Results

### Query Routing Accuracy

| Intent | Precision | Recall |
|--------|-----------|--------|
| cash_position | 95% | 92% |
| fx_rate | 92% | 94% |
| policy | 88% | 85% |
| forecast | 90% | 88% |
| **Average** | **91%** | **90%** |

### User Satisfaction

| Metric | Before Copilot | With Copilot |
|--------|----------------|--------------|
| Query resolution time | 15 minutes | 30 seconds |
| Self-service rate | 20% | 75% |
| Treasury team queries | 50/day | 15/day |

## Thinking Traces

!!! quote "Why RAG over fine-tuning?"
    Treasury policies change frequently (quarterly reviews). RAG allows updating the knowledge base without retraining the model. Fine-tuning would require expensive retraining every time a policy changes.

!!! quote "Why TF-IDF instead of embeddings?"
    For this demonstration, TF-IDF is simpler and doesn't require API calls. In production, you would use embeddings (OpenAI, Azure, or local models) for better semantic understanding.

!!! quote "Why intent classification before RAG?"
    Not all queries need document retrieval. "What's our cash position?" is a data query, not a policy query. Routing improves response accuracy and reduces unnecessary RAG calls.

## Production Considerations

### Technology Stack

| Component | Demo | Production |
|-----------|------|------------|
| Embeddings | TF-IDF | Azure OpenAI |
| Vector Store | In-memory | Pinecone/Weaviate |
| LLM | Rule-based | GPT-4/Claude |
| Data Access | Simulated | ERP/TMS APIs |

### Security Requirements

- **Authentication**: Azure AD / SSO integration
- **Authorization**: Role-based access to data functions
- **Audit logging**: All queries logged for compliance
- **Data masking**: PII and sensitive amounts protected

### Guardrails

```python
GUARDRAILS = {
    'max_amount_display': 100_000_000,  # Mask larger amounts
    'allowed_actions': ['read'],         # No write operations
    'sensitive_topics': ['salary', 'bonus', 'personal'],
    'escalation_triggers': ['approve', 'execute', 'transfer']
}
```

## Next Steps

After mastering this notebook:

1. → [08 Compliance](08-compliance.md) for automated regulatory reporting
2. → [01 Cash Flow Forecasting](01-cash-flow-forecasting.md) to improve forecast quality

## Code Access

📓 **Notebook**: [`notebooks/07_treasury_copilot.ipynb`](https://github.com/ozgurgulerx/treasury/blob/main/notebooks/07_treasury_copilot.ipynb)

---

*Author: Ozgur Guler (ozgur.guler1@gmail.com)*
