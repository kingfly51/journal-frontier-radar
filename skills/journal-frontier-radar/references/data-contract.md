# Run data contract

Each run contains UTF-8 JSON Lines files. Use one JSON object per line.

## `config.json`

Required keys:

```json
{
  "journal": "Journal name",
  "journal_url": "https://example.org/journal",
  "period": "6m",
  "start_date": "2026-01-23",
  "end_date": "2026-07-23",
  "date_rule": "first_publication_date",
  "timezone": "Asia/Shanghai",
  "article_types": "default_scientific_content",
  "output_language": "zh-CN",
  "created_at": "ISO-8601 timestamp"
}
```

## `inventory.jsonl`

Required for every record:

```json
{
  "article_id": "doi:10.xxxx/example",
  "title": "Article title",
  "url": "https://...",
  "doi": "10.xxxx/example",
  "canonical_date": "2026-06-01",
  "status": "included",
  "article_type": "research-article",
  "discovery_source": "official archive",
  "discovery_page": "https://...",
  "access_status": "full_text",
  "authors": ["A. Author"],
  "online_date": "2026-05-20",
  "issue_date": "2026-06-01",
  "volume": "10",
  "issue": "4",
  "abstract": "...",
  "author_keywords": ["..."],
  "discovery_notes": []
}
```

Allowed `status`: `included`, `excluded`, `uncertain`.

Allowed `access_status`: `full_text`, `abstract_only`, `metadata_only`, `unknown`.

## `reading-notes.jsonl`

Required for each included article:

```json
{
  "article_id": "doi:10.xxxx/example",
  "reading_level": "full_text",
  "research_question": "...",
  "study_design": "...",
  "methods": ["..."],
  "data_or_sample": "...",
  "key_findings": ["..."],
  "novelty": "...",
  "author_limitations": ["..."],
  "reader_limitations": ["..."],
  "topics": ["broad > subfield > problem"],
  "keywords": ["..."],
  "evidence_locations": ["Results, Fig. 2", "Discussion"],
  "confidence": "high",
  "notes": ""
}
```

Allowed `reading_level`: `full_text`, `abstract_only`, `metadata_only`.

Allowed `confidence`: `high`, `medium`, `low`.

Do not store long copied passages. `evidence_locations` should point to sections, figures, tables, or pages.

## `frontier-sources.jsonl`

```json
{
  "source_id": "doi:10.xxxx/frontier",
  "topic": "...",
  "title": "...",
  "url": "https://...",
  "doi": "10.xxxx/frontier",
  "published_date": "2026-01-01",
  "source_type": "systematic-review",
  "role": "established-progress",
  "claim_supported": "...",
  "limitations": ["..."],
  "reading_level": "full_text"
}
```

Allowed `role`: `established-progress`, `emerging-progress`, `contradictory-evidence`, `bottleneck`, `benchmark`, `consensus`.

## `discovery-log.jsonl`

Record every archive, issue, search, or index page used:

```json
{
  "url": "https://...",
  "source": "official archive",
  "visited_at": "ISO-8601 timestamp",
  "visible_count": 25,
  "date_min": "2026-05-01",
  "date_max": "2026-07-23",
  "pagination_complete": true,
  "notes": ""
}
```
