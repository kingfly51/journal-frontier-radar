#!/usr/bin/env python3
"""Initialize, audit, and summarize a Journal Frontier Radar run."""

from __future__ import annotations

import argparse
import calendar
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any, Iterable

PERIOD_MONTHS = {"1m": 1, "2m": 2, "3m": 3, "6m": 6, "1y": 12, "2y": 24}
REQUIRED_INVENTORY = {
    "article_id",
    "title",
    "url",
    "canonical_date",
    "status",
    "article_type",
    "discovery_source",
    "access_status",
}
REQUIRED_NOTE = {
    "article_id",
    "reading_level",
    "research_question",
    "key_findings",
    "topics",
    "keywords",
    "confidence",
}


def subtract_months(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 - months
    year, zero_month = divmod(month_index, 12)
    month = zero_month + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def slugify(text: str) -> str:
    value = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value[:48] or "journal"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_number}: expected a JSON object")
        rows.append(row)
    return rows


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def unique_path(candidate: Path) -> Path:
    if not candidate.exists():
        return candidate
    for index in range(2, 1000):
        alternative = candidate.with_name(f"{candidate.name}-{index}")
        if not alternative.exists():
            return alternative
    raise RuntimeError("Could not allocate a unique run directory")


def cmd_init(args: argparse.Namespace) -> int:
    end = date.fromisoformat(args.today) if args.today else date.today()
    start = subtract_months(end, PERIOD_MONTHS[args.period])
    root = Path(args.output_root).resolve()
    run_name = f"{end:%Y%m%d}-{slugify(args.journal)}-{args.period}"
    run_dir = unique_path(root / run_name)
    run_dir.mkdir(parents=True)

    config = {
        "journal": args.journal,
        "journal_url": args.url or "",
        "period": args.period,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "date_rule": args.date_rule,
        "timezone": args.timezone,
        "article_types": args.article_types,
        "output_language": args.language,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(run_dir / "config.json", config)
    for name in (
        "inventory.jsonl",
        "reading-notes.jsonl",
        "frontier-sources.jsonl",
        "discovery-log.jsonl",
    ):
        (run_dir / name).write_text("", encoding="utf-8")
    (run_dir / "report.md").write_text(
        f"# {args.journal}: Journal Frontier Radar\n\n"
        f"Coverage: {start.isoformat()} through {end.isoformat()} (inclusive)\n",
        encoding="utf-8",
    )
    print(str(run_dir))
    return 0


def normalized_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[\W_]+", "", value)


def normalized_doi(value: Any) -> str:
    doi = str(value or "").strip().casefold()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi)
    return doi


def validate_required(
    rows: Iterable[dict[str, Any]], required: set[str], label: str
) -> list[str]:
    issues: list[str] = []
    for index, row in enumerate(rows, 1):
        missing = sorted(key for key in required if key not in row or row[key] in (None, ""))
        if missing:
            issues.append(f"{label} row {index} missing: {', '.join(missing)}")
    return issues


def audit_run(run_dir: Path) -> dict[str, Any]:
    config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
    inventory = read_jsonl(run_dir / "inventory.jsonl")
    notes = read_jsonl(run_dir / "reading-notes.jsonl")
    discovery = read_jsonl(run_dir / "discovery-log.jsonl")
    issues = validate_required(inventory, REQUIRED_INVENTORY, "inventory")
    issues += validate_required(notes, REQUIRED_NOTE, "reading note")

    included = [row for row in inventory if row.get("status") == "included"]
    included_ids = [str(row.get("article_id", "")) for row in included]
    note_ids = [str(row.get("article_id", "")) for row in notes]
    duplicate_article_ids = sorted(
        key for key, count in Counter(included_ids).items() if count > 1
    )
    duplicate_note_ids = sorted(key for key, count in Counter(note_ids).items() if count > 1)
    missing_notes = sorted(set(included_ids) - set(note_ids))
    orphan_notes = sorted(set(note_ids) - set(included_ids))

    doi_groups: dict[str, list[str]] = {}
    title_groups: dict[str, list[str]] = {}
    for row in included:
        article_id = str(row.get("article_id", ""))
        doi = normalized_doi(row.get("doi"))
        title = normalized_title(str(row.get("title", "")))
        if doi:
            doi_groups.setdefault(doi, []).append(article_id)
        if title:
            title_groups.setdefault(title, []).append(article_id)
    duplicate_dois = {key: ids for key, ids in doi_groups.items() if len(ids) > 1}
    duplicate_titles = {key: ids for key, ids in title_groups.items() if len(ids) > 1}

    start = date.fromisoformat(config["start_date"])
    end = date.fromisoformat(config["end_date"])
    out_of_window: list[str] = []
    invalid_dates: list[str] = []
    for row in included:
        article_id = str(row.get("article_id", ""))
        try:
            published = date.fromisoformat(str(row.get("canonical_date")))
        except ValueError:
            invalid_dates.append(article_id)
            continue
        if not start <= published <= end:
            out_of_window.append(article_id)

    reading_levels = Counter(
        str(row.get("reading_level", "unknown"))
        for row in notes
        if row.get("article_id") in set(included_ids)
    )
    if missing_notes:
        issues.append(f"{len(missing_notes)} included articles have no reading note")
    if orphan_notes:
        issues.append(f"{len(orphan_notes)} reading notes do not match an included article")
    if duplicate_article_ids:
        issues.append(f"{len(duplicate_article_ids)} included article IDs are duplicated")
    if duplicate_note_ids:
        issues.append(f"{len(duplicate_note_ids)} article IDs have duplicate reading notes")
    if duplicate_dois:
        issues.append(f"{len(duplicate_dois)} duplicate DOI groups")
    if duplicate_titles:
        issues.append(f"{len(duplicate_titles)} duplicate normalized-title groups")
    if out_of_window:
        issues.append(f"{len(out_of_window)} included articles are outside the date window")
    if invalid_dates:
        issues.append(f"{len(invalid_dates)} included articles have invalid dates")
    if not discovery:
        issues.append("discovery log is empty")
    if discovery and not all(row.get("pagination_complete") is True for row in discovery):
        issues.append("one or more discovery pages are not marked pagination_complete")

    return {
        "run_dir": str(run_dir),
        "window": {"start": config["start_date"], "end": config["end_date"]},
        "inventory_records": len(inventory),
        "included_articles": len(included),
        "reading_notes": len(notes),
        "reading_levels": dict(reading_levels),
        "missing_notes": missing_notes,
        "orphan_notes": orphan_notes,
        "duplicate_article_ids": duplicate_article_ids,
        "duplicate_note_ids": duplicate_note_ids,
        "duplicate_dois": duplicate_dois,
        "duplicate_titles": duplicate_titles,
        "out_of_window": out_of_window,
        "invalid_dates": invalid_dates,
        "discovery_pages": len(discovery),
        "issues": issues,
        "passed": not issues,
    }


