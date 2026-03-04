#!/usr/bin/env python3
"""Generate INDEX.md — a clickable catalog of every PDF in the repo."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".claude", ".cursor", "scripts", "__pycache__"}

CATEGORY_LABELS = {
    "01_programming": "Programming",
    "02_development_tools": "Development Tools",
    "03_generative_ai": "Generative AI",
    "04_presentations": "Presentations",
    "05_certifications": "Certifications",
    "06_interview_prep": "Interview Prep",
}

GITHUB_MODELS_URL = "https://models.inference.ai.azure.com"
MODEL = "gpt-4o-mini"

# Label cache — populated once by _ensure_labels(), never None.
_AI_LABELS: dict[str, str] = {}


def _build_ai_labels(stems: list[str]) -> dict[str, str]:
    """Call GitHub Models once to get human-readable labels for all stems."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        # Fallback: simple title-case with underscores replaced by spaces
        return {s: s.replace("_", " ").title() for s in stems}

    try:
        from openai import OpenAI  # optional; present in CI, may be absent locally

        client = OpenAI(base_url=GITHUB_MODELS_URL, api_key=token)

        system_prompt = (
            "You convert snake_case identifiers (PDF filenames and directory names) "
            "into clean, human-readable display labels for a table-of-contents index.\n\n"
            "Rules:\n"
            "1. Proper title-case English — capitalize the first letter of each major word.\n"
            "2. Keep small prepositions/conjunctions lowercase unless they start the label "
            "(a, an, the, and, but, or, for, nor, on, at, to, by, in, of, up, as, vs, via).\n"
            "3. Correct casing for well-known tech terms, acronyms, and trademarks "
            "(e.g. AI, ML, LLM, RAG, API, SQL, BI, UI, UX, CLI, PDF, GPT, NLP, "
            "AWS, OpenAI, Google, Anthropic, NVIDIA, Neo4j, LangChain, LangGraph, "
            "PyTorch, Databricks, MITRE, TikTok, PwC, GitHub, GenAI, FastAPI, "
            "VS Code, GraphRAG, InsurTech, FinTech, MongoDB, ChatGPT, Perplexity, "
            "SAA-C03, multimodal).\n"
            "4. Preserve meaningful numbers (GPT-4, SAA-C03, Flash Attention 2).\n"
            "5. Respond ONLY with a JSON object mapping each input key to its label. "
            "No commentary, no code block fences."
        )

        # Send in batches of 200 to stay within token limits
        result: dict[str, str] = {}
        batch_size = 200
        for i in range(0, len(stems), batch_size):
            batch = stems[i : i + batch_size]
            user_msg = json.dumps(batch)
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.0,
                max_tokens=2000,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content.strip()
            result.update(json.loads(raw))

        return result

    except Exception as exc:
        print(f"  [warn] AI label generation failed, using fallback: {exc}")
        return {s: s.replace("_", " ").title() for s in stems}


def _ensure_labels(stems: list[str]) -> None:
    """Populate the global label cache for any stems not already present."""
    missing = [s for s in stems if s not in _AI_LABELS]
    if missing:
        _AI_LABELS.update(_build_ai_labels(missing))


def human_name(filename: str) -> str:
    """Return AI-generated (or fallback) human-readable label for a PDF filename."""
    stem = filename.removesuffix(".pdf")
    _ensure_labels([stem])
    return _AI_LABELS.get(stem, stem.replace("_", " ").title())


def subdir_label(name: str) -> str:
    """Return AI-generated (or fallback) human-readable label for a subdirectory."""
    _ensure_labels([name])
    return _AI_LABELS.get(name, name.replace("_", " ").title())


def collect_pdfs() -> dict[str, list[Path]]:
    """Walk the repo and group PDFs by their top-level category directory."""
    categories: dict[str, list[Path]] = {}
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in sorted(filenames):
            if f.lower().endswith(".pdf"):
                rel = Path(dirpath).relative_to(REPO_ROOT) / f
                top = rel.parts[0]
                categories.setdefault(top, []).append(rel)
    return dict(sorted(categories.items()))


def generate_index() -> tuple[str, int]:
    """Return (index_markdown, total_pdf_count)."""
    categories = collect_pdfs()
    total = sum(len(v) for v in categories.values())

    # Collect all stems in one pass so we can make a single batched AI call
    seen: set[str] = set()
    all_stems: list[str] = []
    for pdfs in categories.values():
        for p in pdfs:
            for token in (p.stem, p.parts[1] if len(p.parts) > 2 else None):
                if token and token not in seen:
                    all_stems.append(token)
                    seen.add(token)
    _ensure_labels(all_stems)

    lines = [
        "# Full Index",
        "",
        "_Auto-generated by `scripts/generate_index.py`. Do not edit manually._",
        "",
        f"**{total} PDFs** across {len(categories)} categories.\n",
    ]

    for cat, pdfs in categories.items():
        label = CATEGORY_LABELS.get(cat, cat)
        lines.append(f"## {label} ({len(pdfs)})\n")

        # Group by subdirectory
        subdirs: dict[str, list[Path]] = {}
        for p in pdfs:
            parts = p.parts
            subdir = parts[1] if len(parts) > 2 else ""
            subdirs.setdefault(subdir, []).append(p)

        for subdir in sorted(subdirs.keys()):
            sub_pdfs = subdirs[subdir]
            if subdir:
                lines.append(f"### {subdir_label(subdir)}\n")
            for pdf in sorted(sub_pdfs):
                name = human_name(pdf.name)
                link = str(pdf).replace(" ", "%20")
                lines.append(f"- [{name}]({link})")
            lines.append("")

    return "\n".join(lines), total


def update_readme_count(total: int) -> None:
    """Patch the PDF count in README.md to keep it in sync.

    Targets the specific bold count line near the top of README.md.
    Uses a sentinel comment <!-- PDF_COUNT --> if present, otherwise
    falls back to the first bold '\\d+ PDFs' pattern.
    """
    readme = REPO_ROOT / "README.md"
    text = readme.read_text()

    # Try sentinel-anchored replacement first
    sentinel_pattern = r"(<!-- PDF_COUNT -->.*?)\*\*\d+ PDFs\*\*"
    if re.search(sentinel_pattern, text):
        updated = re.sub(
            sentinel_pattern,
            rf"\g<1>**{total} PDFs**",
            text,
            count=1,
        )
    else:
        # Fallback: first bold count in the file (the summary line)
        updated = re.sub(r"\*\*\d+ PDFs\*\*", f"**{total} PDFs**", text, count=1)

    if updated != text:
        readme.write_text(updated)
        print(f"  README.md count updated to {total}")


if __name__ == "__main__":
    index, total = generate_index()
    out = REPO_ROOT / "INDEX.md"
    out.write_text(index)
    update_readme_count(total)
    print(f"Generated {out} ({total} PDFs)")
