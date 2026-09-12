---
status: current
last_reviewed: 2026-09
sources:
  - murrtada/bug-bounty-agent-skills:hunt-grpc
  - OWASP API Security Top 10 2023
---

# gRPC / Protobuf 安全审查 2026

> 用于授权比赛、CTF、SRC 和白盒审计。目标是识别 gRPC 服务边界、认证授权差异与网关转换问题；默认采用只读、低影响验证。

## 1. 为什么单独成篇

gRPC 的风险往往不在 Protobuf 本身，而在四层边界不一致：

1. 浏览器/REST/gRPC-Web/Connect 对外入口；
2. Envoy、grpc-gateway、Ingress 等转换层；
3. 原生 gRPC 服务与 metadata；
4. 服务间身份、mTLS 与方法级授权。

比赛中高价值问题常表现为：外层网关有限制，但同一后端 RPC 的另一条入口没有等价限制。

## 2. 识别信号

优先关注：

- HTTP/2 + `application/grpc` / `application/grpc-web*`；
- `grpc-status`、`grpc-message` 响应头/Trailer；
- `.proto`、descriptor、Swagger/OpenAPI 转换产物；
- 前端出现 gRPC-Web、Connect、Buf、Envoy、grpc-gateway；
- 常见服务名：`UserService`、`AdminService`、`InternalService`、`PaymentService`；
- 端口只是线索，不把 50051/9090 本身当漏洞。

## 3. 建模方式

对每个服务建立：

| 维度 | 记录内容 |
|---|---|
| service / method | RPC 全名 |
| request message | 对象 ID、租户 ID、角色、分页、批量字段 |
| authn | Cookie、Bearer、mTLS、metadata、网关身份 |
| authz | 方法级、对象级、字段级 |
| exposure | native gRPC / gRPC-Web / JSON transcoding / Connect |
| evidence | 正常基线、低权限差分、拒绝状态 |

不要把 reflection 开启本身直接认定为高危；它主要是攻击面枚举器。

## 4. 重点审查面

### 4.1 Reflection 与 schema

- Reflection 是否暴露完整服务目录；
- 生产环境是否同时泄露 `.proto` / descriptor；
- schema 中是否出现内部、管理、调试方法；
- 关闭 Reflection 后，网关/OpenAPI 是否仍泄露同一面。

### 4.2 身份与 metadata 信任

检查“谁负责写入、谁负责验证”：

- 用户身份、租户、角色是否只在边缘代理验证；
- 后端是否盲信代理注入的 metadata；
- 外部请求能否影响这些身份字段；
- 原生 gRPC 与转码入口是否执行相同授权策略。

核心不是伪造某个固定 Header 名，而是判断 **身份声明是否有可信来源和不可伪造的绑定**。

### 4.3 BOLA / BFLA / 批量 RPC

把 gRPC method 当普通 API 方法审查：

- 对象 ID 是否绑定当前主体；
- 管理型 RPC 是否做功能级授权；
- repeated/map 字段是否允许批量跨对象操作；
- stream 中后续消息是否持续校验身份与租户；
- subscription/watch 是否可能越权收到其他主体事件。

### 4.4 Transcoding 差异

同一后端 RPC 可能同时由以下入口暴露：

- native gRPC；
- grpc-gateway REST；
- Envoy JSON transcoder；
- gRPC-Web；
- Connect JSON/Protobuf。

重点做**行为差分**：认证、字段默认值、重复字段、大小限制、错误处理和方法可见性是否一致。

### 4.5 资源消耗

只做静态/低影响判断：

- message size 上限；
- unary 与 streaming 的配额；
- 单连接 stream 数；
- deadline / timeout；
- cancellation 后是否及时释放资源。

未经明确授权，不做 Rapid Reset、流量型或资源耗尽验证。

## 5. 白盒审计

搜索：

- interceptor 是否统一注册；
- 方法是否绕过 auth interceptor；
- 服务间身份是否来自可控 metadata；
- protobuf 字段是否直接映射 ORM/update object；
- `oneof`、optional/default 值是否产生授权绕过；
- 网关生成代码与原生服务是否使用相同 policy。

## 6. 证据闸门

只有以下差分才升级为 Finding：

- 低权限/未认证主体获得本不应具有的业务能力；
- 不同入口对同一 RPC 的授权结果不一致；
- 能读取其他用户/租户数据；
- 管理方法被低权限调用；
- schema 泄露能进一步闭环到真实安全影响。

Reflection、服务名、版本号、`UNIMPLEMENTED` 等只作为 Signal。

## 7. 与现有专题联动

- 对象/功能授权 → `api-security-review.md`、`idor-test.md`
- HTTP/2/代理转换 → `http2-attacks-test.md`
- Shadow API → `shadow-api-inventory-2026.md`
- GraphQL/多协议 API → `graphql-modern-2026.md`
- Kubernetes / service mesh → `k8s-security-review-2026.md`
