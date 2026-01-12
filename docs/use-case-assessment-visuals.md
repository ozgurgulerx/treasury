# AI Use Case Assessment - Visual Templates

This document provides visual templates for prioritizing and documenting AI use cases in Oil & Gas Treasury.

---

## 1. Priority Matrix (Impact vs Effort)

### Quadrant Chart

```mermaid
quadrantChart
    title AI Use Case Prioritization Matrix
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Big Bets
    quadrant-2 Quick Wins
    quadrant-3 Low Priority
    quadrant-4 Strategic

    Daily Cash Monitoring: [0.25, 0.85]
    Bank Statement Matching: [0.30, 0.70]
    Policy RAG Q&A: [0.20, 0.55]
    Payment Anomaly Detection: [0.35, 0.80]
    FX Exposure Automation: [0.55, 0.85]
    Demurrage Prediction: [0.50, 0.90]
    Carbon Credit Forecasting: [0.60, 0.85]
    Covenant Early Warning: [0.65, 0.90]
    Treasury Copilot: [0.80, 0.95]
    Voyage Cost Optimizer: [0.75, 0.88]
```

### Example Priority Matrix (T8 Use Cases)

```
                           HIGH IMPACT
                                │
    ┌───────────────────────────┼───────────────────────────┐
    │                           │                           │
    │      QUICK WINS           │        BIG BETS           │
    │      Do First             │        Plan Carefully     │
    │                           │                           │
    │  • Daily Cash Monitoring  │  • Demurrage Prediction   │
    │  • Bank Statement Match   │  • Carbon Credit Forecast │
    │  • Payment Anomaly Det.   │  • FX Exposure Automation │
    │  • Policy RAG Q&A         │  • Covenant Early Warning │
    │                           │  • Treasury Copilot       │
    │                           │  • Voyage Cost Optimizer  │
    │                           │                           │
────┼───────────────────────────┼───────────────────────────┼────
    │                           │                           │
    │      LOW PRIORITY         │        STRATEGIC          │
    │      Deprioritize         │        Long-term          │
    │                           │                           │
    │  • Basic report templates │  • Full CTRM integration  │
    │  • Static dashboards      │  • End-to-end automation  │
    │                           │                           │
    └───────────────────────────┼───────────────────────────┘
                                │
                           LOW IMPACT
         LOW EFFORT ────────────┼──────────── HIGH EFFORT
```

### Quadrant Definitions

| Quadrant | Impact | Effort | Strategy |
|----------|--------|--------|----------|
| **Quick Wins** | High | Low | Do First - Immediate value with minimal investment |
| **Big Bets** | High | High | Plan Carefully - High reward but requires significant resources |
| **Low Priority** | Low | Low | Deprioritize - Limited value, consider automation later |
| **Strategic** | Low | High | Long-term - May enable future capabilities |

### Priority Scoring Formula

```
Priority Score = (Impact Score × Confidence Score) / Effort Score

Where:
- Impact Score: 1-5 (weighted average of 8 dimensions)
- Effort Score: 1-5 (weighted average of 9 dimensions)
- Confidence Score: 1-5 (weighted average of 4 dimensions)
```

---

## 2. Data Architecture Diagrams

### Generic Data Flow Template

```mermaid
flowchart LR
    subgraph Sources["Data Sources"]
        S1[ERP<br/>SAP/Oracle]
        S2[Bank<br/>APIs/SWIFT]
        S3[Market<br/>Bloomberg/Refinitiv]
        S4[Documents<br/>SharePoint/Email]
    end

    subgraph Processing["AI Processing Layer"]
        direction TB
        P1[Data Extraction<br/>& Transformation]
        P2[AI/ML Model<br/>Analysis]
        P3[Business Rules<br/>& Validation]
        P1 --> P2 --> P3
    end

    subgraph Outputs["Output Destinations"]
        O1[Dashboards<br/>Power BI]
        O2[Alerts<br/>Teams/Email]
        O3[Reports<br/>PDF/Excel]
        O4[Systems<br/>ERP/TMS]
    end

    Sources --> Processing --> Outputs

    style Processing fill:#e3f2fd
```

