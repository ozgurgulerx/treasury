# AI Use Case Assessment Dashboard

## Executive Summary

This dashboard provides an overview of AI use case prioritization for Oil & Gas Treasury operations.

---

## Portfolio Overview

### Use Cases by Status

| Status | Count | % of Total |
|--------|-------|------------|
| Ideation | 10 | 100% |
| Assessment | 0 | 0% |
| Approved | 0 | 0% |
| In Development | 0 | 0% |
| Live | 0 | 0% |
| **Total** | **10** | **100%** |

### Priority Distribution

```
HIGH PRIORITY     ████████████████████  6 use cases (60%)
MEDIUM PRIORITY   ████████████░░░░░░░░  3 use cases (30%)
LOW PRIORITY      ████░░░░░░░░░░░░░░░░  1 use cases (10%)
```

---

## Priority Matrix

```
                           HIGH IMPACT
                                │
    ┌───────────────────────────┼───────────────────────────┐
    │                           │                           │
    │      QUICK WINS           │        BIG BETS           │
    │      (Do First)           │        (Plan Carefully)   │
    │                           │                           │
    │   Count: 4                │   Count: 6                │
    │   Avg Priority: 7.2       │   Avg Priority: 6.8       │
    │                           │                           │
    │   • Cash Monitoring       │   • Demurrage Prediction  │
    │   • Bank Matching         │   • Carbon Forecasting    │
    │   • Payment Anomaly       │   • FX Automation         │
    │   • Policy Q&A            │   • Covenant Warning      │
    │                           │   • Treasury Copilot      │
    │                           │   • Voyage Optimizer      │
────┼───────────────────────────┼───────────────────────────┼────
    │                           │                           │
    │      LOW PRIORITY         │        STRATEGIC          │
    │      (Deprioritize)       │        (Long-term)        │
    │                           │                           │
    │   Count: 0                │   Count: 0                │
    │   Avg Priority: --        │   Avg Priority: --        │
    │                           │                           │
    └───────────────────────────┼───────────────────────────┘
                                │
                           LOW IMPACT
         LOW EFFORT ────────────┼──────────── HIGH EFFORT
```

---

## Use Cases by Area

| Area | Count | Avg Impact | Avg Effort | Top Priority |
|------|-------|------------|------------|--------------|
| Treasury Liquidity & ALM | 2 | 4.5 | 2.5 | Cash Monitoring |
| Treasury, Market & Commodity Risk | 2 | 4.0 | 3.5 | FX Automation |
| Payments & Treasury Ops | 2 | 4.0 | 2.0 | Bank Matching |
| Maritime & Shipping Finance | 2 | 4.5 | 3.5 | Demurrage Prediction |
| Carbon & Energy Transition | 1 | 4.0 | 3.0 | Carbon Forecasting |
| Compliance / Risk / Controls | 1 | 4.5 | 3.5 | Covenant Warning |
| Trade Finance | 0 | -- | -- | -- |
| Storage & Inventory Finance | 0 | -- | -- | -- |
| Excise Tax & Regulatory | 0 | -- | -- | -- |
| **Total** | **10** | **4.2** | **3.0** | -- |

---

## Use Cases by AI Pattern

| AI Pattern | Count | % | Complexity |
|------------|-------|---|------------|
| Monitoring / anomaly detection | 3 | 30% | Medium |
| Forecasting / predictive ML | 3 | 30% | High |
| RAG Q&A over docs/data | 2 | 20% | Medium |
| Optimization / decision support | 1 | 10% | High |
| Agentic workflow (multi-step) | 1 | 10% | Very High |
| M365 Copilot (assist) | 0 | 0% | Low |
| Document intelligence | 0 | 0% | Medium |
| **Total** | **10** | **100%** | -- |

---

## Top 10 Priority Use Cases

| Rank | Use Case | Area | Impact | Effort | Confidence | Priority | Quadrant |
|------|----------|------|--------|--------|------------|----------|----------|
| 1 | Daily Cash Position Monitoring | Treasury ALM | 5 | 2 | 5 | 12.5 | Quick Win |
| 2 | Bank Statement Smart Matching | Payments Ops | 4 | 2 | 5 | 10.0 | Quick Win |
| 3 | Payment Anomaly Detection | Payments Ops | 4 | 2 | 4 | 8.0 | Quick Win |
| 4 | Policy RAG Q&A | Treasury ALM | 4 | 2 | 4 | 8.0 | Quick Win |
| 5 | Demurrage Prediction | Maritime | 5 | 3 | 4 | 6.7 | Big Bet |
| 6 | Carbon Credit Forecasting | Carbon & ESG | 4 | 3 | 4 | 5.3 | Big Bet |
| 7 | FX Exposure Automation | Risk Mgmt | 4 | 3 | 4 | 5.3 | Big Bet |
| 8 | Covenant Early Warning | Compliance | 5 | 4 | 4 | 5.0 | Big Bet |
| 9 | Voyage Cost Optimizer | Maritime | 4 | 4 | 4 | 4.0 | Big Bet |
| 10 | Treasury Copilot | Treasury ALM | 5 | 4 | 4 | 5.0 | Big Bet |

