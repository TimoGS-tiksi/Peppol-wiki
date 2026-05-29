from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n?", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None

    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def check_file(path: Path, root: Path, vault: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(root)
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)

    if frontmatter is None:
        return [f"{rel}: missing frontmatter"]

    note_type = frontmatter.get("type")
    if not note_type:
        errors.append(f"{rel}: missing type field")
        return errors

    normalized_type = note_type.strip("\"'").lower()
    concept_dir = vault / "03_concepts"
    source_dir = vault / "01_sources"
    staging_dir = vault / "07_staging"

    if normalized_type == "concept" and not is_relative_to(path, concept_dir):
        errors.append(f"{rel}: concept note must live in vault/03_concepts")
    if normalized_type == "source" and not is_relative_to(path, source_dir):
        errors.append(f"{rel}: source note must live in vault/01_sources")
    if normalized_type == "staging" and not is_relative_to(path, staging_dir):
        errors.append(f"{rel}: staging note must live in vault/07_staging")

    return errors


def lint(root: Path) -> list[str]:
    root = root.resolve()
    vault = root / "vault"
    markdown_files = []
    for name in ("README.md", "AGENTS.md"):
        path = root / name
        if path.exists():
            markdown_files.append(path)
    if vault.exists():
        markdown_files.extend(vault.rglob("*.md"))

    markdown_files = sorted(path for path in markdown_files if ".git" not in path.parts)

    errors: list[str] = []
    for path in markdown_files:
        errors.extend(check_file(path.resolve(), root, vault.resolve()))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the Obsidian LLM wiki.")
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root to lint. Defaults to the current directory.",
    )
    args = parser.parse_args()

    errors = lint(Path(args.root))
    if errors:
        print("Wiki lint failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Wiki lint passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
