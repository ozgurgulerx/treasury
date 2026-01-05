# Getting Started

## Prerequisites

- Python 3.10+
- pip package manager

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your environment variables in `.env`

## Running the Documentation

```bash
mkdocs serve
```

Visit `http://localhost:8000` to view the documentation.

## Building for Production

```bash
mkdocs build
```

The static site will be generated in the `site/` directory.
