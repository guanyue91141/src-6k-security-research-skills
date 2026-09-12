# Competition Auto Hunt

<!-- Scope: 已明确授权的网安比赛、CTF、SRC 固定目标。Priority: L2。Owns: 持续调度、时间预算、候选队列、专题分发与停止条件。Does Not Own: 具体漏洞验证细节、破坏性动作、报告格式。 -->

## 目标

当用户提供一个固定内网域名、URL、IP 或比赛资产并要求自动寻找漏洞时，本工作流把已有知识库串成持续执行循环：

`Bootstrap → Surface Map → Dispatch → Controlled Verify → Evidence Gate → Finding/Reject → Continue`

核心原则：

- 不因发现一个漏洞而停止；确认后继续覆盖剩余高价值面。
- 不因一个候选失败而结束目标；失败候选标记 rejected 后转下一个。
- 不因页面是登录页而认定不可测；继续分析前端构建产物、公开接口、认证边界和可观察协议面。
- 不把“200、报错、超时、版本号、反射”直接写成漏洞；必须经过差分证据与 capability delta。
- 全程继承 `rules/01-safety-boundary.md`：低频、可恢复、最小影响，不执行 DoS、批量破坏或真实资损。

## 0. 启动条件

满足以下任一描述即可进入比赛自动模式：

- 用户明确说“比赛 / CTF / 靶场 / 授权测试 / 自动找漏洞”；
- 用户给出固定内网域名、URL 或 IP，并要求连续测试；
- 用户明确要求“持续测试，不要每一步都停下来问”。

固定目标仍然是锁面模式。除非用户给出网段/资产列表，不主动把范围扩展到其他无关主机。

启动后先确认两件可机器验证的事实：

1. Agent 所在运行环境能够解析并访问目标；
2. 当前目标属于用户给定比赛范围。

无法访问时把状态记为 `blocked`，说明 DNS、路由、TLS 或端口层面的实际阻断，不把网络不可达写成“未发现漏洞”。

## 1. Campaign 状态

比赛模式在任务根 `{名}_dig/state/campaign.yaml` 维护以下状态。字段可扩展，但语义保持稳定：

```yaml
mode: competition_auto
phase: bootstrap # bootstrap | surface | dispatch | verify | report | complete | blocked
scope:
  roots: []
  locked: true
budget:
  total_minutes: null      # 用户没给时间时可为空
  started_at: null
  remaining_minutes: null
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
next_actions: []
```

状态更新规则：

- 每完成一个动作，必须改变 coverage、candidate 或 next_actions 至少一项；否则视为空转。
- 每个候选都有唯一 ID，例如 `C-001`。
- 一个候选结束后立即从 `active` 清空，再从队列选择下一项。
- 已确认 finding 不自动终止 campaign。

## 2. 快速 Surface Map

第一轮目标不是“马上喷 payload”，而是在较短时间内建立可搜索攻击面。

至少记录：

- 页面/登录形态、前端框架、SSR/SPA 特征；
- 主 JS chunk、lazy route、source map 是否存在；
- REST/OpenAPI、GraphQL、gRPC/gRPC-Web、WebSocket/SSE；
- 公开与登录后接口、对象 ID、tenant/org/user 等主体字段；
- 上传、下载、导出、搜索、回调、审批、支付/订单/积分等业务流程；
- mobile-only/legacy/shadow API 信号；
- Next.js、Kubernetes、CI/CD、云存储等专项技术信号。

优先调用已有专题：

- SPA/构建产物：`spa-source-map-api-recovery-2026.md`
- 旧版/隐藏 API：`shadow-api-inventory-2026.md`
- API 总体：`api-security-review.md`
- GraphQL：`graphql-modern-2026.md`
- gRPC：`grpc-security-2026.md`
- Next.js：`nextjs-ssr-security-2026.md`
- 业务流程：`business-state-machine-security-2026.md`

Surface Map 结束的判据不是“全部测完”，而是已经有足够信息构建首批候选队列。

## 3. Candidate Queue

每个有价值的信号转换成候选对象，而不是立刻叫“漏洞”：

```yaml
id: C-001
class: authorization
surface: /api/orders/{id}
signal: other-object-id-observed
hypothesis: object ownership may not be enforced
expected_capability_delta: low-privileged user may read another owned object
control: own-object request
test: alternate-object request
confidence: suspected
priority: 82
status: queued # queued | active | confirmed | rejected | blocked | deferred
notes: []
```

### 优先级评分

优先级用于决定“先测哪个”，不代表漏洞严重性。建议 0–100：

- 预期 capability delta：0–30
- 当前证据信号强度：0–25
- 入口可达性与复现成本：0–15
- 与比赛常见得分面的匹配度：0–15
- 验证所需时间：0–10（越短分越高）
- 误报风险：0–5（越低分越高）

同分优先：授权/业务逻辑 → API/隐藏接口 → 客户端泄露形成的服务端边界 → 协议差异 → 单纯配置暴露。

## 4. 自动专题分发

