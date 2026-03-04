# AGENTS.md

## Overview
Curated PDF resource library — **no application source code, build system, or test suite**. All content is categorized PDF files.

## Build / Lint / Test
None. Run `python scripts/generate_index.py` after adding PDFs to regenerate `INDEX.md`.

## Automation (GitHub Actions)
Merging a PDF into `main` (via pull request) triggers `.github/workflows/update_index.yml` which:
1. **AI-renames** newly added PDFs using GitHub Models (`gpt-4o-mini` via `GITHUB_TOKEN`) to produce clean, readable snake_case filenames following the conventions below.
2. **Regenerates** `INDEX.md` and patches the PDF count in `README.md`.
3. **Commits** all changes back to `main` as `github-actions[bot]`.

No API keys or secrets need to be configured — `GITHUB_TOKEN` is built into every Actions run.

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
