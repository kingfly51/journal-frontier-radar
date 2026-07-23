#!/usr/bin/env python3
"""Validate the dual-host Journal Frontier Radar repository."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

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
    for label, manifest in (("Codex", codex), ("Claude Code", claude)):
        if manifest.get("name") != PLUGIN_NAME:
            fail(f"{label} manifest name must be {PLUGIN_NAME!r}")
        version = str(manifest.get("version", ""))
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            fail(f"{label} manifest has invalid semantic version: {version!r}")
        if not str(manifest.get("description", "")).strip():
            fail(f"{label} manifest description is required")
    if codex.get("skills") != "./skills/":
        fail("Codex manifest must expose ./skills/")


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


def main() -> int:
    checks = [
        ("plugin manifests", validate_manifests),
        ("skill metadata", validate_skill),
        ("required paths and placeholders", validate_paths_and_placeholders),
        ("Python syntax", validate_python),
        ("calendar boundaries", validate_calendar_logic),
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
