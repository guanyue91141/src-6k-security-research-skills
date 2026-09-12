# CSP / Trusted Types 安全审查（2026）

> status: current  
> last_reviewed: 2026-09

单独“绕过 CSP”不作为本项目的主漏洞类型；本文件用于 XSS 防御架构审查，并与 `xss-test.md` 联动。

## 现代基线

- 优先采用基于 nonce/hash 的 CSP，而不是维护庞大的域名 allowlist。
- 对动态脚本加载评估 `strict-dynamic` 的使用和浏览器兼容策略。
- 避免 `unsafe-inline`、`unsafe-eval` 成为长期默认配置。
- `object-src 'none'`、合理的 `base-uri` 与 frame 控制应作为常见基线。
- 报告模式 `Content-Security-Policy-Report-Only` 用于上线前观测，但不能替代正式 enforcement policy。

## Trusted Types

对大量 DOM 操作的前端应用，Trusted Types 是 2026 年重要的 DOM XSS 防御层。审查：

- 是否启用 `require-trusted-types-for 'script'`；
- Trusted Types policy 是否集中、最小化；
- policy 是否只是把任意字符串原样标记为可信；
- 第三方组件是否迫使应用回退到宽松 policy；
- `innerHTML`、脚本 URL 等危险 sink 是否逐步迁移到受控接口。

## CSP 审查思路

CSP 的目标是降低 XSS 成功后的执行能力，因此结论应结合真实注入上下文判断。仅发现缺少某个 CSP 指令、某域在 allowlist 或 policy 可优化，不直接等同于可利用 XSS。

## 与其它专题联动

- 实际注入与 DOM sink：`xss-test.md`
- Open Redirect / URL 跳转：`open-redirect-test.md`
- iframe / framing：`clickjacking-test.md`
- 现代前端状态与 API：`js-reverse-guide.md`
