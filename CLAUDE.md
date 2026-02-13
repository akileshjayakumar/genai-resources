# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository and its contents.

## Project Overview

This is a curated PDF resource library — not a software project. There is no source code, build system, test suite, or CI/CD pipeline. The repository consists entirely of categorized PDF files covering software engineering, generative AI, cloud platforms, certifications, and interview preparation.

## Repository Structure

Directories are numbered to enforce browsing order:

- `01_programming/` — Language guides (Python, SQL, TypeScript, React) and framework references (FastAPI, API design), split into `languages/` and `frameworks/`
- `02_development_tools/` — Git, Docker, VS Code, Markdown references (flat directory)
- `03_generative_ai/` — Largest section; sub-categorized by provider/topic: `anthropic/`, `aws/`, `cursor/`, `deeplearning/`, `google/`, `guides_and_books/`, `langchain/`, `neo4j/`, `nvidia/`, `openai/`, `papers/`
- `04_presentations/` — Slide decks across domains: `business_intelligence/`, `cyber/`, `ds/`, `fintech/`, `keynote/`, `llm/`, `test_prep/`
- `05_certifications/` — AWS and GitHub exam guides (flat directory)
- `06_interview_prep/` — Interview tips and LLM interview Q&A (flat directory)

## Conventions

- **Naming**: PDF files use `snake_case` descriptive names (e.g., `python_finance_libraries.pdf`, `AWS_ai_practitioner_exam_guide.pdf`). Vendor/platform prefixes are capitalized.
- **Adding PDFs**: Place new files in the appropriate numbered category and subdirectory. Create a new subdirectory under an existing category if the topic doesn't fit existing ones.
- **Commits**: Follow the pattern `docs: add new PDF on <topic>` or `docs: add multiple new PDF` for bulk additions.
- **License**: MIT
