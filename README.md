# GenAI Resources

**159 PDFs** covering generative AI, software engineering, cloud platforms, certifications, and interview prep.

> Browse the full catalog → [`INDEX.md`](INDEX.md)

---

## Contents

| # | Directory | What's inside |
|---|---|---|
| 1 | [`01_programming/`](01_programming/) | Python, SQL, TypeScript, React, FastAPI, API design |
| 2 | [`02_development_tools/`](02_development_tools/) | Git, Docker, VS Code, Markdown |
| 3 | [`03_generative_ai/`](03_generative_ai/) | The main section — see breakdown below |
| 4 | [`04_presentations/`](04_presentations/) | Slide decks: BI, cybersecurity, data science, fintech, keynotes |
| 5 | [`05_certifications/`](05_certifications/) | AWS and GitHub certification exam guides |
| 6 | [`06_interview_prep/`](06_interview_prep/) | Interview tips and LLM Q&A |

### Generative AI (`03_generative_ai/`)

| Subdirectory | Focus |
|---|---|
| `agents/` | Agent design, evaluation, and production guides |
| `anthropic/` | Claude and Claude Code best practices |
| `aws/` | Bedrock, GenAI on AWS, whitepapers |
| `deeplearning/` | ML fundamentals, PyTorch, deep learning |
| `google/` | Vertex AI, prompting guides, Gemini |
| `guides_and_books/` | General GenAI playbooks and roadmaps |
| `langchain/` | LangChain, LangGraph, agent frameworks |
| `llm_fundamentals/` | Embeddings, chunking, caching, fine-tuning, context engineering |
| `neo4j/` | Graph databases and GraphRAG |
| `nvidia/` | Inference servers and agentic AI development |
| `openai/` | GPT guides, Codex, enterprise AI |
| `papers/` | Attention, FlashAttention, ReAct, RAG, and more |
| `prompting/` | Prompt engineering guides and playbooks |
| `rag/` | RAG architectures, types, and pipeline optimization |

---

## Adding a PDF

1. Drop it in the right subdirectory
2. Push to a new branch and open a pull request
3. Once merged to `main`, CI auto-renames it to a clean snake_case name using AI and regenerates the index
4. No API keys needed; everything runs on the built-in `GITHUB_TOKEN`

To regenerate the index manually: `python scripts/generate_index.py`

---

## License

[MIT](LICENSE)
