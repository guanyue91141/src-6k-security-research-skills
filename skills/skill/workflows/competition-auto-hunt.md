# Competition Auto Hunt

<!-- Scope: 已明确授权的网安比赛、CTF、SRC 固定目标。Priority: L2。Owns: 持续调度、时间预算、候选队列、专题分发与停止条件。Does Not Own: 具体测试细节、破坏性动作、报告格式。 -->

## 目标

比赛模式把已有知识库串成一个连续控制器：

`Bootstrap → Surface Map → Candidate Queue → Dispatch → Controlled Verify → Evidence Gate → Finding/Reject/Hold → Continue`

核心原则：

- 不因确认一个 Finding 而停止；继续覆盖不同根因的高价值候选。
- 不因一个 Candidate 失败而结束目标；Reject 后立即转下一条。
- 不把登录页、状态码、报错、版本、schema、banner 或单次异常直接写成 Finding。
- 全程继承 `rules/01-safety-boundary.md` 的范围、可恢复和最小影响要求。
- 评分只用于排序；最终结论只认差分证据与 Capability Delta。

## 0. 启动条件

满足以下任一情况进入本工作流：

- 用户明确说比赛、CTF、靶场、SRC 冲榜或授权固定目标；
- 用户要求持续寻找有效问题，而不是逐步确认；
- 用户给出明确固定范围并要求在有限时间内提高产出。

固定目标仍是锁面模式。除非用户给出网段或资产列表，不主动扩展到无关资产。

## 1. Campaign 状态

任务根维护 `{名}_dig/state/campaign.yaml` 与 `candidate-board.md`：

```yaml
mode: competition_auto
phase: bootstrap # bootstrap | surface | dispatch | verify | report | complete | blocked
scope:
  roots: []
  locked: true
budget:
  total_minutes: null
coverage:
  frontend: pending
  api: pending
  auth: pending
  authorization: pending
  business_logic: pending
  client_artifacts: pending
  protocol: pending
  exposure: pending
candidates:
  queued: []
  active: null
  confirmed: []
  rejected: []
  hold: []
next_actions: []
```

每个动作至少改变 coverage、candidate 或 next_actions 一项；否则视为空转。

## 2. Surface Map

第一轮只建立足够的“可验证面”，不追求一次测完：

- 页面/登录形态、前端框架、SSR/SPA 特征；
- 主 JS chunk、lazy route、source map 与客户端 schema；
- REST/OpenAPI、GraphQL、gRPC、WebSocket/SSE 等接口形态；
- 对象 ID、user/tenant/org 等主体字段与权限关系；
- 上传、下载、导出、回调、审批、订单、积分等业务状态；
- mobile-only、legacy、shadow API 信号；
- Next.js、CI/CD、Kubernetes、云存储等专项技术信号。

Surface Map 的结束条件：已经能形成首批 Candidate，而不是“所有专题都读完”。

## 3. Candidate Queue

所有线索先变成 Candidate：

```yaml
id: C-001
surface: api/object
hypothesis: object-boundary-may-be-missing
attacker: normal-user
boundary: user-object
baseline: own-object
variant: alternate-object
score: 8
queue: B
status: queued
next_action: build-minimal-differential-control
```

### 唯一评分基准：0–12

统一使用 `rules/05-testing-policy.md` 的六维评分：

- Boundary：0–2
- Capability Delta：0–2
- Evidence：0–2
- Reproducibility：0–2
- Impact：0–2
- Efficiency：0–2

队列解释：

- `9–12` → A：优先闭环；
- `6–8` → B：补关键证据；
- `0–5` → C：最小证伪，不投入长链。

若旧状态里存在 0–100 priority，只用于兼容展示；重新排序时必须转换回上述六维评分，不再维护第二套权重模型。

## 4. Dispatch

根据目标信号只加载最少必要专题：

