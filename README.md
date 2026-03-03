# GenAI Resources Library

Curated collection of 159 PDFs covering generative AI, software engineering, cloud platforms, certifications, and interview prep.

## 📂 Structure

| Directory | Contents |
|---|---|
| [`01_programming/`](01_programming/) | Language guides (Python, SQL, TypeScript, React) and frameworks (FastAPI, API design) |
| [`02_development_tools/`](02_development_tools/) | Git, Docker, VS Code, Markdown references |
| [`03_generative_ai/`](03_generative_ai/) | The main section — organized by provider and topic |
| [`04_presentations/`](04_presentations/) | Slide decks: BI, cybersecurity, data science, fintech, keynotes |
| [`05_certifications/`](05_certifications/) | AWS and GitHub certification exam guides |
| [`06_interview_prep/`](06_interview_prep/) | Interview tips and LLM Q&A |

### Generative AI Breakdown

| Subdirectory | Focus |
|---|---|
| `agents/` | AI agent design, evaluation, and production guides |
| `anthropic/` | Claude Code and agentic coding best practices |
| `aws/` | Bedrock, GenAI infrastructure, and AWS whitepapers |
| `cursor/` | Cursor IDE productivity research |
| `deeplearning/` | ML fundamentals, PyTorch, deep learning |
| `google/` | Vertex AI, prompting guides, and agent frameworks |
| `guides_and_books/` | General GenAI playbooks and roadmaps |
| `langchain/` | LangChain, LangGraph, and agent frameworks |
| `llm_fundamentals/` | Core LLM concepts: embeddings, chunking, caching, fine-tuning, context engineering |
| `neo4j/` | Graph databases and GraphRAG |
| `nvidia/` | Inference servers and agentic AI development |
| `openai/` | GPT prompting guides, Codex, and enterprise AI |
| `papers/` | Research papers: Attention, FlashAttention, ReAct, RAG |
| `prompting/` | Prompt engineering guides and playbooks |
| `rag/` | RAG architectures, types, and pipeline optimization |

## 📖 Full Index

See [`INDEX.md`](INDEX.md) for a complete clickable catalog of every PDF.

To regenerate: `python scripts/generate_index.py`

## 🤝 Contributing

1. Place PDFs in the appropriate numbered category and subdirectory
2. Use `snake_case` names; capitalize vendor prefixes (e.g., `AWS_`, `OpenAI_`)
3. Run `python scripts/generate_index.py` to update the index
4. Commit with `docs: add new PDF on <topic>`

## License

[MIT](LICENSE)