### Treasury-Specific Data Flow

```mermaid
flowchart TB
    subgraph Input["Input Sources"]
        direction LR
        SAP[SAP S/4HANA<br/>FI/CO/TRM]
        BANK[Bank Systems<br/>H2H/SWIFT/API]
        MKT[Market Data<br/>Bloomberg/Refinitiv]
        DOC[Documents<br/>Contracts/Emails]
    end

    subgraph Treasury["Treasury AI Platform"]
        direction TB

        subgraph L1["Layer 1: Data Integration"]
            ETL[ETL/API<br/>Connectors]
            NORM[Normalization<br/>& Cleansing]
        end

        subgraph L2["Layer 2: AI Models"]
            RAG[RAG Q&A<br/>Policy/Docs]
            ML[ML Models<br/>Forecast/Detect]
            OPT[Optimization<br/>Decision Support]
        end

        subgraph L3["Layer 3: Business Logic"]
            RULES[Business Rules]
            VALID[Validation]
            AUDIT[Audit Trail]
        end

        L1 --> L2 --> L3
    end

    subgraph Output["Outputs"]
        direction LR
        DASH[Dashboards]
        ALERT[Alerts]
        REPORT[Reports]
        ACTION[Actions/Postings]
    end

    Input --> Treasury --> Output

    style Treasury fill:#e8f5e9
```

### Refining-Specific Data Sources

```mermaid
flowchart LR
    subgraph Maritime["Maritime & Logistics"]
        AIS[AIS/Vessel Tracking<br/>MarineTraffic]
        PORT[Port Systems<br/>Terminal Data]
        CHARTER[Charter Party<br/>Documents]
    end

    subgraph Carbon["Carbon & ESG"]
        ETS[EU ETS Registry<br/>Allowances]
        EMIS[Emissions Data<br/>Refinery Systems]
        CERT[Certificates<br/>RECs/Offsets]
    end

    subgraph Commodity["Commodity & Trading"]
        ETRM[ETRM<br/>Endur/Allegro]
        PRICE[Price Feeds<br/>Platts/Argus]
        TANK[Tank Gauging<br/>Inventory]
    end

    subgraph Treasury["Treasury Systems"]
        TMS[TMS<br/>Kyriba/ION]
        BANK[Banking<br/>H2H/SWIFT]
        SAP[SAP<br/>FI/CO/TRM]
    end

    Maritime --> T8[T8 AI Platform]
    Carbon --> T8
    Commodity --> T8
    Treasury --> T8

    style T8 fill:#fff3e0
```

---

## 3. Use Case Card Templates

