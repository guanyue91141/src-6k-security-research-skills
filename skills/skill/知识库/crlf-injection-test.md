---
id: crlf-injection
title: CRLF 头注入
category: injection
status: legacy
last_reviewed: 2026-09
purpose: 说明纯 CRLF 头注入默认不交，Host 投毒转 Host 专题。
triggers:
- CRLF
- 响应拆分
- 头注入
inputs:
- 头可控参数
outputs:
- 链路证据或 N/A
related:
- http-host-header-test.md
- ghost-bits-cast-test.md
---

# crlf-injection-test（几乎不交）

> 纯 CRLF 头注入默认不写。Host 毒重置走 `http-host-header-test.md`。Ghost Bits 邮件/走私用公式 `chr((k<<8)|T)`，见 `ghost-bits-cast-test.md`。
