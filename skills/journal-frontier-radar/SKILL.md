---
name: journal-frontier-radar
description: Conduct a complete, evidence-traceable analysis of a user-selected academic journal over exactly 1 month, 2 months, 3 months, 6 months, 1 year, or 2 years. Use Kimi WebBridge to enumerate and read all recent articles, audit coverage, identify topics and keywords, compare the journal's attention with the broader field's current frontier, and formulate unresolved scientific questions. Use when asked for recent journal trends, journal topic mapping, journal surveillance, research-frontier reports, emerging themes, keyword analysis, or open-question discovery from a journal corpus.
---

# Journal Frontier Radar

Produce a reproducible journal-intelligence report from a complete article inventory and article-level reading notes. Separate what the journal publishes from what the broader field has established.

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
3. Initialize a run with `scripts/journal_radar.py init`. Use its exact inclusive start and end dates.
4. Use one Kimi WebBridge session for the whole task. Create one visible tab group named in the user's language and tell the user once. Never close it unless the user explicitly asks.
5. Discover the complete corpus from the official journal archive, issue tables of contents, latest/ahead-of-print pages, and pagination. Cross-check at least one independent index when one exists.
6. Record every candidate in `inventory.jsonl` using [data-contract.md](references/data-contract.md). Deduplicate by DOI, then canonical URL, then normalized title.
7. Read every included article:
   - Read full text when accessible.
   - Otherwise read the complete abstract and label `abstract_only`.
   - Label metadata-only records; never infer findings from titles.
   - Do not silently sample. For large corpora, work in batches and checkpoint until all records are covered.
8. Write one evidence card per article to `reading-notes.jsonl`. Keep claims, methods, findings, novelty, and limitations distinct.
9. Run `scripts/journal_radar.py audit --strict`. Repair omissions and duplicates before synthesis.
10. Analyze journal attention from the complete corpus. Report counts and denominators, not adjectives alone. Run `metrics` for topic, keyword, and temporal-momentum tables.
11. For each major topic, conduct a second, targeted frontier search using reviews, consensus/roadmap papers, and pivotal recent primary studies. Follow [source-playbook.md](references/source-playbook.md).
12. Derive open questions only from documented gaps, contradictions, boundary conditions, or methodological bottlenecks. Make them specific and testable.
13. Write the final report with [report-template.md](references/report-template.md), then rerun the audit and disclose residual limitations.

## Non-negotiable quality rules

- Treat “all articles” as a coverage claim that requires an audit trail.
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
- Every included inventory record has a reading note.
- Duplicate and out-of-window checks pass.
- Full-text, abstract-only, and metadata-only counts are reported.
- Hot topics include counts, shares, representative articles, and momentum.
- Frontier sections use evidence beyond the target journal.
- Each open question includes its evidence basis, why it remains unresolved, and a feasible test.
- The final report includes the full article appendix or a link/path to it.
