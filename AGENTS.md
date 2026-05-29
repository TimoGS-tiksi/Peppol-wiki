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
- Every source note must identify practical implications for technology providers, organizations and decision makers whenever applicable.

## Source Note Generation Rules

When creating a source note, every section must contain meaningful content.

Never leave template sections empty.

The purpose of a source note is analysis, not extraction.

### Summary

Write a concise executive summary.

Length:
3-10 sentences.

Describe:

- what the document is about
- why it matters
- the main conclusions

Do not copy text from the source.

### Key Points

Identify the most important observations.

Use bullet points.

Prefer insights over facts.

Typically 5-15 bullets.

### Claims

Identify explicit or implicit claims made by the source.

For each claim indicate:

- claim
- supporting evidence if available
- confidence level

Example:

- Claim: Peppol adoption will increase because of ViDA.
  Evidence: EU proposals.
  Confidence: Medium.

### Assumptions

Identify assumptions made by the author.

Examples:

- technology assumptions
- regulatory assumptions
- market assumptions

Do not assume assumptions are true.

### Stakeholders

Identify affected stakeholders.

Examples:

- software vendors
- SMEs
- public sector
- accounting firms

Describe why the stakeholder is relevant.

### Risks

Identify risks and failure modes.

Examples:

- implementation risks
- regulatory risks
- vendor lock-in risks
- data quality risks

### Open Questions

Identify unanswered questions.

Focus on:

- missing evidence
- unresolved issues
- contradictions
- future developments

Questions should be actionable and researchable.

Bad:

"What happens next?"

Good:

"Will ViDA require real-time reporting for domestic invoices in Finland?"

### Related Concepts

Identify concepts that should exist in the wiki.

Use Obsidian links.

Example:

- [[Peppol]]
- [[EN 16931]]
- [[ViDA]]
- [[Data Quality]]

Only create links when the concept is genuinely relevant.

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
