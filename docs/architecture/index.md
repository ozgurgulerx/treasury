# Architecture Options

This section evaluates three Microsoft platform options for building Treasury AI solutions for the Oil & Gas sector.

## Platform Overview

| Platform | Type | Primary Use |
|----------|------|-------------|
| [Microsoft Foundry](microsoft-foundry.md) | PaaS for AI/Agents | Multi-agent AI applications |
| [Microsoft Fabric](microsoft-fabric.md) | SaaS Analytics Platform | Data lakehouse & analytics |
| [Copilot Studio](copilot-studio.md) | Low-code Agent Builder | Conversational agents |

## Architecture Comparison Summary

| Criteria | Microsoft Foundry | Microsoft Fabric | Copilot Studio |
|----------|------------------|------------------|----------------|
| **Complexity** | High | Medium-High | Low |
| **AI Capabilities** | Advanced (multi-agent) | Built-in Copilot | Pre-built agents |
| **Data Platform** | External (connects to) | Native OneLake | External (connects to) |
| **Customization** | Full SDK access | Workload-specific | Limited |
| **Target User** | Developers | Data Engineers/Analysts | Business Users |
| **Time to MVP** | Weeks | Days-Weeks | Hours-Days |

## Recommended Architecture Patterns

Based on the Treasury AI use cases, we recommend a **hybrid approach**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TREASURY AI PLATFORM                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│  │  COPILOT STUDIO │   │ MICROSOFT       │   │ MICROSOFT       │           │
│  │                 │   │ FOUNDRY         │   │ FABRIC          │           │
│  │  • Treasury     │   │                 │   │                 │           │
│  │    Chatbot      │   │  • ML Models    │   │  • OneLake      │           │
│  │  • Q&A Bot      │   │  • Custom       │   │  • Data Factory │           │
│  │  • Policy Bot   │   │    Agents       │   │  • Power BI     │           │
│  │                 │   │  • Forecasting  │   │  • Real-Time    │           │
│  │                 │   │    Agents       │   │    Intelligence │           │
│  └────────┬────────┘   └────────┬────────┘   └────────┬────────┘           │
│           │                     │                     │                     │
│           └─────────────────────┼─────────────────────┘                     │
│                                 │                                           │
│                                 ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     MICROSOFT FABRIC - OneLake                        │  │
│  │                     (Unified Data Foundation)                         │  │
│  │                                                                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │ Bronze      │  │ Silver      │  │ Gold        │  │ Semantic    │  │  │
│  │  │ (Raw Data)  │  │ (Cleaned)   │  │ (Curated)   │  │ Models      │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Decision Matrix

See individual architecture pages for detailed pros/cons:

- [Microsoft Foundry Architecture](microsoft-foundry.md)
- [Microsoft Fabric Architecture](microsoft-fabric.md)
- [Copilot Studio Architecture](copilot-studio.md)
- [Data Sources & Simulation](data-sources.md)
- [Recommended Architecture & Verdict](verdict.md)
