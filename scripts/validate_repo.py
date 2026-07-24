#!/usr/bin/env python3
"""Validate the dual-host Journal Frontier Radar repository."""

from __future__ import annotations

import json
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "journal-frontier-radar"


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(relative: str) -> dict:
    path = ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{relative}: {exc}")
    if not isinstance(value, dict):
        fail(f"{relative}: root must be a JSON object")
    return value


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
    fields: dict[str, str] = {}
    current_key: str | None = None
    for raw in text[4:end].splitlines():
        if raw.startswith((" ", "\t")) and current_key:
            fields[current_key] += " " + raw.strip()
            continue
        if ":" not in raw:
            fail(f"{path.relative_to(ROOT)}: invalid frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        current_key = key.strip()
        fields[current_key] = value.strip().strip("\"'")
    return fields


def validate_manifests() -> None:
    codex = load_json(".codex-plugin/plugin.json")
    claude = load_json(".claude-plugin/plugin.json")
    marketplace = load_json(".claude-plugin/marketplace.json")
    for label, manifest in (("Codex", codex), ("Claude Code", claude)):
        if manifest.get("name") != PLUGIN_NAME:
            fail(f"{label} manifest name must be {PLUGIN_NAME!r}")
        version = str(manifest.get("version", ""))
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            fail(f"{label} manifest has invalid semantic version: {version!r}")
        if not str(manifest.get("description", "")).strip():
            fail(f"{label} manifest description is required")
    if codex["version"] != claude["version"]:
        fail("Codex and Claude Code manifest versions must match")
    if codex.get("skills") != "./skills/":
        fail("Codex manifest must expose ./skills/")
    if marketplace.get("name") != "journal-frontier-radar-marketplace":
        fail("Claude Code marketplace has an unexpected name")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("Claude Code marketplace must contain exactly one plugin")
    entry = plugins[0]
    if entry.get("name") != PLUGIN_NAME:
        fail("Claude Code marketplace plugin name must match")
    if entry.get("version") != claude.get("version"):
        fail("Claude Code marketplace and plugin versions must match")
    source = entry.get("source", {})
    if source.get("source") != "github" or source.get("repo") != (
        "kingfly51/journal-frontier-radar"
    ):
        fail("Claude Code marketplace must install from the GitHub repository")


def validate_skill() -> None:
    skill = ROOT / "skills" / PLUGIN_NAME / "SKILL.md"
    fields = parse_frontmatter(skill)
    if set(fields) != {"name", "description"}:
        fail("SKILL.md frontmatter must contain only name and description")
    if fields["name"] != PLUGIN_NAME:
        fail("SKILL.md name must match the plugin name")
    if len(fields["description"]) < 80:
        fail("SKILL.md description is too short to trigger reliably")

    openai = ROOT / "skills" / PLUGIN_NAME / "agents" / "openai.yaml"
    text = openai.read_text(encoding="utf-8")
    if f"$journal-frontier-radar" not in text:
        fail("agents/openai.yaml default prompt must mention the skill")


def validate_paths_and_placeholders() -> None:
    required = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "agents/journal-frontier-researcher.md",
        "skills/journal-frontier-radar/references/research-protocol.md",
        "skills/journal-frontier-radar/references/data-contract.md",
        "skills/journal-frontier-radar/references/source-playbook.md",
        "skills/journal-frontier-radar/references/webbridge-protocol.md",
        "skills/journal-frontier-radar/references/report-template.md",
        "skills/journal-frontier-radar/scripts/journal_radar.py",
        "skills/journal-frontier-radar/scripts/webbridge_client.py",
    ]
    missing = [relative for relative in required if not (ROOT / relative).is_file()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")

    agent = (ROOT / "agents" / "journal-frontier-researcher.md").read_text(
        encoding="utf-8"
    )
    if "disallowedTools: WebSearch, WebFetch" not in agent:
        fail("Claude Code research agent must disable WebSearch and WebFetch")

    placeholder = "[" + "TODO:"
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".py"}:
            continue
        text = path.read_text(encoding="utf-8")
        if placeholder in text:
            fail(f"{path.relative_to(ROOT)} contains a TODO placeholder")


def validate_python() -> None:
    for path in ROOT.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")


