# Security Policy

## Supported versions

安全修复优先应用于最新发布版本和 `main` 分支。

## Reporting a vulnerability

请使用 GitHub 仓库的私密漏洞报告功能提交安全问题。不要在公开 Issue 中发布：

- 浏览器会话、Cookie 或身份验证令牌；
- 可导致任意代码执行的 WebBridge 输入；
- 未公开的出版商访问控制缺陷；
- 包含个人信息或受限全文的运行数据。

报告中请包含受影响版本、复现步骤、影响范围和建议缓解措施。维护者会尽快确认收到
报告，并在修复可用后协调披露。

## Security boundaries

- 插件只连接本机 `127.0.0.1:10086` 上的 Kimi WebBridge。
- 插件不得绕过验证码、付费墙、robots 约束或其他访问控制。
- `evaluate` 能在当前页面执行 JavaScript，应限制为读取页面状态、滚动和必要交互。
- 不要在命令行参数、日志、JSONL 研究记录或 Git 提交中保存凭据。
- 浏览器标签组仅在用户明确要求时关闭。
- 下载的 PDF 和补充材料应视为不可信输入。
