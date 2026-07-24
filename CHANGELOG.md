# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Add a self-hosted Claude Code marketplace for persistent user-scope installation.

## [0.1.1] - 2026-07-24

### Fixed

- Prohibit Claude Code WebSearch, WebFetch, and Fetch fallbacks during journal research.
- Add a Claude Code research agent with built-in WebSearch/WebFetch disabled.
- Require a successful Kimi WebBridge preflight before discovery.
- Require article-level full-text, abstract-only, metadata-only, or failed labels.
- Distinguish actual full-text reading from nominal open-access status.
- Generate a mandatory access ledger with source URLs and article IDs.
- Reject missing access evidence, conflicting access labels, and findings inferred from metadata.
- Require topics to be induced from article-level open codes after corpus audit.
- Prohibit unsupported year-over-year trend claims without an audited comparison corpus.
- Expand README installation and troubleshooting guidance for Kimi WebBridge.

## [0.1.0] - 2026-07-23

### Added

- Dual Codex and Claude Code plugin manifests.
- Complete journal discovery and article-reading protocol.
- Kimi WebBridge UTF-8-safe local client.
- Exact calendar windows for 1, 2, 3, and 6 months and 1 or 2 years.
- JSON Lines contracts for inventory, reading notes, discovery logs, and
  frontier evidence.
- Strict completeness, duplicate, date-boundary, and reading-coverage audit.
- Topic and keyword document-frequency metrics with temporal momentum.
- Evidence rules for separating journal attention from the broader field.
- Report template for trends, frontiers, open questions, and appendices.

[Unreleased]: https://github.com/kingfly51/journal-frontier-radar/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/kingfly51/journal-frontier-radar/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/kingfly51/journal-frontier-radar/releases/tag/v0.1.0
