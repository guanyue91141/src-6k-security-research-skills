---
id: dangling-markup
title: 悬空标记抽取 token
category: client
status: legacy
last_reviewed: 2026-09
purpose: 说明悬空标记抽 CSRF/token 半条链默认不交，现场 XSS 回显转 XSS 专题。
triggers:
- 悬空标记
- 半截标签
- token 抽取
inputs:
- 可控 HTML 上下文
outputs:
- 链路证据或 N/A
related:
- xss-test.md
- csrf-test.md
---

# dangling-markup-test（几乎不交）

> 悬空标记抽 CSRF/token 半条链默认不写。现场 XSS 回显仍走 `xss-test.md`。
