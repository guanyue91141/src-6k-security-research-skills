---
status: current
last_reviewed: 2026-09
sources:
  - https://vite.dev/config/build-options
  - https://nextjs.org/docs/pages/api-reference/config/next-config-js/productionBrowserSourceMaps
  - https://developer.chrome.com/docs/devtools/developer-resources
---

# SPA / Source Map / API Recovery 2026

面向 Vite、Next.js、Webpack/Rollup/Rolldown、React/Vue 等现代前端构建产物的授权分析专题。目标不是“看到 `.map` 就报漏洞”，而是从前端构建产物恢复真实业务入口、API schema、版本线索和隐藏功能，再交给对应专题验证服务端边界。

## 1. 现代构建事实

Vite 官方配置中 `build.sourcemap` 默认是 `false`，可配置为独立、inline 或 hidden sourcemap。Next.js 生产浏览器 sourcemap 默认关闭，只有显式启用 `productionBrowserSourceMaps` 才会输出并由应用提供。

因此：

- source map 暴露不是所有框架的默认现象；
- `.map` 存在不等于安全漏洞；
- 真正价值取决于恢复出的服务端能力、secret、隐藏 endpoint 或安全假设。

## 2. 恢复目标

从 JS/chunk/source map 优先恢复：

- API base URL；
- route / endpoint；
- GraphQL operation 名；
- gRPC-Web / Connect service；
- WebSocket/SSE 地址；
- feature flag；
- admin/internal/legacy 页面；
- OAuth redirect/issuer/client 配置；
- object storage/upload endpoint；
- mobile/Web 共用接口；
- error code / enum / state machine；
- hidden form fields / object schema；
- API version；
- source file path 与模块边界。

## 3. Chunk Inventory

先做“文件清单”而不是盲目全文搜索：

```text
entry
runtime
vendor
route chunks
lazy chunks
worker
service worker
wasm
source maps
```

记录：

```text
url
hash
size
route_hint
map_available
first_party_ratio
framework
```

现代 SPA 大量使用代码分割，隐藏功能往往只存在于 lazy route chunk。

## 4. Source Map 价值判断

source map 可能提供：

- 原始文件名；
- `sourcesContent`；
- TypeScript/JSX 原代码；
- 注释；
- 未压缩 symbol；
- API client 定义；
- schema/type；
- 路由和业务状态。

但以下通常只是信息：

- 普通组件源码；
- 开源依赖源码；
- 不含敏感能力的目录结构；
- 浏览器本来就必须拿到的 public 配置。

## 5. Hidden / Unlinked Route Recovery

前端路由中重点识别：

- admin；
- internal；
- debug；
- beta；
- legacy；
- experiment；
- import/export；
- billing；
- approval；
- support/impersonation；
- feature-flag only page。

恢复页面路径后不要直接认为“隐藏页面=越权”，而是继续测试对应服务端 API 的认证和功能授权。

## 6. API Client Recovery

现代前端 API 常见封装：

- fetch wrapper；
- Axios client；
- generated OpenAPI client；
- GraphQL client；
- tRPC/RPC client；
- Server Action bridge；
- gRPC-Web/Connect client。

优先整理：

```text
method
path
request shape
response type
auth source
error codes
version
calling route
```

然后与 `api-security-review.md`、`graphql-modern-2026.md`、`grpc-security-2026.md` 联动。

## 7. Schema / Type Recovery

TypeScript interface、Zod schema、generated SDK 类型非常有价值，因为它们能暴露：

- 客户端未显示字段；
- role/status enum；
- owner/tenant/userId；
- optional 管理字段；
- internal object ID；
- batch/export/job 参数。

但客户端 schema 只是线索。真正安全结论必须由服务端行为确认。

## 8. Environment / Public Config

常见公开配置：

- `NEXT_PUBLIC_*`；
- `VITE_*`；
- public analytics/project identifiers；
- API origin；
- feature flags。

这些值本身通常不是 secret。

判断标准：

> 这个值是否提供了浏览器正常运行之外的新服务端能力？

如果否，只记录为资产信息。

## 9. Next.js / RSC 联动

Next.js 目标同时检查：

- App Router route chunks；
- RSC/Flight 数据；
- Server Actions 标识；
- `/_next/data`（Pages Router 场景）；
- production source map；
- public runtime config；
- middleware/route handler 边界。

具体安全判断交给 `nextjs-ssr-security-2026.md`。

## 10. Vite / ESM 特征

Vite/现代 ESM 构建常见：

- hashed assets；
- dynamic `import()`；
- manifest；
- `import.meta.env`；
- preloaded module graph；
- lazy route modules。

若发现 source map，应优先恢复第一方 source，而不是把时间花在 vendor 依赖。

## 11. Service Worker / Web Worker

不要漏掉：

- service worker 缓存策略；
- background sync；
- push handler；
- worker 内 API base URL；
- offline route；
- token/message passing。

它们经常包含主 bundle 没有的 endpoint。

## 12. API Version Drift

如果旧 JS/chunk/CDN 缓存或历史 build 仍可访问，比较：

- endpoint inventory；
- API version；
- auth header；
- request fields；
- removed admin/internal action。

联动 `shadow-api-inventory-2026.md`，重点看“当前前端已删除，但旧服务端仍有效”的能力。

## 13. 比赛快速流程

```text
HTML
 ↓
entry + route chunks
 ↓
framework / build fingerprint
 ↓
source map / sourcesContent
 ↓
API clients + schemas + routes
 ↓
first-party endpoint inventory
 ↓
API/GraphQL/gRPC/Next.js 专题
 ↓
capability delta
```

时间有限时优先：

1. lazy/admin/internal route；
2. generated API client；
3. TypeScript enum/schema；
4. old API version；
5. upload/export/job endpoint；
6. GraphQL/gRPC descriptor；
7. source map 中真正的 privilege-bearing secret。

## 14. 误报控制

以下通常不能单独报告：

- production source map 可下载；
- 前端源码可读；
- API endpoint 被发现；
- public env/config；
- route 名含 admin 但服务端正确授权；
- JS 中存在已废弃 endpoint 且服务端不可达。

至少应进一步证明服务端授权、敏感信息或业务能力发生实际安全差异。

## 15. 防御基线

- 生产 sourcemap 按业务需要决定是否公开；
- secret 永远不进入前端 bundle；
- 隐藏 UI 不能代替服务端授权；
- old build/API 做生命周期治理；
- 服务端 schema/字段权限独立于客户端；
- feature flag 不作为访问控制；
- lazy route 同样遵守认证授权；
- CI 对 source map/public config 做敏感信息扫描。

## References

- Vite Build Options: `build.sourcemap`
- Next.js `productionBrowserSourceMaps`
- Chrome DevTools Developer Resources / Source Maps
