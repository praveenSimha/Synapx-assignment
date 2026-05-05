# Intelligent Claims Processing Agent

AI-powered agent that automates initial validation and routing of insurance claims by extracting data from FNOL PDFs using LLMs and applying business rules.

## Features
- **PDF Text Extraction**: Converts FNOL PDFs to text for analysis.
- **Entity Extraction**: Uses Google/Gemini models via OpenRouter to extract structured data (policy info, incident details, parties, assets).
- **Automated Routing**: Routes claims based on damage amount, missing fields, fraud indicators, or injury mentions.
- **JSON Output**: Generates validated JSON with routing decisions.

## Prerequisites
- Python 3.8+
- pip package manager
- OpenRouter API key (free tier available)

## Installation
1. Clone repo: `git clone <repo-url>`
2. Create venv: `python -m venv .venv` (Windows: `.venv\Scripts\activate`)
3. Install deps: `pip install -r requirements.txt`

## Configuration
Create `.env` file with:
```
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/completions
MODEL_NAME=google/gemma-3-4b-it:free
```

## Usage
Process a claim PDF:
```bash
python src/agent.py <path_to_pdf>
```
- If filename only, looks in `data/input/`
- Outputs JSON to console and `data/output/output.json`

## Project Structure
- `src/agent.py`: CLI entrypoint
- `src/synapx/`: Core package
  - `claims_agent.py`: Main logic
  - `schema.py`: Pydantic models
  - `pdf.py`: PDF extraction
  - `llm.py`: OpenRouter client
  - `config.py`: Environment config
- `data/input/`: PDF files
- `data/output/`: JSON results
- `requirements.txt`: Dependencies
- `.env`: Configuration (not in repo)
