---
type: guide
created: 2026-05-29
tags: [wiki, obsidian, llm]
status: active
---

# Peppol LLM Wiki

This repository is an Obsidian-based wiki for building and maintaining LLM-assisted knowledge about Peppol.

The wiki stores knowledge as plain Markdown files under `vault/`. It is intentionally simple: folders, templates, frontmatter, and a lint script. There is no complex application here yet.

## Folder Structure

- `vault/00_inbox/`: quick captures and unsorted material.
- `vault/01_sources/`: one-note-per-source summaries.
- `vault/02_notes/`: working notes and rough synthesis.
- `vault/03_concepts/`: stable concept notes.
- `vault/04_projects/`: project context and task notes.
- `vault/05_answers/`: answers produced from the wiki.
- `vault/06_indexes/`: index notes and maps of content.
- `vault/07_staging/`: drafts, uncertain notes, and review queue.
- `vault/99_templates/`: reusable Markdown templates.
- `vault/assets/`: attachments for Obsidian.

## How Notes Work

Every Markdown file starts with YAML frontmatter. The most important field is `type`, because it tells tools and agents how the note should be handled.

Common note types:

- `source`: a summary of one source, stored in `vault/01_sources/`.
- `concept`: a stable synthesized concept, stored in `vault/03_concepts/`.
- `staging`: an uncertain draft, stored in `vault/07_staging/`.
- `answer`: a direct answer with sources and uncertainty, stored in `vault/05_answers/`.
- `index`: a navigation or overview note, stored in `vault/06_indexes/`.

Use Obsidian links such as `[[example-concept]]` to connect notes.

## Templates

Templates live in `vault/99_templates/`. They are normal Markdown files and can be copied into new notes.

Current templates:

- `source.md`
- `concept.md`
- `answer.md`
- `staging.md`
- `index.md`

## Linting

Run:

```powershell
python scripts/lint_wiki.py
```

The lint script checks that Markdown files have frontmatter, include a `type` field, and that key note types live in the correct folders.

## Ingesting Sources

Place a text file in `vault/00_inbox/`, then create a source note:

```powershell
python scripts/create_source_note.py example.txt --title "Example Source"
```

To ask an LLM for a draft analysis, set `OPENAI_API_KEY` and add `--llm`:

```powershell
python scripts/create_source_note.py example.txt --title "Example Source" --llm
```

The LLM output is always written to `vault/07_staging/` for review. It is never written directly to `vault/03_concepts/`.