### Standard Use Case Card

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ USE CASE: [Name]                                           ID: [UC-XXX]     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Area: [Treasury Area]                    AI Pattern: [Pattern Type]         │
│ Owner: [Business Owner]                  Tech Lead: [Technical Owner]       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ SCORES                                                                      │
│ ────────────────────────────────────────────────────────────────────────    │
│ Impact:     ●●●●○ (4/5)     Effort:     ●●●○○ (3/5)                        │
│ Confidence: ●●●●● (5/5)     Priority:   ████████░░ HIGH (8.5)              │
│                                                                             │
│ Quadrant: QUICK WIN                                                         │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ PROBLEM STATEMENT                                                           │
│ ────────────────────────────────────────────────────────────────────────    │
│ [One paragraph describing the business problem and pain points]             │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ PROPOSED AI SOLUTION                                                        │
│ ────────────────────────────────────────────────────────────────────────    │
│ [One paragraph describing how AI will solve the problem]                    │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ DATA ARCHITECTURE                                                           │
│ ────────────────────────────────────────────────────────────────────────    │
│                                                                             │
│ Data Sources:              AI Processing:          Outputs:                 │
│ ┌────────────────┐        ┌──────────────┐        ┌──────────────┐         │
│ │ • SAP FI/CO    │───────►│ • Extract    │───────►│ • Dashboard  │         │
│ │ • Bank API     │        │ • ML Model   │        │ • Alerts     │         │
│ │ • Market Data  │        │ • Rules      │        │ • Reports    │         │
│ └────────────────┘        └──────────────┘        └──────────────┘         │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ KPI & BENEFITS                                                              │
│ ────────────────────────────────────────────────────────────────────────    │
│                                                                             │
│ Primary KPI:        [Metric name]                                           │
│ Baseline:           [Current value]                                         │
│ Target:             [Target value]                                          │
│ Est. Annual Benefit: [Currency amount]                                      │
│ Benefit Type:       [Cost reduction / Risk reduction / etc.]                │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ COMPLIANCE & TECHNICAL                                                      │
│ ────────────────────────────────────────────────────────────────────────    │
│                                                                             │
│ Data Classification: [Confidential]     PII Present: [Yes/No]               │
│ Auditability:        [Required]         Human-in-loop: [Yes/No]             │
│ Integration:         [API/Batch/RPA]    Complexity: [Low/Med/High]          │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ DEPENDENCIES & NEXT STEPS                                                   │
│ ────────────────────────────────────────────────────────────────────────    │
│                                                                             │
│ Dependencies:                                                               │
│ • [Dependency 1]                                                            │
│ • [Dependency 2]                                                            │
│                                                                             │
│ Next Steps:                                                                 │
│ □ [Action 1]                                                                │
│ □ [Action 2]                                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Compact Use Case Card (One-Pager)

```
┌────────────────────────────────────────────────────────────┐
│ [UC-001] Daily Cash Position Monitoring                    │
├────────────────────────────────────────────────────────────┤
│ Area: Treasury ALM          Pattern: Anomaly Detection     │
│ Impact: ●●●●○  Effort: ●●○○○  Confidence: ●●●●●           │
│ PRIORITY: HIGH (8.5) - QUICK WIN                           │
├────────────────────────────────────────────────────────────┤
│ Problem: Manual cash visibility delayed; anomalies missed  │
│ Solution: Auto-assemble positions, flag anomalies by 9am   │
├────────────────────────────────────────────────────────────┤
│ Sources: SAP, Bank API    →  Outputs: Power BI, Alerts     │
│ KPI: Cash visible by 9am  →  Target: 100% (from 60%)       │
│ Benefit: $500K/yr (working capital improvement)            │
└────────────────────────────────────────────────────────────┘
```

---

## 4. Scoring Rubrics

### Impact Scoring (1-5 Scale)

| Score | Label | Financial Value | Strategic Significance |
|-------|-------|-----------------|------------------------|
| **5** | Transformational | >$10M annual benefit | Competitive advantage, new capability |
| **4** | High | $2M-10M annual benefit | Strategic enabler, significant efficiency |
| **3** | Moderate | $500K-2M annual benefit | Good ROI, measurable improvement |
| **2** | Low | $100K-500K annual benefit | Limited scope, incremental improvement |
| **1** | Marginal | <$100K annual benefit | Nice-to-have, minimal impact |

### Effort Scoring (1-5 Scale)

| Score | Label | Duration | Complexity |
|-------|-------|----------|------------|
| **5** | Major | >6 months | Enterprise-wide change, multiple systems, heavy training |
| **4** | High | 3-6 months | Multiple integrations, process change, significant testing |
| **3** | Moderate | 1-3 months | Some process change, 2-3 integrations |
| **2** | Low | 2-4 weeks | 1-2 integrations, minimal process change |
| **1** | Trivial | <2 weeks | Single system, no process change, simple config |

### Confidence Scoring (1-5 Scale)

