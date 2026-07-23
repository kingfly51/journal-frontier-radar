# Example prompts

## 综合期刊雷达

```text
使用 $journal-frontier-radar 分析 Nature Communications 最近6个月的全部科学文章。
以首次在线发表日期为边界，逐篇阅读可访问全文，使用 Crossref 或 PubMed 核对完整性。
用中文输出主题占比、关键词、时间动量、外部领域前沿和可检验的开放科学问题。
```

## 医学期刊

```text
分析 The Lancet Digital Health 最近1年的 Research、Review 和 Comment。
对涉及临床性能的结论检查外部验证、样本代表性和偏倚风险。
把期刊关注热点与数字医疗领域已经建立的证据分开报告。
```

## 方法学期刊

```text
分析 Nature Methods 最近3个月的文章。
重点提取新技术解决的瓶颈、性能基准、适用边界、复现条件和仍缺少的对照实验。
对每个主要技术方向提出一个可证伪的后续研究问题。
```

## 仅摘要限制

```text
分析指定期刊最近2个月的文章。如果遇到付费墙，不得尝试绕过。
完整保留文章记录并标为 abstract_only；最终报告单独说明哪些结论主要依赖摘要。
```

## 比较时间动量

```text
分析期刊最近2年的文章，把窗口分成前后两半，比较各主题的标准化占比变化。
识别上升主题时同时报告分子、分母和代表文章，不要只输出趋势形容词。
```

## Claude Code 调用

将以上提示中的 `$journal-frontier-radar` 替换为：

```text
/journal-frontier-radar:journal-frontier-radar
```