def cmd_audit(args: argparse.Namespace) -> int:
    result = audit_run(Path(args.run_dir).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.strict and not result["passed"] else 0


def cmd_metrics(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
    inventory = read_jsonl(run_dir / "inventory.jsonl")
    notes = read_jsonl(run_dir / "reading-notes.jsonl")
    included = {
        row["article_id"]: row
        for row in inventory
        if row.get("status") == "included" and row.get("article_id")
    }
    start = date.fromisoformat(config["start_date"])
    end = date.fromisoformat(config["end_date"])
    midpoint_ordinal = (start.toordinal() + end.toordinal()) // 2

    topics: Counter[str] = Counter()
    keywords: Counter[str] = Counter()
    early_topics: Counter[str] = Counter()
    late_topics: Counter[str] = Counter()
    early_docs = 0
    late_docs = 0
    for note in notes:
        article = included.get(note.get("article_id"))
        if not article:
            continue
        published = date.fromisoformat(article["canonical_date"])
        unique_topics = {str(item).strip() for item in note.get("topics", []) if str(item).strip()}
        unique_keywords = {
            str(item).strip().casefold()
            for item in note.get("keywords", [])
            if str(item).strip()
        }
        topics.update(unique_topics)
        keywords.update(unique_keywords)
        if published.toordinal() <= midpoint_ordinal:
            early_docs += 1
            early_topics.update(unique_topics)
        else:
            late_docs += 1
            late_topics.update(unique_topics)

    momentum = []
    for topic in sorted(set(early_topics) | set(late_topics)):
        early_share = early_topics[topic] / early_docs if early_docs else 0.0
        late_share = late_topics[topic] / late_docs if late_docs else 0.0
        momentum.append(
            {
                "topic": topic,
                "early_count": early_topics[topic],
                "late_count": late_topics[topic],
                "early_share": round(early_share, 4),
                "late_share": round(late_share, 4),
                "share_change": round(late_share - early_share, 4),
            }
        )
    momentum.sort(key=lambda row: (-row["share_change"], row["topic"]))
    result = {
        "included_articles": len(included),
        "notes_analyzed": sum(1 for note in notes if note.get("article_id") in included),
        "topic_document_frequency": topics.most_common(),
        "keyword_document_frequency": keywords.most_common(),
        "time_halves": {"early_documents": early_docs, "late_documents": late_docs},
        "topic_momentum": momentum,
    }
    output = Path(args.output).resolve() if args.output else run_dir / "metrics.json"
    write_json(output, result)
    print(str(output))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a run directory")
    init_parser.add_argument("--journal", required=True)
    init_parser.add_argument("--url")
    init_parser.add_argument("--period", required=True, choices=sorted(PERIOD_MONTHS))
    init_parser.add_argument("--today", help="Override end date (YYYY-MM-DD)")
    init_parser.add_argument("--output-root", default=".journal-frontier-radar/runs")
    init_parser.add_argument("--date-rule", default="first_publication_date")
    init_parser.add_argument("--timezone", default="local")
    init_parser.add_argument("--article-types", default="default_scientific_content")
    init_parser.add_argument("--language", default="zh-CN")
    init_parser.set_defaults(func=cmd_init)

    audit_parser = subparsers.add_parser("audit", help="Audit inventory and notes")
    audit_parser.add_argument("run_dir")
    audit_parser.add_argument("--strict", action="store_true")
    audit_parser.set_defaults(func=cmd_audit)

    metrics_parser = subparsers.add_parser("metrics", help="Compute topic metrics")
    metrics_parser.add_argument("run_dir")
    metrics_parser.add_argument("--output")
    metrics_parser.set_defaults(func=cmd_metrics)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
