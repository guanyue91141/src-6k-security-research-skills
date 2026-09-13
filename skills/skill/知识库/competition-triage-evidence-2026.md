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
Candidate
  ↓
Controlled Test
  ↓
Differential Evidence
  ↓
Capability Delta
  ↓
Finding / Reject / Hold
```

AI 不允许从“200”“报错”“版本旧”“路径存在”“组件可枚举”直接跳到漏洞结论。

## 2. 六问闸门

每个 Candidate 至少回答：

1. **Attacker**：攻击者起点是什么？匿名、普通用户、某租户、开发者？
2. **Control**：攻击者真正控制哪个输入、对象或状态？
3. **Boundary**：跨过了哪条安全边界？认证、授权、租户、网络、信任域？
4. **Delta**：成功后新增了什么原本没有的能力？
5. **Evidence**：有没有可复核差分，不只是状态码/错误文本？
6. **Scope**：是否符合比赛题目或授权范围？

如果第 3/4/5 项答不清楚，默认继续验证或 Reject，不直接写漏洞。

## 3. 0–12 分 Candidate 评分

评分只决定验证顺序，不替代六问闸门。每项 0–2 分：

| 维度 | 0 | 1 | 2 |
|---|---|---|---|
| Boundary | 没有边界 | 边界可疑 | 明确跨身份/对象/租户/状态边界 |
| Capability Delta | 无新增能力 | 有有限增量 | 获得真实新能力 |
| Evidence | 只有单点信号 | 有部分对照 | 稳定 A/B 差分 |
| Reproducibility | 偶发/依赖脏状态 | 条件化复现 | 干净状态可稳定复现 |
| Impact | 仅表面信息 | 有限业务影响 | 明确业务/跨主体影响 |
| Efficiency | 验证成本高 | 中等 | 少量受控步骤即可确认/证伪 |

推荐解释：

- `9–12`：A 队列，优先闭环；
- `6–8`：B 队列，补关键证据；
- `0–5`：C 队列，只做最小证伪，不投入长链。

硬阻断项不参与加分：超范围、不可回滚、真实资损、无法安全验证、无法复现时直接 Hold/Reject。

## 4. 最小差分证据

优先构造 A/B 对照：

| 类型 | A 基线 | B 测试 | 真正有价值的差分 |
|---|---|---|---|
| 对象授权 | 自己对象 | 其他对象 | 返回主体真正改变 |
| 身份边界 | 正常身份 | 匿名/低权限 | 获得原本禁止的能力 |
| API Version | 当前版本 | 旧版本 | 安全控制退化 |
| Cache | 用户 A | 用户 B/新会话 | 私有数据跨主体复用 |
| CI/CD | 低信任输入 | 高权限 job | 输入跨入高权限执行/secret 域 |
| Cloud/K8s | 当前 token | 权限查询 | 实际 grants 超出预期 |
| 状态机 | 合法顺序 | 跳步/重复动作 | 终态或权益不变量被破坏 |

## 5. Parser / WAF / Auth 层级误判

常见假阳性：

- malformed body 返回 400，不代表已经绕过 auth；
- WAF/CDN 403/200 不代表 origin 行为；
- GraphQL introspection 不代表越权；
- gRPC reflection 不代表敏感方法可调用；
- Kubernetes `/version` 或资源列表不代表高权限；
- 旧 API 返回 200 不代表它还执行真实业务；
- source map、JS 路由和接口名只说明 surface 存在，不说明边界被突破。

验证身份/授权时，优先使用**最简单的合法请求结构**，避免先被 parser 拦住后误判层级。

## 6. Invariant-first

对复杂业务，不要从 payload 开始，先定义 invariant：

- 用户只能读取属于自己的对象；
- 优惠只能消费一次；
- 审批完成前不能进入终态；
- 租户 A 不能影响租户 B；
- 未经授权的输入不能进入高权限执行域；
- token 只能用于预期 audience；
- cache 不得跨身份复用私有响应；
- 异步回调必须绑定原始业务对象并保持幂等。

然后沿数据流找破坏 invariant 的点。

## 7. 比赛模式优先级

时间有限时，优先测试：

1. 有真实业务对象的授权边界；
2. 认证、找回、多因素认证、session 状态机；
3. Shadow API / 旧客户端接口；
4. Mobile-only API 与 source map 暴露的隐藏业务面；
5. 文件/对象存储/签名链；
6. 服务端 fetch 与异步回调；
7. GraphQL/gRPC/WebSocket 多协议授权差异；
8. Next.js/SSR/RSC/cache 边界；
9. CI/CD/K8s/云身份暴露面；
10. 注入类按真实 sink 和技术栈定向测试。

不是按列表机械轮询；命中高质量差分面就深入闭环。

## 8. Stop / Continue 规则

一个 Candidate 被 Reject，只代表**这一条线索死亡**，不代表目标安全。

连续两次受控验证都没有增加 `Boundary / Capability Delta / Evidence` 任一项时，当前 Candidate 默认停止并切换下一条。除非新信息改变假设，否则不要继续在同一弱信号上重复消耗。

Reject 原因统一记录：

- `no_boundary_crossed`
- `no_capability_delta`
- `false_positive_layering`
- `expected_behavior`
- `out_of_scope`
- `not_reproducible`
- `insufficient_evidence`
- `duplicate_surface`

`Hold` 用于缺少第二账号、缺少测试数据、依赖比赛环境后续阶段等情况。

## 9. Candidate Board

赛中统一维护：

```text
ID | Surface | Hypothesis | Score | Queue | Boundary | Delta | Evidence | Status | Next Action
```

状态只使用：`queued / testing / confirmed / rejected / hold`。

每完成一次验证必须更新：

- score 是否变化；
- 哪个维度增加/下降；
- 下一步是否仍是最小判定动作；
- 是否应从 A/B/C 队列迁移。

这样可以避免“开了很多页面，但没有真正推进候选”的假进度。

## 10. Finding 最小结构

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

## 11. 赛后复盘

每场比赛只统计三件事：

1. 哪些 confirmed Candidate 在最早阶段就有高分信号；
2. 哪些 rejected Candidate 消耗最多时间，以及当时缺失哪个判定条件；
3. 哪些 hold Candidate 值得下次优先补账号、环境或数据条件。

优化下一场比赛时，优先修改评分权重、入口路由与假阳性规则，不要只增加更多知识文件。

## 12. 与现有规则联动

本专题补充 `rules/05-testing-policy.md` 的 Evidence-First 模型，不替代现有 reporting 规则。比赛入口由 `workflows/competition-mode.md` 调度，正式报告仍由 `rules/06-reporting.md` 控制。