| Score | Label | Criteria |
|-------|-------|----------|
| **5** | Very High | Problem crystal clear, stakeholders aligned, data ready, proven technology |
| **4** | High | Good understanding, most stakeholders aligned, data mostly ready |
| **3** | Moderate | Some ambiguity, key stakeholders engaged, data gaps identified |
| **2** | Low | Unclear requirements, limited buy-in, significant data gaps |
| **1** | Very Low | Undefined problem, no stakeholder alignment, no data |

---

## 5. Implementation Roadmap Template

```mermaid
gantt
    title AI Use Case Implementation Roadmap
    dateFormat YYYY-MM

    section Phase 1: Foundation
    Data Platform Setup           :p1a, 2025-01, 2M
    API Integrations             :p1b, after p1a, 1M
    Security & Compliance        :p1c, after p1a, 2M

    section Phase 2: Quick Wins
    Cash Position Monitoring     :p2a, after p1b, 1M
    Bank Statement Matching      :p2b, after p2a, 1M
    Payment Anomaly Detection    :p2c, after p2a, 1M

    section Phase 3: Core AI
    FX Exposure Automation       :p3a, after p2b, 2M
    Cash Flow Forecasting        :p3b, after p2c, 2M
    Collections Copilot          :p3c, after p3a, 2M

    section Phase 4: Advanced
    Covenant Early Warning       :p4a, after p3b, 2M
    Trade Finance Automation     :p4b, after p3c, 3M
    Treasury Copilot             :p4c, after p4a, 3M
```

---

## 6. Data Source Inventory

### Core Treasury Systems

| System | Type | Data | Integration | Classification |
|--------|------|------|-------------|----------------|
| SAP S/4HANA | ERP | GL, AR, AP, Cash | API/RFC | Confidential |
| Kyriba | TMS | Positions, Hedges | API | Confidential |
| Bloomberg | Market | FX, Rates, Commodities | API | Internal |
| Bank H2H | Banking | Statements, Payments | SWIFT/EBICS | Highly Confidential |

### Refining-Specific Systems

| System | Type | Data | Integration | Classification |
|--------|------|------|-------------|----------------|
| MarineTraffic | AIS | Vessel positions, ETA | API | Internal |
| EU ETS Registry | Regulatory | Carbon allowances | API/File | Confidential |
| Platts/Argus | Pricing | Oil, Products, Bunker | API | Internal |
| ETRM (Endur) | Trading | Trades, Positions | API | Confidential |
| Tank Gauging | Operations | Inventory levels | API/OPC | Confidential |

---

## 7. AI Pattern Reference

```mermaid
mindmap
  root((AI Patterns))
    Copilot
      M365 Copilot
      Copilot Studio
      Custom Chatbot
    RAG
      Policy Q&A
      Document Search
      Knowledge Base
    Document AI
      OCR/Extraction
      Classification
      Compliance Check
    Predictive ML
      Forecasting
      Anomaly Detection
      Scoring
    Optimization
      Decision Support
      Scheduling
      Allocation
    Agentic
      Multi-step Workflow
      Autonomous Actions
      Orchestration
```

| Pattern | Best For | Complexity | Examples |
|---------|----------|------------|----------|
| **M365 Copilot** | Document assistance, summaries | Low | Weekly bulletin, meeting notes |
| **RAG Q&A** | Policy queries, knowledge access | Medium | Treasury policy bot, compliance Q&A |
| **Document Intelligence** | Form extraction, validation | Medium | LC processing, invoice matching |
| **Anomaly Detection** | Monitoring, fraud detection | Medium | Payment screening, reconciliation |
| **Forecasting** | Prediction, planning | High | Cash forecast, FX exposure |
| **Optimization** | Resource allocation, decisions | High | Hedge optimization, payment timing |
| **Agentic Workflow** | Multi-step automation | Very High | End-to-end processes, copilots |

---

## Appendix: Visual Assets Checklist

- [ ] Priority matrix with actual use cases plotted
- [ ] Data architecture diagram for each high-priority use case
- [ ] Use case cards for top 10 priorities
- [ ] Implementation roadmap with dates
- [ ] Data source inventory complete
- [ ] Stakeholder presentation deck
