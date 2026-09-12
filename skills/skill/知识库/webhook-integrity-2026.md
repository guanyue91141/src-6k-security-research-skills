---
status: current
last_reviewed: 2026-09
sources:
  - https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
  - https://docs.stripe.com/webhooks
---

# Webhook Integrity 2026

用于授权安全审查中的 Webhook/事件接收端完整性检查。重点放在来源真实性、原始载荷、时效性、去重、幂等和业务对象绑定。

## 1. 来源与完整性

GitHub 官方建议使用高熵 webhook secret，并基于原始 payload 验证 `X-Hub-Signature-256`。检查：

- secret 是否独立且安全存储；
- 是否基于原始 body 计算；
- 是否使用推荐算法；
- 比较是否采用 constant-time 方法；
- test/live/legacy endpoint 是否保持一致策略。

## 2. Freshness

Stripe 官方签名包含时间戳，并建议对签名时间进行容忍窗口检查以降低重放风险。

检查：

- 是否验证事件时间；
- 时钟是否同步；
- 窗口是否合理；
- 已过期事件是否拒绝进入业务逻辑。

## 3. Delivery ID / Event ID

Webhook 天然可能重试，因此需要持久去重。

模型：

```text
event_id → processing_state → business_object → side_effect
```

检查同一事件再次出现时是否安全，以及并发重复投递是否仍保持一次性业务结果。

## 4. 幂等性

高价值业务包括支付、退款、发货、权益、积分、订阅和审批。

服务端应保证：

- 去重记录可持久化；
- side effect 与去重状态保持一致；
- worker 超时/重启不会重复执行；
- redelivery 使用同一幂等逻辑。

## 5. Event Ordering

不要依赖到达顺序表示业务顺序。对多阶段事件建立允许的状态迁移，例如：

```text
created → authorized → paid → refunded
```

服务端应根据当前状态判断事件是否仍有效，避免旧事件覆盖新状态。

## 6. Business Object Binding

即使签名正确，也要确认：

- external ID 唯一；
- transaction/order/customer 与本地对象一致；
- tenant/account 映射正确；
- 金额、币种、套餐等关键字段由可信事件驱动；
- 客户端字段不能覆盖可信 provider 结果。

## 7. Retry / Redelivery

retry、redelivery、dead-letter 与后台重放入口必须继续经过：

- 来源/权限检查；
- event 去重；
- tenant scope；
- 状态机；
- 审计。

## 8. 误报控制

以下不能单独成立：

- webhook endpoint 可公网访问；
- provider 会自动 retry；
- header 中有 event ID；
- 请求返回不同 HTTP 状态。

必须证明来源、时效、幂等、对象绑定或状态机中的至少一个边界真实失效。

## 9. 防御基线

- HTTPS；
- 高熵 secret；
- raw-body signature verification；
- constant-time compare；
- freshness/timestamp；
- durable event-id dedupe；
- idempotent side effects；
- explicit state machine；
- object/tenant binding；
- retry/redelivery 复用同一安全链路；
- 审计与 secret rotation。

## References

- GitHub Docs: Validating webhook deliveries
- Stripe Docs: Webhooks / replay protection
