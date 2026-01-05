# Copilot Studio Architecture

Microsoft Copilot Studio is a low-code, graphical tool for building conversational AI agents and agent flows. It enables rapid deployment of chatbots with minimal technical expertise.

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        COPILOT STUDIO                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     AGENT BUILDER                                    │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Topics     │  │  Knowledge   │  │    Tools     │              │    │
│  │  │ (Dialogs)    │  │   Sources    │  │  (Actions)   │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Triggers   │  │   Entities   │  │  Variables   │              │    │
│  │  │              │  │ (Slot Fill)  │  │              │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     AGENT FLOWS                                      │    │
│  │         (Automated workflows with natural language)                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     CONNECTORS                                       │    │
│  │   Power Automate  |  Custom APIs  |  MCP Servers  |  Dataverse      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     CHANNELS                                         │    │
│  │   Teams  |  Web  |  Facebook  |  M365 Copilot  |  Custom            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Key Capabilities for Treasury

| Capability | Treasury Application |
|------------|---------------------|
| **Topics** | Pre-defined treasury Q&A dialogs |
| **Knowledge Sources** | Connect to SharePoint policies, documentation |
| **Generative AI** | Answer questions from uploaded documents |
| **Power Automate** | Trigger workflows (approvals, notifications) |
| **Teams Integration** | Treasury chatbot in Microsoft Teams |
| **Authentication** | Secure access with Azure AD |

## Treasury Chatbot Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TREASURY CHATBOT (Copilot Studio)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  USER CHANNELS                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │  Teams   │  │   Web    │  │  Mobile  │  │  M365    │                    │
│  │  App     │  │  Widget  │  │   App    │  │  Copilot │                    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                    │
│       │             │             │             │                           │
│       └─────────────┴─────────────┴─────────────┘                           │
│                            │                                                 │
│                            ▼                                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    TREASURY ASSISTANT AGENT                           │   │
│  │                                                                       │   │
│  │   ┌─────────────────────────────────────────────────────────────┐    │   │
│  │   │                     TOPICS                                   │    │   │
│  │   │                                                              │    │   │
│  │   │  • Cash Position    • FX Rates        • Policy Questions    │    │   │
│  │   │  • Payment Status   • Approval Status • Bank Info           │    │   │
│  │   │  • Forecast Query   • Limit Check     • Contact Info        │    │   │
│  │   └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                       │   │
│  │   ┌─────────────────────────────────────────────────────────────┐    │   │
│  │   │                  KNOWLEDGE SOURCES                           │    │   │
│  │   │                                                              │    │   │
│  │   │  • Treasury Policy Documents (SharePoint)                   │    │   │
│  │   │  • FAQ Database                                             │    │   │
│  │   │  • Procedure Manuals                                        │    │   │
│  │   └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                       │   │
│  │   ┌─────────────────────────────────────────────────────────────┐    │   │
│  │   │                      ACTIONS                                 │    │   │
│  │   │                                                              │    │   │
│  │   │  • Get Cash Balance  (→ Power Automate → SAP)              │    │   │
│  │   │  • Get FX Rate       (→ Power Automate → Bloomberg)        │    │   │
│  │   │  • Check Limit       (→ Power Automate → TMS)              │    │   │
│  │   │  • Submit Request    (→ Power Automate → Approval Flow)    │    │   │
│  │   └─────────────────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Pros and Cons

| Pros | Cons |
|------|------|
| **Fastest time to deploy** - hours not weeks | **Limited AI sophistication** |
| **No-code/low-code** - business users can build | **Less flexible** than custom agents |
| **Built-in Teams integration** | **Simpler conversations** only |
| **Knowledge grounding** from documents | **Limited multi-agent** orchestration |
| **Power Automate** for backend actions | **Dependent on connectors** |
| **Easy maintenance** and updates | **Cannot do complex ML** |
| **Cost-effective** for simple use cases | **M365 licensing** requirements |
| **Built-in analytics** | |

## Best Suited For

| Use Case | Fit |
|----------|-----|
| Treasury Policy Q&A | Excellent - document grounding |
| Payment Status Inquiry | Good - simple queries |
| Cash Balance Lookup | Good - with Power Automate |
| Employee Self-Service | Excellent - FAQ deflection |
| Complex Forecasting | Poor - needs custom ML |
| Multi-step Analysis | Limited - basic flows only |

## Sample Topic Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TOPIC: Cash Balance Inquiry                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐                                                   │
│  │ TRIGGER              │                                                   │
│  │ "What's our cash     │                                                   │
│  │  balance?"           │                                                   │
│  │ "Show cash position" │                                                   │
│  └──────────┬───────────┘                                                   │
│             │                                                                │
│             ▼                                                                │
│  ┌──────────────────────┐                                                   │
│  │ ASK QUESTION         │                                                   │
│  │ "Which entity do you │                                                   │
│  │  want to check?"     │                                                   │
│  │ [Entity dropdown]    │                                                   │
│  └──────────┬───────────┘                                                   │
│             │                                                                │
│             ▼                                                                │
│  ┌──────────────────────┐                                                   │
│  │ ASK QUESTION         │                                                   │
│  │ "Which currency?"    │                                                   │
│  │ [USD/EUR/TRY]        │                                                   │
│  └──────────┬───────────┘                                                   │
│             │                                                                │
│             ▼                                                                │
│  ┌──────────────────────┐     ┌──────────────────────┐                     │
│  │ CALL ACTION          │────▶│ Power Automate Flow  │                     │
│  │ "Get Cash Balance"   │     │ → SAP API Call       │                     │
│  └──────────┬───────────┘     └──────────────────────┘                     │
│             │                                                                │
│             ▼                                                                │
│  ┌──────────────────────┐                                                   │
│  │ SHOW MESSAGE         │                                                   │
│  │ "The cash balance    │                                                   │
│  │  for {Entity} in     │                                                   │
│  │  {Currency} is       │                                                   │
│  │  {Balance}"          │                                                   │
│  └──────────────────────┘                                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Comparison: Copilot Studio vs M365 Copilot Agent Builder

| Feature | Copilot Studio | M365 Agent Builder |
|---------|---------------|-------------------|
| Target User | Makers/Developers | Information Workers |
| Complexity | Medium | Low |
| Audience | Dept/Org/External | Individual/Small Team |
| Capabilities | Full workflows | Q&A focused |
| Governance | Full lifecycle | Limited |

## Prototype Space

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROTOTYPE: Treasury Policy Bot                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Status: [ ] Not Started  [ ] In Progress  [ ] Complete                     │
│                                                                              │
│  Components:                                                                 │
│  [ ] Create Copilot Studio agent                                            │
│  [ ] Upload treasury policy documents                                       │
│  [ ] Configure knowledge sources                                            │
│  [ ] Create 5 core topics (Cash, FX, Limits, Payments, Contacts)           │
│  [ ] Build Power Automate connectors                                        │
│  [ ] Deploy to Teams                                                        │
│  [ ] Test with treasury team                                                │
│                                                                              │
│  Notes:                                                                      │
│  _________________________________________________________________________  │
│  _________________________________________________________________________  │
│  _________________________________________________________________________  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```
