---
type: guide
created: 2026-05-29
tags: [wiki, agents, rules]
status: active
---

# LLM Wiki Agent Instructions

This repository contains an Obsidian-based LLM wiki. The wiki is a knowledge base, not an application.

## Core Rules

- Write wiki content in Finnish unless the user asks otherwise.
- Prefer small, linked Markdown notes over long documents.
- Do not invent sources, citations, or certainty.
- If a note is uncertain, incomplete, or waiting for review, place it in `vault/07_staging/`.
- Do not create complex applications, services, databases, or UI layers unless the user explicitly asks for them.

## Folder Rules

- `vault/00_inbox/`: raw captures, quick drops, and unsorted notes.
- `vault/01_sources/`: source notes. Each note describes one source only.
- `vault/02_notes/`: working notes that are not yet stable concepts.
- `vault/03_concepts/`: concept notes. These should synthesize multiple sources or notes.
- `vault/04_projects/`: project-specific notes and task context.
- `vault/05_answers/`: answered questions with sources and uncertainty.
- `vault/06_indexes/`: maps of content and navigation indexes.
- `vault/07_staging/`: draft or uncertain notes waiting for review.
- `vault/99_templates/`: reusable Markdown templates.
- `vault/assets/`: images, PDFs, exports, and other attachments.

## Required Frontmatter

Every Markdown file must begin with YAML frontmatter and include at least:

```yaml
---
type: source
created: 2026-05-29
tags: []
status: draft
---
```

Allowed `type` values include:

- `source`
- `concept`
- `note`
- `project`
- `answer`
- `index`
- `staging`
- `template`
- `guide`

## Source Notes

- Use `type: source`.
- Store only in `vault/01_sources/`.
- Summarize one source only.
- Include enough bibliographic or URL information to find the source again.
- Separate direct quotes from summaries.

## Concept Notes

- Use `type: concept`.
- Store only in `vault/03_concepts/`.
- Keep one concept per file.
- Link related concepts with Obsidian links such as `[[routing]]`.
- Concept notes should synthesize; they should not be raw extraction from a single source.

## Staging Notes

- Use `type: staging`.
- Store only in `vault/07_staging/`.
- Explain what is uncertain or unfinished.
- Move or rewrite the note when it becomes stable.

## Answer Notes

Every answer note should include:

- The question.
- The short answer.
- Sources used.
- Uncertainty.
- Suggested wiki updates.

## Maintenance

- Run `python scripts/lint_wiki.py` before large reorganizations.
- Fix structure problems before adding more content.
- Keep templates simple enough that humans can use them directly in Obsidian.
