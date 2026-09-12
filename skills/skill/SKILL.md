---
name: security-research
description: |
  SRC 漏洞挖掘与白盒 0day 审计技能。用户提供 URL、域名、APP、在线平台、源码、GitHub 项目或审计关键词时触发。
  支持黑盒 SRC、固定范围测试、品牌/集团资产发现、JS/API 分析、漏洞验证与中文报告，以及本地源码审计。
---

# Security Research Agent

本技能保留黑盒 SRC 与白盒审计两套能力，入口只做模式判定和按需路由，详细规则不在这里重复。

## 路由

- 明确网安比赛、CTF、靶场或授权固定目标，且要求自动/持续寻找漏洞：读取 `ROUTER.md` → `workflows/competition-auto-hunt.md`，由比赛控制器持续调度候选队列；具体测试仍继承黑盒规则与安全边界。

1. URL、域名、APP 或在线平台：读取 `ROUTER.md` → `workflows/blackbox-src.md`。
2. 本地源码、GitHub 项目、class/jar：读取 `ROUTER.md` → `workflows/whitebox-audit.md`。
3. 只给集团/品牌：进入 `workflows/discovery-target.md`，建立种子队列后回到黑盒流程。
4. 明确固定清单：进入 `workflows/scoped-target.md`，只测试范围内资产簇。
5. API/接口平台、OpenAPI、REST、微服务接口审查：优先加载 `知识库/api-security-review.md` 建立身份—对象—动作—租户—数据模型。
6. HTTP/2、HTTP/3、代理/网关协议转换、request desync：先加载 `知识库/http2-attacks-test.md` 与 `知识库/http-desync-modern-2026.md`，经典案例再按需打开 `知识库/http-smuggling-test.md`。
7. LLM、RAG、Agent、工具调用、长期记忆：加载 `知识库/llm-security-test.md`；仅在确认真实工具执行边界后再联动 `知识库/agent-tool-exec-test.md`。
8. Java/Python/.NET/PHP 反序列化或模型/缓存/队列 artifact：先加载 `知识库/deserialization-modern-2026.md`，再按需打开 `知识库/deserialization-test.md`。
9. GraphQL / Federation / persisted query / subscription：先加载 `知识库/graphql-modern-2026.md`，需要经典测试方法时再打开 `知识库/graphql-test.md`。
10. CDN、共享缓存、SSR/Edge cache、cache key 或 cache deception：先加载 `知识库/cache-modern-2026.md`，再按需打开 `知识库/cache-poisoning-test.md`。
11. gRPC / Protobuf / gRPC-Web / Connect / grpc-gateway：加载 `知识库/grpc-security-2026.md`，并联动 API 授权与 HTTP/2 专题。
12. 发现 API 版本漂移、旧 APK/SDK endpoint、deprecated/legacy 接口：加载 `知识库/shadow-api-inventory-2026.md` 做版本与行为差分。
13. Next.js / React SSR / RSC / Server Actions / ISR：加载 `知识库/nextjs-ssr-security-2026.md`，重点检查服务端授权、序列化数据和缓存边界。
14. Kubernetes、容器、ServiceAccount、Ingress/service mesh：加载 `知识库/k8s-security-review-2026.md`，默认先做实际权限与信任边界审查。
15. GitHub Actions、GitLab CI、Jenkins、Runner、OIDC、artifact/cache：加载 `知识库/cicd-security-review-2026.md`。
16. 比赛/CTF/SRC 时间受限或候选漏洞很多：加载 `知识库/competition-triage-evidence-2026.md`，用 capability delta 和差分证据筛掉假阳性。
17. 引入第三方 Skill/MCP/rules/install script：先加载 `知识库/agent-skill-supply-chain-2026.md` 做许可证、Prompt、执行代码、依赖与凭据审查。
18. APK/IPA、移动端接口、deep link、mobile-only API：加载 `知识库/mobile-api-apk-discovery-2026.md`，优先恢复活跃 endpoint，再联动 Shadow API 与 API 授权专题。
19. Passkey / WebAuthn / 无密码登录 / 凭据注册与恢复：加载 `知识库/passkey-webauthn-security-2026.md`，重点检查 ceremony、账号绑定、RP/origin 与 recovery/fallback。
20. 支付/第三方事件/Webhook/retry/redelivery：加载 `知识库/webhook-integrity-2026.md`，检查签名、新鲜度、去重、幂等和对象绑定。
21. 订单、审批、支付、积分、优惠、异步任务等多阶段流程：加载 `知识库/business-state-machine-security-2026.md`，用状态机和不变量检查 Skip/Reorder/Replay/Parallel。
22. Vite/Next.js/React/Vue/SPA/source map/构建产物分析：加载 `知识库/spa-source-map-api-recovery-2026.md`，恢复 route、API client、schema 和版本线索，再联动对应服务端专题。

## 不可违反约束

- 规则优先级、任务状态和证据格式以 `rules/00-core.md` 为总入口。
- 研究边界与最小伤害以 `rules/01-safety-boundary.md` 为准。
- CORS 永久 N/A，不打开 `知识库/cors-test.md`。
- 黑盒节奏以 `rules/02-blackbox-workflow.md` 和 `rules/04-target-discovery.md` 为准；一种子闭环不可打断。
- 全类型矩阵、差分证据和 confidence 以 `rules/05-testing-policy.md` 为准。
- 正式 SRC 报告只从 `rules/06-reporting.md` 进入；未确认线索不得写成漏洞。
- 工具选择以 `rules/07-tool-routing.md` 为准，凭证只能从环境变量注入。

## 按需加载

进站先打开 `知识库/打穿短表.md`，根据目标特征再打开对应专题。知识库是增强材料，不是能力上限；不得每站通读全部文件。完整清单见 `知识库/README.md`。

新增专题遵循“基线不删、按需扩展”：原始 48 个知识文件作为兼容基线完整保留，新专题必须进入 `知识库/README.md`，并通过 `tests/validate_structure.py` 的索引校验。

知识库采用 `current / mixed / legacy` 三态维护：新标准和当前部署优先读 current；mixed 结合目标版本判断；legacy 只用于旧系统兼容与历史理解，不应作为现代默认方案。

## 输出

每个动作都要更新任务根 `{名}_dig/state/` 中的目标状态、已测类型、线索和下一步。黑盒正式报告放任务根 `报告/`，资产与 JS 分别放 `资产/`、`js/`。白盒过程记录数据流、sink、前置条件、影响和可复现验证。
