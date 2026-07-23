# Contributing

感谢你改进 Journal Frontier Radar。

## 开发原则

- 保持 Codex 与 Claude Code 共用同一份核心 `SKILL.md`。
- 不要为某个出版商写死只能用于单一期刊的选择器。
- 对“全量”“全文”“前沿”等强结论保留可审计证据。
- 不得加入绕过验证码、付费墙或访问控制的功能。
- 新的自动化逻辑应使用 Python 标准库，除非外部依赖带来明确且必要的收益。
- 详细说明放入 `references/`，保持 `SKILL.md` 聚焦核心执行流程。

## 本地验证

```bash
python scripts/validate_repo.py
```

如果修改 `journal_radar.py`，至少验证：

- 每个允许的时间窗口；
- 月末和闰年日期；
- DOI、URL 和标题去重；
- included/excluded 版本并存；
- 漏失 reading note；
- out-of-window 记录；
- topic momentum 的分母。

如果修改 WebBridge 行为，请勿在自动测试中操作用户已有标签页，也不要自动关闭会话。

## Pull request

PR 应说明：

1. 改动内容和原因；
2. 对 Codex、Claude Code 或两者的影响；
3. 使用的验证命令；
4. 涉及真实期刊时的测试范围和访问限制；
5. 是否改变数据结构或报告兼容性。

不要提交期刊全文、登录信息、Cookie、令牌或真实运行产生的
`.journal-frontier-radar/` 数据。