---

## Data Source Coverage

### Source System Usage

| Source System | Use Cases | % Coverage |
|---------------|-----------|------------|
| SAP S/4HANA (FI/CO) | 8 | 80% |
| Bank host-to-host / API | 4 | 40% |
| Bloomberg / Refinitiv | 3 | 30% |
| SharePoint / M365 | 2 | 20% |
| Power BI | 2 | 20% |
| MarineTraffic / AIS | 2 | 20% |
| EU ETS Registry | 1 | 10% |
| ETRM (Endur/Allegro) | 1 | 10% |

### Data Type Distribution

| Data Type | Count | % |
|-----------|-------|---|
| Structured transactions | 8 | 80% |
| Bank statements (MT940/camt) | 4 | 40% |
| Market data (FX/commodities) | 4 | 40% |
| Master data | 3 | 30% |
| Vessel tracking (AIS) | 2 | 20% |
| Contracts / PDFs | 2 | 20% |
| Carbon credits/allowances | 1 | 10% |

---

## Implementation Roadmap

### Phase 1: Foundation (Months 1-3)
- [ ] Data platform setup
- [ ] API integrations
- [ ] Security & compliance framework

### Phase 2: Quick Wins (Months 3-6)
- [ ] Use case 1: [TBD]
- [ ] Use case 2: [TBD]
- [ ] Use case 3: [TBD]

### Phase 3: Core AI (Months 6-9)
- [ ] Use case 4: [TBD]
- [ ] Use case 5: [TBD]
- [ ] Use case 6: [TBD]

### Phase 4: Advanced (Months 9-12)
- [ ] Use case 7: [TBD]
- [ ] Use case 8: [TBD]
- [ ] Use case 9: [TBD]

---

## Benefit Summary

| Benefit Type | Est. Annual Value | Use Case Count |
|--------------|-------------------|----------------|
| Cost reduction | $0 | 0 |
| Working capital / cash | $0 | 0 |
| Risk reduction | $0 | 0 |
| Compliance / audit | $0 | 0 |
| Productivity / cycle time | $0 | 0 |
| **Total Estimated Benefit** | **$0** | **0** |

---

## Risk & Compliance Overview

### Data Classification

| Classification | Use Cases | % |
|----------------|-----------|---|
| Public | 0 | 0% |
| Internal | 0 | 0% |
| Confidential | 0 | 0% |
| Highly Confidential | 0 | 0% |

### Human-in-the-Loop Requirements

| Requirement | Use Cases | % |
|-------------|-----------|---|
| Required (HITL) | 0 | 0% |
| Optional | 0 | 0% |
| Not Required | 0 | 0% |

### Auditability Requirements

| Requirement | Use Cases | % |
|-------------|-----------|---|
| Full audit trail required | 0 | 0% |
| Partial audit trail | 0 | 0% |
| Not required | 0 | 0% |

---

## Next Actions

### Immediate (This Week)
- [ ] Complete use case intake for [Area]
- [ ] Schedule scoring workshop
- [ ] Identify data owners

### Short-term (This Month)
- [ ] Finalize priority rankings
- [ ] Create business cases for top 5
- [ ] Engage technology partners

### Medium-term (This Quarter)
- [ ] Approve Phase 1 use cases
- [ ] Allocate budget and resources
- [ ] Begin implementation

---

## Appendix: Scoring Methodology

### Priority Formula
```
Priority Score = (Impact × Confidence) / Effort

Quadrant Assignment:
- Impact ≥ 3 AND Effort < 3  → Quick Win
- Impact ≥ 3 AND Effort ≥ 3  → Big Bet
- Impact < 3 AND Effort < 3  → Low Priority
- Impact < 3 AND Effort ≥ 3  → Strategic
```

### Weight Configuration

| Lens | Dimension | Weight |
|------|-----------|--------|
| **Impact** | Financial value | 12.5% |
| | Working capital / liquidity | 12.5% |
| | Risk reduction | 12.5% |
| | Compliance / audit | 12.5% |
| | Cycle time reduction | 12.5% |
| | Decision quality | 12.5% |
| | Stakeholder experience | 12.5% |
| | Strategic value | 12.5% |
| **Effort** | Data availability & quality | 11.1% |
| | Integration complexity | 11.1% |
| | Process change / adoption | 11.1% |
| | Model complexity | 11.1% |
| | Security / compliance effort | 11.1% |
| | Ops & support effort | 11.1% |
| | Vendor dependency | 11.1% |
| | Time to deliver | 11.1% |
| | Change mgmt / training | 11.1% |
| **Confidence** | Problem clarity | 25% |
| | Stakeholder alignment | 25% |
| | Data readiness | 25% |
| | Technical feasibility | 25% |

---

*Dashboard generated: [Date]*
*Data source: Use Case Assessment Template v2*
