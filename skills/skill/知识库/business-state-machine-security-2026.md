---
status: current
last_reviewed: 2026-09
sources:
  - https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/06-Testing_for_the_Circumvention_of_Work_Flows/
  - https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/10-Business_Logic_Testing/
  - https://portswigger.net/web-security/logic-flaws
---

# Business State Machine Security 2026

业务逻辑问题往往不属于某个固定 payload，而是“应用允许了本不该出现的状态或状态迁移”。OWASP WSTG 最新业务逻辑章节明确把流程跳步、请求重排、状态参数操纵和并发依赖动作列为工作流绕过测试重点。

本专题把业务逻辑审查统一成有限状态机（FSM）/不变量（Invariant）模型。

## 1. 从页面流程升级为状态机

不要只记录 UI 的 1→2→3 页面，而要描述：

```text
State S
Actor A
Action X
Precondition P
Transition T
Side Effect E
Invariant I
```

例如：

```text
created → pending_payment → paid → fulfilled → closed
                         ↘ cancelled
paid → refunded
```

每条箭头都需要明确：谁能触发、什么条件下触发、触发几次、是否可逆。

## 2. 核心不变量

常见不变量：

- 未付款不能进入已履约；
- 已退款不能再次发放同一权益；
- 一个优惠权益只能消费一次；
- tenant A 的审批不能作用于 tenant B；
- 低权限主体不能把对象转入管理员状态；
- 终态对象不能重新进入处理中；
- 删除/撤销后旧 token/job 不得继续生效；
- 异步 worker 的结果不能覆盖更新后的新状态。

比赛中优先寻找“服务端没有真正维护这个不变量”的位置。

## 3. 状态迁移表

建议为关键对象建立：

| Current | Action | Expected Next | Actor | Preconditions | Repeatable |
|---|---|---|---|---|---|
| created | submit | pending | owner | valid fields | no |
| pending | approve | approved | reviewer | policy checks | no |
| approved | execute | completed | system/user | approved | no |
| completed | cancel | rejected/none | - | terminal | no |

然后检查代码/API 是否存在表外迁移。

## 4. OWASP Workflow Abuse 四类

### Skip

是否能绕过必要前置步骤直接进入后续状态。

### Reorder

是否能把本应 A→B→C 的动作按 A→C→B 执行仍成功。

### Replay

已成功消费的一次性动作是否能重复执行。

### Parallel

两个单独看都合法的动作在并发时是否破坏不变量。

这些模式可统一记录成状态差分，而不是为每种业务单独记忆 payload。

## 5. Client State vs Server State

重点识别：

- `status`、`step`、`phase`、`approved` 等是否由客户端提供；
- hidden field 是否被当成真实状态；
- 前端禁用按钮是否是唯一约束；
- mobile/Web 两个客户端是否使用不同流程；
- API v1/v2 是否有不同状态校验。

服务端应根据持久化状态和当前主体重新计算允许动作。

## 6. 一次性能力与计数器

OWASP WSTG 专门覆盖“一项功能可使用次数限制”。

常见对象：

- 优惠券；
- 邀请码；
- OTP/验证码；
- 下载额度；
- 免费试用；
- 积分/奖励；
- 提现/退款；
- 审批动作；
- 一次性链接。

检查计数器是否绑定正确的：用户、租户、业务对象、时间窗口和最终状态。

## 7. Async / Queue / Saga

现代系统大量使用异步队列，业务状态不再发生在一个 HTTP 请求内。

建立：

```text
request
  ↓
DB state
  ↓
event/outbox
  ↓
queue
  ↓
worker
  ↓
external service
  ↓
callback/reconciliation
```

检查：

- worker 是否验证对象当前状态；
- 旧 job 是否可能在对象已取消后继续生效；
- retry 是否重复 side effect；
- out-of-order event 是否回滚状态；
- compensation 是否完整；
- 幂等键是否跨 tenant/对象正确绑定。

## 8. TOCTOU / Concurrency

竞态专题负责具体同步方法，本专题负责业务不变量。

审查：

- 检查与写入是否在同一事务；
- quota/coupon/balance 是否采用原子更新；
- version/etag/optimistic lock 是否覆盖关键对象；
- 多 worker 是否可能同时认为自己是第一执行者。

联动 `race-condition-test.md`。

## 9. Cross-channel State Drift

特别关注同一业务的多个入口：

- Web；
- Mobile；
- Admin；
- GraphQL；
- gRPC；
- legacy API；
- webhook/async worker。

一个入口修复状态校验，不代表其他入口同步修复。联动 `shadow-api-inventory-2026.md` 和 `mobile-api-apk-discovery-2026.md`。

## 10. Capability Delta

业务逻辑 finding 必须回答：

> 攻击者原本处于状态/权限 X，通过非法迁移 Y，获得了原本不能获得的业务能力 Z。

“返回码异常”“可以重复点击”“页面顺序变化”不够。

## 11. 比赛快速流程

```text
选高价值对象
  ↓
画 5~10 个核心状态
  ↓
标终态/一次性动作/审批/金额
  ↓
Skip / Reorder / Replay / Parallel
  ↓
换角色 / 换客户端 / 换 API version
  ↓
验证 capability delta
```

优先对象：支付、订单、退款、优惠、积分、审批、邀请、会员/权限、文件处理、异步 job。

## 12. 误报控制

以下不能直接成立：

- UI 可以返回上一步；
- endpoint 可重复请求但结果幂等；
- 状态字段出现在响应；
- 不同客户端流程不同但业务约束一致；
- 请求并发但最终数据库状态正确。

必须证明非法状态、重复权益、跨权限动作或安全不变量破坏。

## 13. 防御基线

- 服务端显式状态机；
- 状态迁移白名单；
- 终态保护；
- 业务对象级授权；
- 一次性动作持久化消费；
- 幂等 key + 唯一约束；
- 原子事务/乐观锁；
- async worker 重查当前状态；
- retry 与 compensation 设计；
- 多渠道共享统一业务规则。

## References

- OWASP WSTG Business Logic Testing
- OWASP Testing for the Circumvention of Work Flows
- PortSwigger Business Logic Vulnerabilities
