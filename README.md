# SRC-6K Security Research Skills

一套面向授权安全研究、网安比赛、CTF、SRC 与白盒审计的 Grok/Codex 安全研究能力包，覆盖黑盒测试、固定范围测试、资产发现、JS/API 分析、漏洞验证、中文报告和源码审计。

## 目录

```text
rules/                    # 00-07 分层运行时规则
skills/skill/             # 兼容现有安装路径的安全研究技能入口
skills/skill/知识库/       # 原始 48 个兼容基线 + 持续扩展专题（当前 65 个）
docs/legacy-rules/        # 重构前规则归档，不参与运行时加载
tests/                    # 结构与回归检查
mcp-servers/fofa_MCP/     # FOFA MCP 服务（凭证仅从环境变量读取）
```

## 设计要点

- `rules/00-core.md` 定义 L0-L4 单向优先级和统一目标状态模型。
- 黑盒、白盒、资产发现和测试策略分离，入口技能仅负责路由和按需加载。
- 所有发现遵循 Evidence-First：`Signal → Hypothesis → Controlled Test → Differential Evidence → Capability Delta → Finding`。
- 原始 48 个知识专题作为兼容基线完整保留；扩展专题采用“只增不误删”的验证策略，不再被固定数量限制。
- 第一轮现代化增加 API、HTTP Desync、GraphQL、Cache、反序列化、LLM/Agent 等专题。
- 比赛向第二轮新增 gRPC、Shadow API、Next.js/SSR、Kubernetes、CI/CD、候选漏洞证据闸门和 Agent Skill 供应链审查。
- 第三轮补齐 Mobile API/APK、Passkey/WebAuthn、Webhook 完整性、业务状态机、SPA/source map/API 恢复。
- 第三方 Skill 不整包复制；优先检查许可证、抽取增量能力、按本项目架构重写并保留来源元数据。
- `.env`、私钥和密钥类文件默认被 Git 忽略，FOFA 脚本不包含硬编码凭证。

## 比赛优先专题

时间受限时优先从这些 current 专题进入：

- `competition-triage-evidence-2026.md`：候选漏洞筛选、差分证据与 capability delta；
- `api-security-review.md` + `shadow-api-inventory-2026.md`：BOLA/BFLA、旧版本/隐藏 API；
- `mobile-api-apk-discovery-2026.md`：APK/IPA 中恢复 mobile-only/legacy API；
- `spa-source-map-api-recovery-2026.md`：从 Vite/Next.js/SPA 构建产物恢复 route、schema 与 API client；
- `business-state-machine-security-2026.md`：订单/审批/支付/积分等流程的不变量与状态迁移；
- `grpc-security-2026.md`：gRPC、Protobuf、transcoding 与方法级授权；
- `nextjs-ssr-security-2026.md`：RSC、Server Actions、SSR/ISR/cache；
- `passkey-webauthn-security-2026.md`：WebAuthn ceremony、账号绑定、RP/origin 和恢复；
- `webhook-integrity-2026.md`：Webhook 签名、重放、幂等和业务对象绑定；
- `cicd-security-review-2026.md`：GitHub Actions、OIDC、Runner、artifact/cache；
- `k8s-security-review-2026.md`：RBAC、ServiceAccount、workload identity、容器边界。

## 验证

```bash
python3 tests/validate_structure.py
```

结构检查会验证：

1. `rules/00-07` 是否完整；
2. 工作流入口与 Markdown 引用是否有效；
3. 原始 48 个知识专题是否全部保留；
4. 新增专题是否已经登记进知识库索引；
5. 现代 overlay 是否包含维护元数据；
6. README 声明数量是否与知识库目录一致；
7. 是否存在重复文件或入口文件异常膨胀。

## 本地配置

复制 `mcp-servers/fofa_MCP/.env.example` 为 `.env`，按需填写 FOFA 环境变量。不要把凭证写入规则、知识库、配置模板或 Git 提交。

详细重构记录见 [REFACTOR_AUDIT.md](REFACTOR_AUDIT.md)。