| Signal | 优先专题 |
|---|---|
| object/user/tenant/order | `api-security-review.md` + `idor-test.md` |
| version/legacy/mobile endpoint | `shadow-api-inventory-2026.md` |
| workflow/order/approval/积分 | `business-state-machine-security-2026.md` |
| JS chunk/source map/client schema | `spa-source-map-api-recovery-2026.md` |
| APK/IPA | `mobile-api-apk-discovery-2026.md` |
| GraphQL | `graphql-modern-2026.md` |
| gRPC/protobuf | `grpc-security-2026.md` |
| Next.js/RSC/Server Actions | `nextjs-ssr-security-2026.md` |
| OAuth/session/passkey | `oauth-jwt-test.md` / `passkey-webauthn-security-2026.md` |
| webhook/event delivery | `webhook-integrity-2026.md` |
| upload/object storage | `file-upload-test.md` |
| cache/CDN/SSR cache | `cache-modern-2026.md` |
| HTTP protocol differential | `http2-attacks-test.md` + `http-desync-modern-2026.md` |
| CI/CD / K8s | `cicd-security-review-2026.md` / `k8s-security-review-2026.md` |
| AI/Agent | `llm-security-test.md` |

没有匹配专题时回到 `打穿短表.md` 与 `rules/05-testing-policy.md`，不凭空扩展结论。

## 5. Controlled Verify Loop

每次只激活一个 Candidate：

1. 固定基线；
2. 一次只改变一个与假设相关的主体、对象、状态或输入；
3. 比较主体、对象字段、条数、状态迁移或业务结果；
4. 回答 Capability Delta：新增了什么原本没有的能力；
5. 检查一个合理反证，例如缓存、公开数据、解析层或展示层差异；
6. 裁决 `confirmed / rejected / hold`；
7. 更新评分并自动选择下一 Candidate。

### 两次无增量止损

连续两次受控验证都没有增加以下任一项时，停止当前 Candidate：

- Boundary
- Capability Delta
- Evidence

只有新信息改变 Hypothesis 时才允许重新激活，避免沉没成本。

## 6. 连续执行策略

### confirmed

- 保存最小充分证据；
- 合并同根因重复候选；
- 不扩大影响；
- 返回队列寻找不同根因 Candidate。

### rejected

记录统一原因，例如：

- `no_boundary_crossed`
- `no_capability_delta`
- `false_positive_layering`
- `expected_behavior`
- `not_reproducible`
- `insufficient_evidence`
- `duplicate_surface`

然后立即继续。

### hold

用于缺少账号、测试对象、环境条件或需要用户补充授权范围的候选，不与 rejected 混淆。

## 7. 时间预算

用户未给时间时，不虚构总时长，只持续按评分推进。

用户给出明确剩余时间时，建议动态分配：

- 前 15%：Surface Map；
- 中间 55%：A/B 队列验证；
- 后 20%：状态机、Shadow API、客户端恢复等深挖；
- 最后 10%：复测 confirmed、整理证据与 Coverage Gate。

若早期已有 confirmed，后续仍优先寻找不同根因的第二、第三个高分 Candidate。

## 8. Coverage Gate

结束前至少确认：

```text
[ ] frontend / JS / route surface 已建立
[ ] API inventory 已建立或明确 N/A
[ ] auth 与 authorization 已形成判定
[ ] 业务状态机有入口则已检查
[ ] source-map/mobile/shadow-api 信号有则已跟进
[ ] 协议/框架专项信号有则已分发专题
[ ] 低价值 surface signal 未被误写成 Finding
[ ] Candidate Queue 无高分未处理项，或剩余项已有 hold/deferred 原因
```

Coverage Gate 只表示本次比赛范围与预算内完成了可解释覆盖，不表示“目标绝对无问题”。

## 9. 停止条件

只允许在以下情况结束自动循环：

1. 用户明确停止；
2. 目标持续不可达且已有实际阻断证据；
3. 继续会越过 `rules/01-safety-boundary.md`；
4. 用户给定预算耗尽；
5. Coverage Gate 完成且没有未处理的 A 队列 Candidate。

以下都不是停止理由：一个 Finding 已确认、一个 Candidate 失败、首页需要登录、自动扫描没有命中、页面缺少明显输入框。

## 10. 阶段输出

自动模式只在这些节点主动汇报：

- Surface Map 完成并形成首批 A/B 队列；
- confirmed Finding 出现；
- 目标被网络或安全边界阻塞；
- Coverage Gate 完成。

普通 rejected Candidate 只进入状态板，不逐条打断用户。

## 11. 赛后复盘

统计：

- confirmed Candidate 的初始得分与最早高价值 Signal；
- 最耗时的 rejected Candidate 及缺失的判定条件；
- hold Candidate 的缺口；
- 每个 confirmed 从 Signal 到 Evidence Gate 的动作数。

下一场优先调整评分、路由和假阳性规则，而不是只增加更多知识文件。