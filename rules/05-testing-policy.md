# 测试策略与证据闸门

<!-- Scope: 黑盒矩阵和白盒发现验证。Priority: L3。Owns: 类型覆盖、差分证据、confidence。Does Not Own: 资产搜索节奏和报告排版。 -->

## Evidence-First

所有发现按以下链路推进：`Signal → Hypothesis → Controlled Test → Differential Evidence → Impact → Finding`。Finding 至少包含：

```yaml
type: authorization
target: https://example.invalid/api
prerequisite: session-a
request: request-or-file-reference
control_request: baseline-reference
observed_difference: concrete-field-or-status-change
security_boundary_broken: user-or-tenant-boundary
impact: verified-impact
confidence: confirmed # confirmed | high | medium | suspected | rejected
```

正式报告只允许 `confirmed`；其余进入 pending/rejected，不写成漏洞。

## 全类型矩阵

有入口就测试，无入口写 N/A 和理由：未授权、越权/IDOR、注入、SSRF、RCE/执行链、凭证/密钥、敏感路径、XSS、上传、穿越、CSRF、提权/逻辑、认证/接管、GraphQL、WebSocket、协议与配置暴露。注入按栈和差分面选探针，禁止对每个 path 机械喷单引号；上传必须追到业务越权、可执行或 SSRF 链；凭证必须过认钥闸。CORS 不测试。

基线请求与探针请求必须可对照，记录状态码、条数、主体、租户、时间差或回显差异。空列表、报错、超时不能直接等同于登录墙。
