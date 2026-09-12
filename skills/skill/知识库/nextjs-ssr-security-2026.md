---
status: current
last_reviewed: 2026-09
sources:
  - murrtada/bug-bounty-agent-skills:hunt-nextjs
---

# Next.js / React SSR 安全审查 2026

> 面向授权比赛、SRC 与白盒审计。重点不是“看到 Next.js 就套 CVE”，而是理解 App Router、Server Actions、RSC、Middleware、缓存与图片优化形成的新边界。

## 1. 识别面

常见信号：

- `/_next/static/`、`/_next/image`、`__NEXT_DATA__`；
- RSC/Flight 响应；
- App Router、Server Actions；
- ISR/SSG/SSR 混合；
- `x-nextjs-*`、Vercel/Edge Runtime；
- source map、构建 ID、route manifest。

先记录 framework/version/deployment 模式，再决定是否参考特定 CVE。

## 2. Server / Client 边界

重点问：

- 业务授权是在服务端执行，还是只靠 UI 隐藏按钮；
- Server Action 是否把客户端提供的对象/租户 ID 当可信值；
- action 与传统 API route 是否使用相同 policy；
- 服务端读取到的 secret 是否意外进入客户端序列化数据；
- 页面组件不可见是否只是 client-side 条件，而不是真正授权。

## 3. RSC / Server Props 数据暴露

检查：

- RSC Flight payload 是否包含不应下发的服务器字段；
- `__NEXT_DATA__` / page props 中是否出现内部对象；
- 页面只显示脱敏值，但序列化数据是否仍含完整值；
- SSR 错误边界是否把 stack/context 带到客户端。

“客户端没有渲染”不等于“客户端没有收到”。

## 4. Middleware 与 Route Matcher

Middleware 是高频误判点。审查：

- matcher 是否覆盖 API、data route、locale、rewrite 后路径；
- auth 是否只放在 middleware，而业务 handler 不做第二层校验；
- rewrite/redirect 后是否进入未受保护 handler；
- App Router、Route Handler、Server Action 是否采用不同授权组件。

结论必须基于**最终业务能力差分**，不能只因某条路径经过不同 middleware 就报漏洞。

## 5. `/_next/data`、预渲染与对象授权

对于 Pages Router/SSG/ISR 项目：

- 预渲染 JSON 是否包含用户/租户数据；
- 动态路由对象 ID 是否做主体绑定；
- 页面 HTML 受保护，但数据 endpoint 是否具有等价授权；
- cache key 是否包含用户/租户身份。

## 6. Image Optimization / 服务端取 URL

`/_next/image` 或自定义 image loader 只在服务端真正发起请求时才进入 SSRF 模型。

审查：

- remote pattern/domain allowlist；
- redirect 后是否重新验证目标；
- DNS 解析后是否检查私网/链路本地地址；
- scheme、port 与最终 IP 是否受控；
- 响应内容是否只作为图像处理，而不是原样代理。

状态码本身不能证明 SSRF；需要可靠的服务器端请求证据。

## 7. Cache / ISR / Revalidation

结合 `cache-modern-2026.md` 检查：

- cache key 是否遗漏身份、locale、tenant、header；
- personalized SSR 是否误进入共享缓存；
- revalidation endpoint 是否有服务端授权；
- stale-while-revalidate 期间是否跨主体返回旧对象；
- Edge/CDN 与 Next.js 自身缓存是否使用不同规范化。

## 8. Source Map 与构建产物

source map 价值主要在恢复：

- 内部 API path；
- feature flag；
- Server Action/route 名称；
- 错误处理逻辑；
- 不应进入浏览器 bundle 的 secret/credential。

只有恢复源码而无安全影响通常是信息线索，不直接抬高定级。

## 9. Dev / Debug 模式

检查生产环境是否意外运行开发模式或暴露调试路由。必须区分：

- 真实 dev server；
- CDN/WAF 自定义 404；
- source map 暴露；
- framework 正常生产行为。

## 10. 比赛快速矩阵

看到 Next.js 后优先：

1. 枚举公开 route/API/Server Action 面；
2. 对有业务对象的页面做 BOLA/BFLA；
3. 检查 RSC/`__NEXT_DATA__` 数据超集；
4. 检查 image/server fetch 与 cache 边界；
5. 检查 source map 与历史 API；
6. 结合具体版本再查 CVE，不反过来。

## 11. 联动

- API 对象/功能授权 → `api-security-review.md`
- RSC/API 历史面 → `shadow-api-inventory-2026.md`
- 缓存 → `cache-modern-2026.md`
- 服务端 URL 获取 → `ssrf-test.md`
- XSS/Trusted Types → `xss-test.md`、`csp-bypass-test.md`
