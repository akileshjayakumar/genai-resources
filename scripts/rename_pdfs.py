#!/usr/bin/env python3
"""AI-powered PDF renamer using GitHub Models.

Accepts newly added PDF file paths as CLI arguments, extracts title/text
from each PDF, then calls GitHub Models (gpt-4o-mini) to suggest a clean
snake_case filename that follows this repo's naming conventions.
Files are renamed in-place.

Authentication: uses GITHUB_TOKEN (automatically available in GitHub Actions).
No external API keys or setup required.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import pypdf
from openai import OpenAI

GITHUB_MODELS_URL = "https://models.inference.ai.azure.com"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """\
You are a file-naming assistant for a curated GenAI and tech PDF resource \
library hosted on GitHub.

You will receive the content extracted from multiple pages of a PDF. \
Read it carefully to understand what the document is actually about — \
its topic, subject matter, and purpose — then output a single clean filename \
(without the .pdf extension) that reflects the true content.

RULES:
1. snake_case — lowercase words joined by underscores.
2. Capitalize vendor/platform prefixes ONLY when the PDF is clearly produced
   by that vendor AND the vendor name should appear as the first token:
     AWS_  OpenAI_  Google_  Anthropic_  NVIDIA_  Neo4j_  LangChain_
     LangGraph_  PyTorch_  Databricks_  MITRE_  TikTok_  PwC_  GitHub_
3. Descriptive and concise — 3 to 7 words capturing the core TOPIC/SUBJECT,
   not the author's name, course code, module number, or institution.
4. Name the CONTENT, not the packaging — "fintech_payments_and_blockchain"
   is better than "fintech_sarin_module_2"; "insurtech_risk_and_data_models"
   is better than "fintech_geczy_insurtech_slides".
5. Include version or year only when it meaningfully distinguishes the file
   (e.g. gpt_4_1, flash_attention_2, prompting_guide_2024_04).
6. No special characters other than underscores.
7. Omit filler: "the", "a", "an", "of", "document", "file", "pdf",
   "slides", "presentation", "module", "lecture", "overview" (unless truly
   the only useful descriptor).

GOOD EXAMPLES:
  aws_bedrock_rag_architecture
  OpenAI_practical_guide_to_building_agents
  attention_is_all_you_need
  fintech_payments_and_blockchain_overview
  fintech_lending_credit_risk_models
  insurtech_ai_risk_pricing
  real_estate_proptech_platforms
  Google_prompting_guide_101_2024_04
  llm_system_design_guide
  Neo4j_developers_guide_to_graphrag

Respond with ONLY the filename — no extension, no punctuation, no explanation.
"""


def extract_pdf_info(path: Path) -> tuple[str, str]:
    """Return (title_from_metadata, text_from_first_eight_pages)."""
    title = ""
    text = ""
    try:
        reader = pypdf.PdfReader(str(path))
        meta = reader.metadata
        if meta and getattr(meta, "title", None):
            title = (meta.title or "").strip()
        pages_to_read = min(8, len(reader.pages))
        for i in range(pages_to_read):
            text += (reader.pages[i].extract_text() or "") + "\n"
    except Exception as exc:
        print(f"  [warn] Could not read {path.name}: {exc}", file=sys.stderr)
    return title, text.strip()


def get_category(path: Path) -> str:
    """Return the relative directory of the PDF for context (e.g. 03_generative_ai/aws)."""
    parts = path.parts
    return "/".join(parts[:-1]) if len(parts) > 1 else "."


def suggest_filename(path: Path, client: OpenAI) -> str:
    """Ask GitHub Models for a clean filename suggestion."""
    title, text = extract_pdf_info(path)
    category = get_category(path)

    user_msg = (
        f"Category directory: {category}\n"
        f"Current filename: {path.name}\n"
        f"PDF title metadata: {title[:300] if title else 'N/A'}\n"
        f"First pages text (truncated to 3000 chars):\n{text[:3000] if text else 'N/A'}"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.1,
            max_tokens=80,
        )
        raw = response.choices[0].message.content.strip()
        # Sanitize: allow only alphanumeric and underscores.
        # This also neutralizes any path-traversal attempts (/ and . → _).
        clean = re.sub(r"[^a-zA-Z0-9_]", "_", raw)
        clean = re.sub(r"_+", "_", clean).strip("_")
        # Cap length — max_tokens=80 already limits this, but be explicit.
        clean = clean[:100]
        return clean
    except Exception as exc:
        print(f"  [warn] Model call failed for {path.name}: {exc}", file=sys.stderr)
        return ""


def rename_if_needed(path: Path, suggested: str) -> Path:
    """Rename path to suggested.pdf if the name differs; return the final path."""
    if not suggested or suggested.lower() == path.stem.lower():
        print(f"  OK (already well-named): {path.name}")
        return path

    new_path = path.with_name(suggested + ".pdf")
    if new_path.exists() and new_path != path:
        print(f"  [skip] Target already exists: {new_path.name} — keeping {path.name}")
        return path

    path.rename(new_path)
    print(f"  Renamed: {path.name}  →  {new_path.name}")
    return new_path


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set — skipping AI rename step.", file=sys.stderr)
        sys.exit(0)  # non-fatal: let the index regenerate anyway

    pdf_paths = [Path(p) for p in sys.argv[1:] if p.strip()]
    if not pdf_paths:
        print("No PDF paths provided — nothing to rename.")
        return

    client = OpenAI(base_url=GITHUB_MODELS_URL, api_key=token)

    renamed = 0
    for pdf in pdf_paths:
        if not pdf.exists():
            print(f"  [skip] File not found: {pdf}")
            continue
        print(f"\nProcessing: {pdf.name}")
        suggestion = suggest_filename(pdf, client)
        result = rename_if_needed(pdf, suggestion)
        if result != pdf:
            renamed += 1

    print(f"\nDone. {renamed} file(s) renamed.")


if __name__ == "__main__":
    main()
