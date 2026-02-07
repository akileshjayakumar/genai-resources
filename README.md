# GenAI Resources Library

Curated PDFs for learning software engineering, generative AI, tools, certifications, and interview prep.

## Quick Start

### Prerequisites
- Git
- A PDF reader

### Clone
```bash
git clone https://github.com/akileshjayakumar/daily-genai-guides.git
cd daily-genai-guides
```

### Browse by Topic
```bash
ls -1
ls -1 03_generative_ai
```

### Open a Resource (macOS)
```bash
open 03_generative_ai/openai/OpenAI_gpt_5_prompting_guide.pdf
```

## Core Sections
- `01_programming`: language and framework guides.
- `02_development_tools`: Git, Docker, markdown, and productivity references.
- `03_generative_ai`: vendor guides, papers, and practical GenAI playbooks.
- `04_presentations`: presentation decks across DS, BI, fintech, cyber, and LLM topics.
- `05_certifications`: exam guides and certification prep.
- `06_interview_prep`: technical interview study materials.

## Configuration
No environment variables are required.

## Usage Example
Find all OpenAI resources:
```bash
find 03_generative_ai/openai -type f -name "*.pdf" | sort
```

## Contributing and Validation
1. Add files in the most specific existing folder.
2. Use clear, descriptive filenames.
3. Verify links and paths in this README after changes.

Quick check:
```bash
find . -type f -name "*.pdf" | wc -l
```

## License
MIT (see `LICENSE`).
