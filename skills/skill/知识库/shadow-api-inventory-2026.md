---
status: current
last_reviewed: 2026-09
sources:
  - murrtada/bug-bounty-agent-skills:hunt-shadow-api
  - OWASP API Security Top 10 2023 API9
---

# Shadow / Zombie API 资产与差分审查 2026

> 用于授权测试、比赛和白盒审计。该专题负责“找出仍然活着但已经不在当前产品主路径里的 API”，再把具体漏洞交给对应专题验证。

## 1. 核心思想

旧 API 真正的价值通常不是“版本旧”，而是**安全控制没有同步回填**。

常见差异：

- 新版本要求登录，旧版本仍匿名；
- 新版本加了对象/租户授权，旧版本没有；
- 新版本删掉敏感字段，旧版本仍返回；
- 新版本有速率/验证码/状态机，旧版本仍沿用旧逻辑；
- Web 已迁移，但移动端、合作方、旧 SDK 仍指向老入口。

## 2. 版本面清单

建立版本矩阵，不依赖固定 `v1/v2`：

| 类型 | 示例 |
|---|---|
| path | `/v1/`、`/v2/`、日期版、`legacy/old/beta` |
| header | `Accept` vendor media type、版本 Header |
| host | `api-v1`、`legacy-api`、移动端专用 host |
| client | Web、APP、旧 APK/IPA、桌面端、合作 SDK |
| spec | OpenAPI/Swagger/Postman/proto 历史版本 |

## 3. Spec 与客户端驱动发现

优先从真实证据恢复历史面：

- 当前和历史 OpenAPI/Swagger；
- 前端 JS source map / chunk；
- APK/IPA、桌面客户端中的 base URL；
- SDK、示例代码、文档；
- Git history / release note / changelog；
- 归档网页只作为候选来源，最终必须回到当前可达资产验证。

## 4. 行为差分

对于同一业务操作，比较旧/新入口：

### 认证
- 是否都需要等价身份；
- token/session 生命周期规则是否一致；
- 旧入口是否遗漏 MFA/step-up。

### 授权
- 对象 ID、tenant/org/app 字段是否在两版都绑定主体；
- 管理功能是否都做功能级授权；
- 批量/导出/异步 job 是否沿用旧授权模型。

### 数据暴露
- 响应字段是否多出内部字段、PII、调试信息；
- pagination、total、export 是否暴露更大数据范围。

### 安全控制
- 输入 schema、文件类型、上传处理是否一致；
- 速率限制、验证码、幂等、重放控制是否一致；
- cache、CORS、网关策略是否只部署在新版本。

## 5. False-positive Gate

以下不单独算漏洞：

- 旧 path 返回 200，但只是 deprecated 提示页；
- response shape 不同，但权限和数据边界相同；
- 版本号不同，但实际都代理到同一个实现；
- 历史 spec 中存在 endpoint，但现在已经不可达。

只有出现**真实安全行为回退**才升级 Finding。

## 6. 比赛中的快速使用

遇到以下信号时立即开本专题：

- 前端调用 `/v3`，但 APK 里还出现 `/v1`；
- Swagger `info.version` 与实际 base path 不一致；
- 同一个对象在不同版本返回字段明显不同；
- 新接口 401/403，旧接口返回业务 JSON；
- 文档宣布 deprecated，但 endpoint 仍执行真实业务。

## 7. 联动

- API 授权 → `api-security-review.md`
- IDOR/BOLA/BFLA → `idor-test.md`
- gRPC/proto 旧版本 → `grpc-security-2026.md`
- JS/API 历史入口 → `js-reverse-guide.md`
- 移动端入口 → 后续 `mobile-api-surface-2026.md`
