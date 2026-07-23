# Source playbook

## Source priority

Prefer sources in this order:

1. Official journal archive and article pages for corpus identity.
2. Publisher HTML/PDF and supplements for article reading.
3. DOI registry and discipline indexes for cross-checking.
4. Peer-reviewed systematic reviews, meta-analyses, consensus statements, roadmaps, and benchmarks for field status.
5. Primary research for advances and contradictions.
6. Preprints only for genuinely recent developments; label them unreviewed.
7. News, blogs, and press releases only for discovery, never as sole scientific evidence.

Use retraction/correction services and publisher notices when a record appears corrected or disputed.

## Browser strategy

Start from the official journal domain. Prefer semantic page snapshots and visible archive controls. Use page evaluation only when needed to extract repetitive metadata or links. Do not bypass access controls, captchas, or paywalls.

When an archive uses infinite scroll:

1. Capture current item count and oldest date.
2. Scroll/load more.
3. Repeat until the oldest date is before the start boundary and the count stops changing.
4. Save the final count and boundary dates in the discovery log.

When an archive has numbered pagination, visit every page overlapping the date window plus one older boundary page.

When a search UI caps results, split queries by month, issue, or article type and reconcile overlaps.

## Frontier query design

For each major topic, create queries that combine:

- Core concept and synonyms.
- `review`, `systematic review`, `meta-analysis`, `consensus`, `roadmap`, or `benchmark`.
- The enabling method or model.
- The key unresolved mechanism or outcome.
- Recent year filters appropriate to the field.

Search for disconfirmation explicitly with terms such as `negative`, `failed replication`, `limitations`, `bias`, `external validation`, `benchmark`, and `controversy`.

## Evidence rules

- Use at least two independent strong sources for a broad “field has advanced” claim when available.
- Prefer direct primary evidence for quantitative performance or causal claims.
- Do not use a review's citation to stand in for a primary result when the primary paper is accessible.
- Record whether evidence is full text, abstract only, or metadata only.
- Clearly identify inference when combining sources.