def validate_calendar_logic() -> None:
    namespace: dict = {"__name__": "journal_radar_validation"}
    script = ROOT / "skills" / PLUGIN_NAME / "scripts" / "journal_radar.py"
    exec(compile(script.read_text(encoding="utf-8"), str(script), "exec"), namespace)
    subtract_months = namespace["subtract_months"]
    cases = [
        (date(2026, 7, 23), 6, date(2026, 1, 23)),
        (date(2024, 3, 31), 1, date(2024, 2, 29)),
        (date(2025, 3, 31), 1, date(2025, 2, 28)),
        (date(2026, 1, 31), 24, date(2024, 1, 31)),
    ]
    for end, months, expected in cases:
        actual = subtract_months(end, months)
        if actual != expected:
            fail(
                f"calendar subtraction failed: {end} - {months} months "
                f"was {actual}, expected {expected}"
            )


def validate_access_audit_and_ledger() -> None:
    namespace: dict = {"__name__": "journal_radar_validation"}
    script = ROOT / "skills" / PLUGIN_NAME / "scripts" / "journal_radar.py"
    exec(compile(script.read_text(encoding="utf-8"), str(script), "exec"), namespace)
    with tempfile.TemporaryDirectory() as temporary:
        run_dir = Path(temporary)
        (run_dir / "config.json").write_text(
            json.dumps(
                {
                    "start_date": "2026-01-01",
                    "end_date": "2026-07-24",
                }
            ),
            encoding="utf-8",
        )
        inventory = [
            {
                "article_id": "doi:10.1000/full",
                "title": "Full text paper",
                "url": "https://example.org/full",
                "doi": "10.1000/full",
                "canonical_date": "2026-02-01",
                "status": "included",
                "article_type": "research-article",
                "discovery_source": "official archive",
                "access_status": "full_text",
            },
            {
                "article_id": "doi:10.1000/abstract",
                "title": "Abstract paper",
                "url": "https://example.org/abstract",
                "doi": "10.1000/abstract",
                "canonical_date": "2026-05-01",
                "status": "included",
                "article_type": "research-article",
                "discovery_source": "official archive",
                "access_status": "abstract_only",
            },
        ]
        notes = [
            {
                "article_id": "doi:10.1000/full",
                "reading_level": "full_text",
                "source_url": "https://example.org/full",
                "accessed_at": "2026-07-24T10:00:00+08:00",
                "sections_read": ["Abstract", "Methods", "Results"],
                "research_question": "Question",
                "key_findings": ["Finding"],
                "open_codes": ["article code"],
                "topics": ["inductive theme"],
                "keywords": ["keyword"],
                "evidence_locations": ["Results"],
                "confidence": "high",
            },
            {
                "article_id": "doi:10.1000/abstract",
                "reading_level": "abstract_only",
                "source_url": "https://example.org/abstract",
                "accessed_at": "2026-07-24T10:10:00+08:00",
                "sections_read": ["Abstract"],
                "research_question": "Question",
                "key_findings": ["Abstract finding"],
                "open_codes": ["second code"],
                "topics": ["inductive theme"],
                "keywords": ["keyword"],
                "evidence_locations": ["Abstract"],
                "confidence": "medium",
            },
        ]
        for name, rows in (
            ("inventory.jsonl", inventory),
            ("reading-notes.jsonl", notes),
        ):
            (run_dir / name).write_text(
                "\n".join(json.dumps(row) for row in rows) + "\n",
                encoding="utf-8",
            )
        (run_dir / "discovery-log.jsonl").write_text(
            json.dumps(
                {
                    "url": "https://example.org/archive",
                    "pagination_complete": True,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        result = namespace["audit_run"](run_dir, final=True)
        if not result["passed"]:
            fail(f"valid access fixture failed audit: {result['issues']}")
        namespace["cmd_ledger"](
            SimpleNamespace(run_dir=str(run_dir), output=None)
        )
        ledger = (run_dir / "access-ledger.md").read_text(encoding="utf-8")
        if "[全文]" not in ledger or "[摘要]" not in ledger:
            fail("access ledger omitted full-text or abstract labels")


def main() -> int:
    checks = [
        ("plugin manifests", validate_manifests),
        ("skill metadata", validate_skill),
        ("required paths and placeholders", validate_paths_and_placeholders),
        ("Python syntax", validate_python),
        ("calendar boundaries", validate_calendar_logic),
        ("access audit and ledger", validate_access_audit_and_ledger),
    ]
    try:
        for label, check in checks:
            check()
            print(f"[OK] {label}")
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