根据候选特征加载最少必要专题，不通读全部知识库：

| Signal | 优先专题 |
|---|---|
| object/user/tenant/order ID | `idor-test.md` + `api-security-review.md` |
| version/legacy/mobile endpoint | `shadow-api-inventory-2026.md` |
| workflow/order/payment/approval | `business-state-machine-security-2026.md` |
| JS chunk/source map/client schema | `spa-source-map-api-recovery-2026.md` |
| APK/IPA | `mobile-api-apk-discovery-2026.md` |
| GraphQL | `graphql-modern-2026.md` |
| gRPC/protobuf | `grpc-security-2026.md` |
| Next.js/RSC/Server Actions | `nextjs-ssr-security-2026.md` |
| OAuth/JWT/session/passkey | `oauth-jwt-test.md` / `passkey-webauthn-security-2026.md` |
| webhook/event delivery | `webhook-integrity-2026.md` |
| upload/object storage | `file-upload-test.md` |
| cache/CDN/SSR cache | `cache-modern-2026.md` |
| HTTP/2/3 proxy differential | `http2-attacks-test.md` + `http-desync-modern-2026.md` |
| CI/CD / K8s | `cicd-security-review-2026.md` / `k8s-security-review-2026.md` |

没有匹配专题时回到 `打穿短表.md` 与 `05-testing-policy.md`，而不是凭空发明结论。

## 5. Controlled Verify Loop

每次只激活一个候选，减少上下文和证据混淆：

1. 固定基线：保存正常请求/响应或正常状态变化；
2. 明确变量：一次只改变一个与假设相关的主体、对象、状态或输入；
3. 获取差分：比较状态码、主体、对象字段、条数、状态迁移或业务结果；
4. Capability Delta：回答“攻击者新增了什么原本没有的能力”；
5. 反证：至少检查一个合理的正常解释，例如缓存、前置解析、公开数据、客户端展示差异；
6. 裁决：confirmed / rejected / deferred；
7. 更新 candidate queue，自动转下一个。

正式 finding 仍必须满足 `rules/05-testing-policy.md` 和 `competition-triage-evidence-2026.md`。

## 6. 连续执行策略

### 发现漏洞后

- 立即保存最小充分证据；
- 不继续扩大影响，不批量读取/修改；
- 将相关同根因候选合并，避免重复消耗时间；
- 回到队列，继续下一个不同根因候选。

### 候选失败后

- 写入 rejected 原因；
- 若反证暴露了新攻击面，则生成新的候选；
- 否则直接继续，不在已证伪路径上反复换 payload。

### 低价值信号

版本号、banner、单独 source map、单独 introspection、登录页、公开 swagger 本身只作为 Surface Signal；除非能产生新的 capability delta，否则不占用长时间验证。

## 7. 时间预算

用户没有给时间时，不虚构总时长；只按优先级持续推进。

用户给出明确比赛剩余时间时，可采用动态预算：

- 前 15%：快速 Surface Map；
- 中间 55%：高优先候选验证；
- 后 20%：业务逻辑、Shadow API、客户端恢复等深挖；
- 最后 10%：复测 confirmed、整理证据和输出。

若早期已经拿到 confirmed finding，后续预算仍优先寻找**不同根因**的第二、第三个漏洞，而不是重复扩大第一个漏洞的影响。

## 8. Coverage Gate

结束前检查：

```text
[ ] frontend / JS / route surface 已建立
[ ] API inventory 已建立或明确 N/A
[ ] auth 与 authorization 已形成判定
[ ] 业务状态机有入口则已检查
[ ] source-map/mobile/shadow-api 信号有则已跟进
[ ] GraphQL/gRPC/WebSocket/Next.js 等协议/框架信号有则已分发专题
[ ] exposure/config 只保留能形成实际边界影响的候选
[ ] candidate queue 无高优先级未处理项，或剩余项已标 deferred 原因
```

Coverage Gate 不表示“目标绝对无漏洞”，只表示本次比赛时间/范围内已完成可解释覆盖。

## 9. 停止条件

只有以下情况允许结束自动循环：

1. 用户明确要求停止；
2. 目标持续不可达，且已记录 DNS/网络/服务层证据；
3. 继续测试会越过 `01-safety-boundary.md`；
4. 用户给定时间预算耗尽；
5. Coverage Gate 已满足，且候选队列没有未处理的高优先项。

禁止以下“伪停止”：

- “发现一个漏洞，所以完成”；
- “首页需要登录，所以无法测试”；
- “nuclei 没扫到，所以无漏洞”；
- “一个候选失败，所以目标安全”；
- “页面没有明显输入框，所以无攻击面”。

## 10. 对用户的阶段输出

自动模式中减少无意义打断。只在以下节点主动汇报：

- Surface Map 完成并形成首批高优先候选；
- confirmed finding 出现；
- 目标被网络或安全边界阻塞；
- Coverage Gate 完成。

普通 rejected 候选只记录到状态文件，不逐条打断用户。
