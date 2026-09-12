---
status: current
last_reviewed: 2026-09
sources:
  - MoonFuji/invariant-first-bug-bounty
  - murrtada/bug-bounty-agent-skills:triage-validation
---

# 网安比赛 / SRC 候选漏洞证据闸门 2026

> 目标：让 AI 少在假阳性、弱影响和重复线索上浪费时间，把精力留给能闭环的候选漏洞。

## 1. Candidate 不等于 Finding

所有线索先进入 Candidate：

```text
Signal
  ↓
Hypothesis
  ↓
Controlled Test
  ↓
Differential Evidence
  ↓
Capability Delta
  ↓
Finding / Reject / Hold
```

AI 不允许从“200”“报错”“版本旧”“路径存在”直接跳到漏洞结论。

## 2. 六问闸门

每个 Candidate 至少回答：

1. **Attacker**：攻击者起点是什么？匿名、普通用户、某租户、开发者？
2. **Control**：攻击者真正控制哪个输入、对象或状态？
3. **Boundary**：跨过了哪条安全边界？认证、授权、租户、网络、信任域？
4. **Delta**：成功后新增了什么原本没有的能力？
5. **Evidence**：有没有可复核差分，不只是状态码/错误文本？
6. **Scope**：是否符合比赛题目或授权范围？

如果第 3/4/5 项答不清楚，默认继续验证或 Reject，不直接写漏洞。

## 3. 最小差分证据

优先构造 A/B 对照：

| 类型 | A 基线 | B 测试 | 真正有价值的差分 |
|---|---|---|---|
| IDOR | 自己对象 | 其他对象 | 返回主体真正改变 |
| Auth | 有效身份 | 匿名/低权限 | 获得原本禁止的能力 |
| API Version | 当前版本 | 旧版本 | 安全控制退化 |
| Cache | 用户 A | 用户 B/新会话 | 私有数据跨主体复用 |
| CI/CD | 低信任输入 | 高权限 job | 输入跨入高权限执行/secret 域 |
| Cloud/K8s | 当前 token | 权限查询 | 实际 grants 超出预期 |

## 4. Parser / WAF / Auth 层级误判

常见假阳性：

- malformed body 返回 400，不代表已经绕过 auth；
- WAF/CDN 403/200 不代表 origin 行为；
- GraphQL introspection 不代表越权；
- gRPC reflection 不代表敏感方法可调用；
- Kubernetes `/version` 或资源列表不代表 cluster-admin；
- 旧 API 返回 200 不代表它还执行真实业务。

验证身份/授权时，优先使用**最简单的合法请求结构**，避免先被 parser 拦住后误判层级。

## 5. Invariant-first

对复杂业务，不要从 payload 开始，先定义 invariant：

- 用户只能读取属于自己的对象；
- 优惠只能消费一次；
- 审批完成前不能进入终态；
- 租户 A 不能影响租户 B；
- 未经授权的输入不能进入高权限 CI/CD；
- token 只能用于预期 audience；
- cache 不得跨身份复用私有响应。

然后沿数据流找破坏 invariant 的点。

## 6. 比赛模式优先级

时间有限时，优先测试：

1. 有真实业务对象的 BOLA/BFLA；
2. 认证/找回/MFA/session 状态机；
3. Shadow API / 旧客户端接口；
4. 文件上传/对象存储/签名链；
5. SSRF / Server-side fetch；
6. GraphQL/gRPC/WebSocket 多协议授权差异；
7. Next.js/SSR/RSC/cache 边界；
8. CI/CD/K8s/云身份暴露面；
9. 注入类按真实 sink 和技术栈定向测试。

不是按列表机械轮询；命中高质量差分面就深入闭环。

## 7. Stop / Continue 规则

一个 Candidate 被 Reject，只代表**这一条线索死亡**，不代表目标安全。

Reject 原因统一记录：

- `no_boundary_crossed`
- `no_capability_delta`
- `false_positive_layering`
- `expected_behavior`
- `out_of_scope`
- `not_reproducible`
- `insufficient_evidence`

`Hold` 用于缺少第二账号、缺少测试数据、依赖比赛环境后续阶段等情况。

## 8. Finding 最小结构

最终候选至少包含：

```text
Title
Attacker model
Precondition
Invariant / security boundary
Baseline
Test
Differential evidence
Capability gained
Impact
Confidence
Cleanup / rollback
```

比赛答题时可以压缩表达，但内部 state 不要省略这些字段。

## 9. 与现有规则联动

本专题补充 `rules/05-testing-policy.md` 的 Evidence-First 模型，不替代现有 reporting 规则。正式报告仍由 `rules/06-reporting.md` 控制。
