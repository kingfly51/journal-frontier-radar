# Journal Frontier Radar

[![Validate plugin](https://github.com/kingfly51/journal-frontier-radar/actions/workflows/validate.yml/badge.svg)](https://github.com/kingfly51/journal-frontier-radar/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

面向 **Codex** 与 **Claude Code** 的期刊前沿雷达插件。它通过
[Kimi WebBridge](https://www.kimi.com/zh-cn/features/webbridge) 操作用户的真实浏览器，
全量检索指定期刊在选定时间窗口内的文章，逐篇阅读并建立证据卡，最终回答：

- 该期刊近期重点关注哪些领域？
- 高频和上升关键词是什么？
- 这些主题在整个领域中的前沿进展如何？
- 当前证据有哪些争议、边界和方法学瓶颈？
- 哪些科学问题值得继续研究，如何设计可证伪的研究？

> English summary: A Codex and Claude Code plugin that uses Kimi WebBridge to
> enumerate and read a journal's recent articles, audit corpus completeness,
> map topics and keywords, assess the broader research frontier, and formulate
> evidence-grounded open scientific questions.

## 核心特性

- **用户自定义期刊**：支持期刊名称、主页或 archive URL。
- **固定时间选项**：`1m`、`2m`、`3m`、`6m`、`1y`、`2y`。
- **默认全量覆盖**：不因文章数量较大而静默抽样。
- **逐篇证据卡**：区分研究问题、方法、样本、结果、创新和局限。
- **多来源完整性核对**：官方 archive、issue TOC、online first 与独立索引交叉检查。
- **访问层级披露**：分别统计全文、仅摘要和仅元数据记录。
- **趋势量化**：输出主题占比、关键词文档频率和时间窗口前后半段动量。
- **期刊热点与领域前沿分离**：热点来自目标期刊全集；前沿结论使用期刊外部证据。
- **开放问题可检验**：每个问题包含证据基础、未决原因、建议设计和证伪标准。
- **可审计输出**：完整文章清单、逐篇笔记、外部前沿来源和发现日志均可追溯。

## 工作流

```text
确定期刊与精确日期边界
        ↓
遍历官方 archive / issue / online-first / pagination
        ↓
使用独立索引核对并去重
        ↓
逐篇阅读全文或完整摘要
        ↓
运行覆盖、重复和日期审计
        ↓
计算主题、关键词和时间动量
        ↓
检索综述、共识、基准和关键原始研究
        ↓
区分已建立进展、早期进展、争议和未知
        ↓
生成可证伪的开放科学问题与最终报告
```

## 前置条件

1. Codex 或 Claude Code。
2. Python 3.9 或更高版本。
3. 已安装并连接浏览器扩展的 Kimi WebBridge。
4. 对目标期刊页面的合法访问权限。

插件不会绕过验证码、付费墙或网站访问控制。无法访问全文的文章会明确标记为
`abstract_only`，而不是伪装成全文证据。

## 安装 Kimi WebBridge

本插件**不会捆绑** Kimi WebBridge。首次使用前请从官方页面安装浏览器扩展和本地服务：

- [Kimi WebBridge 中文安装页](https://www.kimi.com/zh-cn/features/webbridge)
- [Kimi WebBridge English](https://www.kimi.com/features/webbridge)

安装后打开浏览器并确认扩展已连接，然后在插件目录运行：

```bash
python skills/journal-frontier-radar/scripts/webbridge_client.py \
  --session journal-radar-check \
  list_tabs
```

成功时会返回包含 `success` 和 `tabs` 的 JSON。若客户端无法连接，会自动尝试启动本地
服务一次；再次失败时应先修复或更新 WebBridge，不要改用 Claude Code 的
`WebSearch`、`WebFetch` 或 `Fetch`。

## 安装与加载

### Claude Code

克隆仓库并使用本地插件目录启动：

```bash
git clone https://github.com/kingfly51/journal-frontier-radar.git
claude --plugin-dir ./journal-frontier-radar
```

技能入口：

```text
/journal-frontier-radar:journal-frontier-radar
```

完整分析推荐在 Claude Code 的 `/agents` 中选择
`journal-frontier-radar:journal-frontier-researcher`。该代理明确禁用
`WebSearch` 和 `WebFetch`，只通过 Kimi WebBridge 访问期刊页面。

Claude Code 插件结构遵循其
[官方插件规范](https://code.claude.com/docs/en/plugins-reference)。

### Codex

仓库根目录包含 `.codex-plugin/plugin.json`，可作为 Codex 本地插件源或个人/团队
marketplace 中的插件目录使用。安装后调用：

```text
使用 $journal-frontier-radar 分析 Nature Communications 最近6个月的文章，
用中文输出热点、关键词、领域前沿和开放科学问题。
```

Codex 的个人 marketplace、团队 marketplace 和插件 UI 可能随版本更新，请使用当前
Codex 客户端提供的“添加本地插件/marketplace”入口注册本仓库。

## 使用示例

### 基础请求

```text
分析 The Lancet Digital Health 最近6个月的全部科学文章。
逐篇阅读可访问全文，输出该期刊关注领域、关键词、领域前沿以及待解决问题。
```

### 指定文章类型

```text
分析 Nature Machine Intelligence 最近1年的 Research Article、Review 和 Perspective，
排除新闻、书评和纯编辑通知。请列出所有排除项及原因。
```

### 强调研究机会

```text
分析 Cell 最近3个月的文章。除了期刊趋势，还要对每个主要主题检索外部综述和
关键原始研究，最后给出5个高影响且可执行的科学问题。
```

更多请求模板见 [examples/prompts.md](examples/prompts.md)。

## 运行数据

每次分析会在当前项目下创建：

```text
.journal-frontier-radar/
└── runs/
    └── YYYYMMDD-journal-period/
        ├── config.json
        ├── inventory.jsonl
        ├── reading-notes.jsonl
        ├── frontier-sources.jsonl
        ├── discovery-log.jsonl
        ├── metrics.json
        ├── access-ledger.md
        └── report.md
```

主要文件：

| 文件 | 内容 |
|---|---|
| `inventory.jsonl` | 文章全集、日期、DOI、类型、访问状态和发现来源 |
| `reading-notes.jsonl` | 逐篇研究问题、方法、结果、创新、局限、主题和关键词 |
| `frontier-sources.jsonl` | 期刊外部综述、共识、基准、原始研究和反面证据 |
| `discovery-log.jsonl` | archive、issue、搜索页和独立索引的覆盖证据 |
| `metrics.json` | 主题/关键词文档频率与时间动量 |
| `access-ledger.md` | 每篇文章的全文、摘要、仅元数据或访问失败标识 |
| `report.md` | 最终综合报告 |

详细字段见
[data-contract.md](skills/journal-frontier-radar/references/data-contract.md)。

## 确定性工具

初始化研究运行：

```bash
python skills/journal-frontier-radar/scripts/journal_radar.py init \
  --journal "Nature Communications" \
  --url "https://www.nature.com/ncomms/" \
  --period 6m \
  --language zh-CN
```

严格检查是否漏读、重复或日期越界：

```bash
python skills/journal-frontier-radar/scripts/journal_radar.py audit \
  .journal-frontier-radar/runs/<run-name> \
  --strict
```

计算主题和关键词指标：

```bash
python skills/journal-frontier-radar/scripts/journal_radar.py metrics \
  .journal-frontier-radar/runs/<run-name>
```

生成必须纳入报告的逐篇访问台账：

```bash
python skills/journal-frontier-radar/scripts/journal_radar.py ledger \
  .journal-frontier-radar/runs/<run-name>
```

Kimi WebBridge 客户端示例：

```bash
python skills/journal-frontier-radar/scripts/webbridge_client.py \
  --session nature-6m \
  navigate \
  --args-json '{"url":"https://www.nature.com/nature/research-articles","newTab":true,"group_title":"Nature近6个月研究"}'
```

## 质量边界

- “全部文章”必须由发现日志和数量核对支持。
- 先完成文章全集和逐篇阅读，再从文章开放编码中归纳主题；禁止预设主题框架。
- `[全文]` 表示实际打开并阅读文章正文，不等同于文章被标记为 Open Access。
- 最终报告必须逐篇显示 `[全文]`、`[摘要]`、`[仅元数据]` 或 `[访问失败]`。
- 标题不能作为研究结论的证据。
- 关键词频率不等于科学重要性。
- 发文量不等于科学或临床有效性。
- 期刊偏好不等于整个领域的研究前沿。
- 大语料可以分批处理，但不能静默改为抽样。
- 预印本、仅摘要来源、争议证据和推断必须明确标记。
- 任何开放问题都必须能追溯到具体文章或前沿来源。
- 未建立独立、完整、已审计的往年语料时，不得声称“较上一年上升”或“达到新高”。

## 常见问题

### `Unable to verify if domain ... is safe to fetch`

这说明 Claude Code 调用了内置 `Fetch`，而不是 Kimi WebBridge。停止当前运行，不要继续
用 Web Search 补文章。请依次检查：

1. 已加载最新版插件；
2. Kimi WebBridge 连通性命令成功；
3. 在 `/agents` 中使用 `journal-frontier-radar:journal-frontier-researcher`；
4. 在一个新 Claude Code 会话中重新运行。

新版插件规定：Kimi 不可用时必须停止，不能静默退回到 WebSearch/WebFetch。

### 报告没有逐篇全文/摘要标识

检查运行目录是否存在 `inventory.jsonl`、`reading-notes.jsonl` 和
`access-ledger.md`。如果只有一个最终 Markdown，说明执行契约没有完成，该报告不能
视为全量、可审计结果。重新运行插件，并在最终交付前执行：

```bash
python skills/journal-frontier-radar/scripts/journal_radar.py audit \
  .journal-frontier-radar/runs/<run-name> --strict --final
```

## 插件结构

```text
journal-frontier-radar/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── agents/journal-frontier-researcher.md
├── skills/journal-frontier-radar/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
├── scripts/validate_repo.py
├── examples/
└── .github/
```

## 开发与验证

```bash
python scripts/validate_repo.py
```

验证包括：

- Claude Code 与 Codex 清单 JSON；
- 插件名和技能名一致性；
- Skill YAML frontmatter；
- 相对路径指向的真实文件；
- Python 脚本语法；
- 日期窗口边界与闰年行为；
- 残留 TODO 占位符。

提交改动前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 隐私与安全

Kimi WebBridge 使用用户当前浏览器会话。插件只应在用户授权的页面上运行，并把研究
数据写入当前项目目录。不要把受版权或隐私限制的全文、登录凭据、Cookie 或令牌提交
到仓库。安全问题请参阅 [SECURITY.md](SECURITY.md)。

## 许可证

[MIT License](LICENSE)
