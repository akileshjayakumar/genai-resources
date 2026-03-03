# AGENTS.md

## Overview
Curated PDF resource library — **no source code, build system, tests, or CI/CD**. All content is categorized PDF files.

## Build / Lint / Test
None. Run `python scripts/generate_index.py` after adding PDFs to regenerate `INDEX.md`.

## Repository Structure
Numbered directories enforce browsing order:
- `01_programming/` — `languages/` and `frameworks/` (Python, SQL, TypeScript, React, FastAPI, API design)
- `02_development_tools/` — Git, Docker, VS Code, Markdown (flat)
- `03_generative_ai/` — Largest section; subdirs by provider (`anthropic/`, `aws/`, `google/`, `openai/`, etc.) and topic (`agents/`, `llm_fundamentals/`, `prompting/`, `rag/`, `papers/`, `deeplearning/`)
- `04_presentations/` — Slide decks: `business_intelligence/`, `cyber/`, `ds/`, `fintech/`, `keynote/`, `llm/`, `test_prep/`
- `05_certifications/` — AWS and GitHub exam guides (flat)
- `06_interview_prep/` — Interview tips and LLM Q&A (flat)

## Conventions
- **File naming**: `snake_case` descriptive names; capitalize vendor/platform prefixes (e.g., `AWS_ai_practitioner_exam_guide.pdf`).
- **Adding files**: Place PDFs in the correct numbered category/subdirectory. Create a new subdirectory if the topic doesn't fit.
- **Index**: Run `python scripts/generate_index.py` to update `INDEX.md`.
- **Commits**: Use `docs: add new PDF on <topic>` or `docs: add multiple new PDFs`.
- **License**: MIT.
