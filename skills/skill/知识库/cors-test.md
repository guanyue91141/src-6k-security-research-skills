---
id: cors
title: CORS（仅技术资料，SRC 停用）
category: disabled
status: disabled
last_reviewed: 2026-09
purpose: 永久停用：不做 CORS 测试、不写 CORS 报告；跨站写转 CSRF，跨权读转授权。
triggers: []
inputs: []
outputs: []
related:
- csrf-test.md
- idor-test.md
---

# cors（仅技术资料 · SRC 禁用）

> **永久强制：** SRC 黑盒 CORS **不挖、不测、勿开本篇**（`rules/01-safety-boundary.md`）。看到 ACAO/ACAC → 立刻转注入 / SSRF / XSS / RCE / 越权 / 未授权业务读。写不写只认 `rules/06-reporting.md`。
