# Treasury

Enterprise AI Solutions for the Oil & Gas Industry

---

## Overview

Treasury is a comprehensive AI platform engineered specifically for the energy sector. It delivers intelligent automation, predictive analytics, and document intelligence capabilities designed to address the unique challenges of oil and gas operations.

## Features

- **Predictive Maintenance** — Anticipate equipment failures and optimize maintenance schedules
- **Production Optimization** — Maximize output through AI-driven operational insights
- **Document Intelligence** — Extract structured data from technical documents and regulatory filings
- **Anomaly Detection** — Real-time monitoring and alerting for critical operational parameters

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd treasury
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Documentation

Serve the documentation locally:

```bash
mkdocs serve
```

Build static documentation:

```bash
mkdocs build
```

## Project Structure

```
treasury/
├── docs/                 # MkDocs documentation source
├── 99-references/        # Reference materials (not tracked in git)
├── mkdocs.yml           # MkDocs configuration
├── requirements.txt     # Python dependencies
└── README.md
```

## Technology Stack

- **Documentation**: MkDocs with Material theme
- **Language**: Python 3.10+

## License

Proprietary — All rights reserved.

---

*Built for the energy industry.*
