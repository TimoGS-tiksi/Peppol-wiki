from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib import request


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_title.lower()).strip("-")
    return slug or "untitled-source"


def first_non_empty_line(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    counter = 2
    while True:
        candidate = path.with_name(f"{path.stem}-{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def markdown_list(items: list[str]) -> str:
    if not items:
        return "-"
    return "\n".join(f"- {item}" for item in items)


def resolve_inbox_file(root: Path, inbox: Path, user_path: str) -> Path:
    candidate = Path(user_path)
    if not candidate.is_absolute():
        candidate = inbox / candidate

    resolved = candidate.resolve()
    try:
        resolved.relative_to(inbox.resolve())
    except ValueError:
        raise ValueError("Input file must be inside vault/00_inbox.")

    if not resolved.is_file():
        raise FileNotFoundError(f"Input file not found: {resolved}")

    return resolved


def build_llm_prompt(title: str, body: str) -> str:
    return f"""Analyze this source text for an Obsidian LLM wiki.

Return only valid JSON with these keys:
- summary: string
- key_points: array of strings
- claims: array of strings
- related_concepts: array of strings
- open_questions: array of strings

Do not invent facts. If the text does not support something, omit it or add an open question.

Title: {title}

Source text:
{body}
"""


def extract_json(text: str) -> dict[str, object]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"\A```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```\Z", "", stripped)
    return json.loads(stripped)


def normalize_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def call_openai_llm(prompt: str, model: str) -> dict[str, object]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You extract structured wiki staging notes from source text.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with request.urlopen(req, timeout=120) as response:
        response_payload = json.loads(response.read().decode("utf-8"))

    content = response_payload["choices"][0]["message"]["content"]
    return extract_json(content)


def build_staging_note(
    *,
    title: str,
    source_note_path: Path,
    analysis: dict[str, object],
    model: str,
) -> str:
    today = date.today().isoformat()
    summary = str(analysis.get("summary", "")).strip()
    key_points = normalize_string_list(analysis.get("key_points"))
    claims = normalize_string_list(analysis.get("claims"))
    related_concepts = normalize_string_list(analysis.get("related_concepts"))
    open_questions = normalize_string_list(analysis.get("open_questions"))

    return f"""---
type: staging
created: {today}
tags: [llm-ingest, source-analysis]
status: draft
reason: "LLM-generated source analysis for human review"
source_title: {yaml_quote(title)}
source_note: {yaml_quote(str(source_note_path.as_posix()))}
llm_model: {yaml_quote(model)}
---

# {title} - staging analysis

## Summary

{summary}

## Key Points

{markdown_list(key_points)}

## Claims

{markdown_list(claims)}

## Related Concepts

{markdown_list(related_concepts)}

## Open Questions

{markdown_list(open_questions)}

## Suggested Destination

Review this note before moving any synthesized concepts into `vault/03_concepts/`.
"""


def build_source_note(
    *,
    title: str,
    body: str,
    source_url: str,
    source_author: str,
    source_date: str,
) -> str:
    today = date.today().isoformat()
    return f"""---
type: source
created: {today}
tags: []
status: draft
source_title: "{title}"
source_url: "{source_url}"
source_author: "{source_author}"
source_date: "{source_date}"
---

# {title}

## Summary


## Key Points

-

## Direct Quotes


## Original Text

```text
{body.rstrip()}
```

## Related Notes

-

## Open Questions

-
"""


def create_source_note(
    root: Path,
    input_name: str,
    title: str | None,
    source_url: str,
    source_author: str,
    source_date: str,
) -> tuple[Path, str, str]:
    vault = root / "vault"
    inbox = vault / "00_inbox"
    sources = vault / "01_sources"
    sources.mkdir(parents=True, exist_ok=True)

    input_path = resolve_inbox_file(root, inbox, input_name)
    body = input_path.read_text(encoding="utf-8")
    note_title = title or first_non_empty_line(body) or input_path.stem
    slug = slugify(note_title)
    output_path = unique_path(sources / f"{slug}.md")

    note = build_source_note(
        title=note_title,
        body=body,
        source_url=source_url,
        source_author=source_author,
        source_date=source_date,
    )
    output_path.write_text(note, encoding="utf-8", newline="\n")
    return output_path, note_title, body


def create_staging_analysis(
    root: Path,
    title: str,
    body: str,
    source_note_path: Path,
    model: str,
) -> Path:
    vault = root / "vault"
    staging = vault / "07_staging"
    staging.mkdir(parents=True, exist_ok=True)

    prompt = build_llm_prompt(title, body)
    analysis = call_openai_llm(prompt, model)
    output_path = unique_path(staging / f"{slugify(title)}-analysis.md")
    note = build_staging_note(
        title=title,
        source_note_path=source_note_path.relative_to(root),
        analysis=analysis,
        model=model,
    )
    output_path.write_text(note, encoding="utf-8", newline="\n")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a source note from a text file in vault/00_inbox."
    )
    parser.add_argument("input", help="Text file name or path inside vault/00_inbox.")
    parser.add_argument("--title", help="Source note title. Defaults to first text line or filename.")
    parser.add_argument("--source-url", default="", help="Original source URL.")
    parser.add_argument("--source-author", default="", help="Original source author.")
    parser.add_argument("--source-date", default="", help="Original source publication date.")
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Call an LLM and write generated analysis to vault/07_staging.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        help="LLM model to use when --llm is set. Defaults to OPENAI_MODEL or gpt-4o-mini.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to the current directory.",
    )
    args = parser.parse_args()

    try:
        output_path, note_title, body = create_source_note(
            root=Path(args.root).resolve(),
            input_name=args.input,
            title=args.title,
            source_url=args.source_url,
            source_author=args.source_author,
            source_date=args.source_date,
        )
        print(f"Created {output_path}")

        if args.llm:
            staging_path = create_staging_analysis(
                root=Path(args.root).resolve(),
                title=note_title,
                body=body,
                source_note_path=output_path,
                model=args.model,
            )
            print(f"Created staging analysis {staging_path}")
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
