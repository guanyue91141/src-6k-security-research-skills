---
id: dependency-confusion
title: 依赖混淆
category: injection
status: legacy
last_reviewed: 2026-09
purpose: 现场识别内部包名后才打，不靠教材默认覆盖。
triggers:
- 内部包名
- 私有 registry
- 依赖混淆
inputs:
- 依赖清单或包名
outputs:
- 供应链污染证据或 N/A
related:
- agent-skill-supply-chain-2026.md
---

# dependency-confusion-test（几乎不交）

> 依赖混淆默认不写。供应链/内部包名现场认到再打，不靠本篇教材。
