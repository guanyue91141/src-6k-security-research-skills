---
id: clickjacking
title: Clickjacking 与嵌框防护
category: client
status: mixed
last_reviewed: 2026-09
purpose: 审查页面是否需要被第三方嵌入，以及敏感界面的 framing 防护匹配度。
triggers:
- X-Frame-Options
- frame-ancestors
- 嵌框
- iframe
inputs:
- 敏感页面
outputs:
- 嵌框证据或 N/A
related:
- csrf-test.md
- csp-bypass-test.md
---

# Clickjacking / Framing 安全背景（2026）

单独缺少 framing 防护头不直接作为高价值结论。本专题用于审查页面是否需要被第三方嵌入，以及敏感界面是否具有与其风险相匹配的浏览器防护。

现代基线：

- 优先使用 CSP `frame-ancestors` 表达允许嵌入来源；
- `X-Frame-Options` 作为历史兼容层继续保留；
- iframe 场景同时检查 `sandbox`、`allow` 与 postMessage 信任边界；
- 本来就设计成嵌入式组件的页面，应使用明确 allowlist，而不是简单全部禁止；
- 浏览器 framing 防护不能替代服务端身份、对象授权与高风险操作确认。

相关专题：`csrf-test.md`、`csp-bypass-test.md`、`xss-test.md`。
