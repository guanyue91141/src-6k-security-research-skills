---
id: hpp
title: HTTP 参数污染
category: injection
status: legacy
last_reviewed: 2026-09
purpose: 说明参数污染本身不单独交，只作为越权/注入的成因。
triggers:
- 参数污染
- 重复参数
- 数组参数
inputs:
- 多值参数接口
outputs:
- 作为成因的越权/注入证据
related:
- idor-test.md
- injection-test.md
---

# hpp-test（几乎不交）

> HTTP 参数污染本身不交。污染导致越权/注入按那个洞写，走 `idor-test.md` / `injection-test.md`。
