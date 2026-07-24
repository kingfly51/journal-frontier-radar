# Kimi WebBridge protocol

Use the local daemon at `http://127.0.0.1:10086/command`. Keep one stable session name for the entire journal task. The first `navigate` call must use `newTab: true` and a human-readable `group_title`.

## Tool exclusivity

This workflow is Kimi-only. Never use Claude Code `WebSearch`, `WebFetch`, or `Fetch`, and never use a generic fetch/search tool as a fallback. Those tools may reject publisher domains even when the user's real browser can access them.

Before discovery, prove the dependency works:

```text
python scripts/webbridge_client.py --session journal-check list_tabs
```

If that command fails after the client's one start attempt, stop. Do not continue with another browser tool and do not produce a research report.

Use `scripts/webbridge_client.py` to avoid shell quoting and Unicode corruption:

```text
python scripts/webbridge_client.py --session nature-6m navigate --args-json "{\"url\":\"https://www.nature.com/nature/research-articles\",\"newTab\":true,\"group_title\":\"Nature近6个月研究\"}"
python scripts/webbridge_client.py --session nature-6m snapshot
python scripts/webbridge_client.py --session nature-6m list_tabs
```

Available actions include `navigate`, `find_tab`, `snapshot`, `click`, `fill`, `evaluate`, `screenshot`, `network`, `upload`, `save_as_pdf`, `list_tabs`, `close_tab`, and `close_session`.

Prefer `snapshot` and its semantic element references. Use `evaluate` only for metadata not exposed in the snapshot, repetitive extraction, scrolling, or complex events. Wrap evaluation code in an IIFE and return compact JSON.

Use `newTab: true` only when pages need to coexist. Use `find_tab` with the exact URL to return to a task tab.

Never call `close_session` unless the user explicitly requests that the task's browser tabs be closed.

If the daemon is unreachable, the client attempts to start it once. If the retry fails, direct the user to:

- Chinese: https://www.kimi.com/zh-cn/features/webbridge
- English: https://www.kimi.com/features/webbridge

Do not stop, restart, or uninstall the daemon automatically. Do not bypass captchas, paywalls, or site security controls.
