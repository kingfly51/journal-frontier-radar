---
name: journal-frontier-radar
description: Conduct a complete, evidence-traceable analysis of a user-selected academic journal over exactly 1 month, 2 months, 3 months, 6 months, 1 year, or 2 years. Use Kimi WebBridge to enumerate and read all recent articles, audit coverage, identify topics and keywords, compare the journal's attention with the broader field's current frontier, and formulate unresolved scientific questions. Use when asked for recent journal trends, journal topic mapping, journal surveillance, research-frontier reports, emerging themes, keyword analysis, or open-question discovery from a journal corpus.
---

# Journal Frontier Radar

Produce a reproducible journal-intelligence report from a complete article inventory and article-level reading notes. Separate what the journal publishes from what the broader field has established.

## Mandatory tool lock

Use Kimi WebBridge for every browser action in this workflow.

- Do not call `WebSearch`, `WebFetch`, `Fetch`, a generic browser fetcher, or a built-in search tool for journal discovery, article reading, or frontier research.
- Run the bundled `scripts/webbridge_client.py` through the shell. In Claude Code, prefer the plugin agent `journal-frontier-researcher`, which disables `WebSearch` and `WebFetch`.
- Perform a Kimi preflight with `list_tabs` before research. If Kimi remains unavailable after the client's one automatic start attempt, stop and report the dependency failure. Never fall back silently.
- If an error says a publisher domain is unsafe to fetch, the wrong tool was used. Return to Kimi WebBridge; do not retry with Fetch.

## Required inputs

Obtain or infer:

- Journal name and preferably its official homepage or archive URL.
- One allowed window: `1m`, `2m`, `3m`, `6m`, `1y`, or `2y`.
- Output language; default to the user's language.
- Optional article-type rules. Default to research articles, reviews, methods, resources, brief reports, perspectives, and editorials with substantive scientific content. Report excluded types and counts.

Ask only for a missing choice that would materially change the result. If the journal identity is ambiguous, resolve it with the user before browsing.

## Execution contract

1. Read [research-protocol.md](references/research-protocol.md) before starting.
2. Read [webbridge-protocol.md](references/webbridge-protocol.md) before browser actions.
3. Initialize a run with `scripts/journal_radar.py init`. Use its exact inclusive start and end dates. Do not write a standalone final report outside this run directory.
4. Run a Kimi `list_tabs` preflight, then use one Kimi session for the whole task. Create one visible tab group named in the user's language and tell the user once. Never close it unless the user explicitly asks.
5. Discover the complete corpus from the official journal archive, issue tables of contents, latest/ahead-of-print pages, and pagination. During discovery, use only journal/date/article-type queries. Do not search predicted topics.
6. Record every candidate in `inventory.jsonl` using [data-contract.md](references/data-contract.md). Deduplicate by DOI, then canonical URL, then normalized title.
7. Read every included article before defining themes:
   - Read full text when accessible.
   - Otherwise read the complete abstract and label `abstract_only`.
   - Label metadata-only and failed records; never infer findings from titles.
   - Record `source_url`, `accessed_at`, and the sections actually seen.
   - Do not silently sample. For large corpora, work in batches and checkpoint until all records are covered.
8. Write one evidence card per article to `reading-notes.jsonl`. Assign article-derived open codes, not a predetermined taxonomy.
9. Run `scripts/journal_radar.py audit --strict`. Repair omissions, access-label conflicts, and duplicates before any topic synthesis.
10. Derive themes inductively:
    - Review all article open codes.
    - Merge synonymous codes with a recorded rationale.
    - Retain outliers and multi-topic articles.
    - Freeze the topic codebook only after the corpus audit passes.
11. Run `metrics` for topic, keyword, and temporal-momentum tables. Report exact counts and denominators.
12. Run `ledger` and include the generated article-level access table in the report without removing rows or access labels.
13. Only now conduct targeted frontier searches derived from the frozen corpus topics. Use reviews, consensus/roadmap papers, pivotal recent primary studies, and contrary evidence. Follow [source-playbook.md](references/source-playbook.md).
14. Derive open questions only from documented gaps, contradictions, boundary conditions, or methodological bottlenecks. Make them specific and testable.
15. Write the final report with [report-template.md](references/report-template.md), then rerun `audit --strict --final` and disclose residual limitations.

## Non-negotiable quality rules

- Treat “all articles” as a coverage claim that requires an audit trail.
- Do not predefine themes, keyword buckets, or scientific questions before reading the corpus.
- Do not make comparisons with an earlier year unless that comparison corpus was independently inventoried and audited.
- Keep publication date, online date, issue date, and discovery date separate. Apply the window to the journal's chosen canonical publication date and state that choice.
- Distinguish journal attention, field-wide frontier, and the author's interpretation.
- Cite the article or source supporting every substantive frontier claim and open question.
- Do not treat keyword frequency as scientific importance. Combine frequency, share, momentum, novelty, and evidence strength.
- Do not equate publication volume with clinical or scientific validity.
- Flag paywalls, inaccessible supplements, retractions, corrections, expressions of concern, and abstract-only evidence.
- Preserve uncertainty. Use `insufficient evidence` when the corpus cannot support a conclusion.
- Quote sparingly; prefer faithful paraphrase and source links.

## Completion gate

Do not call the work complete until:

- Discovery pages and their coverage bounds are documented.
- The run directory contains `config.json`, all four JSONL evidence files, `metrics.json`, `access-ledger.md`, and `report.md`.
- Every included inventory record has a reading note.
- Duplicate, access-consistency, and out-of-window checks pass.
- Every article row displays `[全文]`, `[摘要]`, `[仅元数据]`, or `[访问失败]`, with a source URL.
- Full-text, abstract-only, metadata-only, and failed counts exactly equal the included-article total.
- Hot topics include counts, shares, representative articles, and momentum.
- Topics were frozen only after article reading and strict audit, and the report describes the inductive coding process.
- Frontier sections use evidence beyond the target journal.
- Each open question includes its evidence basis, why it remains unresolved, and a feasible test.
- The final report includes the full article appendix or a link/path to it.
- If any required artifact is missing, report the run as incomplete instead of producing an unaudited narrative.
