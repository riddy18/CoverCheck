# CoverCheck

An AI assistant that checks patient cases against health plan coverage policies and returns cited, auditable determinations for human review.

> Portfolio project. Uses public policy documents and synthetic patient data only. Not for real coverage or clinical decisions.

## What it does

Given a patient case, a requested service, and a payer, CoverCheck finds the governing policy, extracts its criteria, and reports which criteria are met, unmet, or lack documentation, citing the policy passages behind each one.

## Status

The first stage, criteria extraction, works today. It takes the coverage section of a Medicare LCD and returns structured criteria, each backed by a verbatim quote from the policy. On the included Lumbar MRI sample (LCD L34220), every extracted quote matches the source text exactly. Policy retrieval, patient-case matching, and the API come next.

## Example output

Running the extractor on the Lumbar MRI LCD (L34220) returns structured criteria, each paired with the exact policy text it came from. On this sample, every `source_quote` matches the LCD text exactly.

```json
{
  "policy_title": "LCD L34220 - Lumbar MRI",
  "criteria": [
    {
      "description": "Lumbar MRI may be indicated for patients with a red-flag condition.",
      "category": "diagnosis",
      "source_quote": "Lumbar MRI may be indicated for a patient with a “red-flag” condition , such as a suspected tumor, infection, herniated intervertebral disc with nerve compression, or a major neurological problem."
    },
    {
      "description": "For non-red flag conditions, MRI may be appropriate after one month of symptoms.",
      "category": "duration",
      "source_quote": "For a \"non-red flag\" condition, the MRI may be appropriate after 1 month of symptoms."
    }
  ]
}
```

Full output: [`examples/lumbar_mri_L34220.json`](examples/lumbar_mri_L34220.json)

## Quickstart

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

    git clone https://github.com/riddy18/CoverCheck.git
    cd CoverCheck
    uv sync
    echo "GEMINI_API_KEY=your-key" > .env
    uv run python -m covercheck.extract data/sample_lcd.txt

Get a free key at [Google AI Studio](https://aistudio.google.com/apikey). The model defaults to `gemini-3.8-flash`; set `COVERCHECK_MODEL` to override it.

## Development

    uv run ruff check .
    uv run pytest

## Stack

**Current:** Python, Pydantic, Gemini API, pytest, ruff, GitHub Actions
**Planned:** FastAPI, PostgreSQL + pgvector, Docker, Google Cloud Run

## Data

- Policies: [CMS Medicare Coverage Database](https://www.cms.gov/medicare-coverage-database/search.aspx)
- Patients: [Synthea](https://synthetichealth.github.io/synthea/) synthetic records (planned)