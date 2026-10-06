# CoverCheck
An AI assistant that checks patient cases against health plan coverage policies and returns cited, auditable determinations for human review.


Portfolio project. Uses public policy documents and synthetic patient data only. Not for real coverage or clinical decisions.

What it does

Given a patient case, a requested service, and a payer, CoverCheck finds the governing policy, extracts its criteria, and reports which criteria are met, unmet, or lack documentation, citing the policy passages behind each one.

Stack

Python, FastAPI, PostgreSQL + pgvector, Docker, GitHub Actions, Google Cloud Run

Data
CMS Medicare Coverage Database for policies
Synthea for synthetic patients
