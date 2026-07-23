# Research protocol

## 1. Freeze the scope

Record the journal name, ISSN if available, publisher, official archive URL, selected window, exact inclusive dates, timezone, canonical publication-date rule, article types, and output language. Use calendar subtraction rather than fixed 30-day months.

If the journal has multiple editions, supplements, or renamed/merged titles, document what is in scope. Do not merge a similarly named journal.

## 2. Build the discovery map

Open the official journal site first. Locate:

1. Latest articles or online-first/ahead-of-print.
2. Archive by year, volume, and issue.
3. Search results filtered by date.
4. Special collections or supplements that fall in the window.
5. Corrections, retractions, or expressions of concern linked to included records.

Traverse every page until the oldest observed canonical date is earlier than the window start. Record each discovery page URL and the visible result count or issue count. Repeat the boundary page once to catch mixed dates.

Cross-check against at least one independent index appropriate to the journal, such as Crossref, PubMed, Europe PMC, DOAJ, Scopus, Web of Science, Dimensions, or the publisher's API/search. An independent index is a completeness check, not automatically the source of truth.

Reconcile discrepancies:

- In official site only: verify article type and DOI.
- In index only: search the official site by DOI/title.
- Conflicting dates: preserve all date fields and apply the declared canonical-date rule.
- Duplicate online-first and issue versions: retain one article record and both URLs/dates.

## 3. Create the inventory

Create one `inventory.jsonl` record per candidate. Use stable `article_id` values, preferably `doi:<lowercase-doi>`; otherwise use `url:<canonical-url>` or a deterministic title/date identifier.

Normalize DOI by removing URL prefixes and lowercasing. Normalize titles for matching by Unicode normalization, lowercase, whitespace collapse, and punctuation removal. Never discard a suspected duplicate without recording the merge reason in `discovery_notes`.

Classify:

- `included`: scientific content in scope.
- `excluded`: outside article-type rules, outside dates, duplicate version, or non-content page.
- `uncertain`: requires manual resolution.

Keep excluded records when needed to substantiate archive totals.

## 4. Read every included article

For each included record, read in this order:

1. Abstract and article metadata.
2. Full text HTML or PDF if accessible.
3. Figures, tables, and captions that support the main claims.
4. Methods and limitations.
5. Supplementary material when central to the result and accessible.

Write the evidence card immediately. Do not postpone all note-taking until synthesis.

An evidence card must distinguish:

- The research question.
- Study design, model/system, sample/data, comparator, and analysis.
- Principal findings with direction and important magnitudes where available.
- What is genuinely new relative to prior work.
- Authors' limitations.
- Reader-identified limitations, clearly labeled as interpretation.
- Topic labels and controlled keywords.
- Reading level: `full_text`, `abstract_only`, or `metadata_only`.

Never convert a title or graphical abstract into a finding. If only the abstract is accessible, avoid detailed claims about methods or limitations not present there.

## 5. Audit before synthesis

Run the strict audit. Also perform a browser-level completeness audit:

- Official issue/article counts versus inventory counts.
- Earliest and latest dates.
- All pagination exhausted.
- Online-first and issue content deduplicated.
- Independent-index discrepancies resolved or listed.
- Every included article has one reading note.

If the corpus is large, process batches of 20–30 records and rerun the audit after each batch. Do not replace full coverage with a sample because of corpus size.

## 6. Analyze journal attention

Use hierarchical topic labels: broad field, subfield, and specific problem. Merge synonyms only when their scientific meaning is equivalent. Keep a mapping of merged labels.

For every topic report:

- Article count and share of included corpus.
- Article-type mix.
- Representative articles.
- Methods/models most used.
- Temporal momentum: compare the later half of the exact window with the earlier half, normalized by the number of articles in each half.
- Evidence strength and reading-level composition.

Keywords should combine author keywords, recurring concepts, methods, populations/models, outcomes, and enabling technologies. Report raw count and document frequency. Avoid generic terms such as “study,” “analysis,” and the journal's discipline name unless discriminative.

## 7. Research the broader frontier

Use the journal topics as queries, but do not constrain the frontier evidence to the target journal. For each major topic:

1. Find one recent authoritative review, consensus, roadmap, or benchmark when available.
2. Find pivotal recent primary studies supporting major advances.
3. Search for contradictory or negative evidence.
4. Identify technical bottlenecks, validation gaps, and boundary conditions.
5. Record each source in `frontier-sources.jsonl`.

Separate:

- Established progress: replicated or supported by multiple strong sources.
- Emerging progress: promising but early, narrow, or weakly validated.
- Contested claims: credible sources disagree.
- Unknowns: insufficient direct evidence.

## 8. Formulate scientific questions

Generate questions from evidence, not brainstorming alone. Each question must contain:

1. Precise unresolved question.
2. Evidence basis: article/source IDs.
3. Gap type: contradiction, mechanism, generalizability, measurement, causal inference, scalability, safety, translation, or reproducibility.
4. Why current methods/data cannot answer it.
5. A feasible study design or experiment.
6. Primary endpoint or falsification criterion.
7. Dependencies and likely risks.
8. Priority: impact, tractability, and time horizon.

Prefer a smaller set of defensible questions over a long speculative list.

## 9. Synthesize and disclose

Write conclusions at the strength allowed by the evidence. Include coverage numbers and date bounds near the top. Attach the full article inventory and evidence-card appendix. State unresolved discovery discrepancies, access limitations, and areas where conclusions rely heavily on abstracts.
