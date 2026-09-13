# 测试策略与证据闸门

<!-- Scope: 黑盒矩阵和白盒发现验证。Priority: L3。Owns: 类型覆盖、差分证据、confidence、比赛候选优先级。Does Not Own: 资产搜索节奏和报告排版。 -->

## Evidence-First

所有发现按以下链路推进：

`Signal → Hypothesis → Candidate → Controlled Test → Differential Evidence → Capability Delta → Finding / Reject / Hold`

Finding 至少包含：

```yaml
type: authorization
target: https://example.invalid/api
prerequisite: session-a
request: request-or-file-reference
control_request: baseline-reference
observed_difference: concrete-field-or-status-change
security_boundary_broken: user-or-tenant-boundary
capability_delta: newly-gained-capability
impact: verified-impact
confidence: confirmed # confirmed | high | medium | suspected | rejected
```

正式报告只允许 `confirmed`；其余进入 pending/rejected，不写成漏洞。`200`、报错、版本旧、路径存在、反射、schema/方法可枚举都只能形成 Signal/Candidate，不能直接升级为 Finding。

## 比赛候选评分

用户明确处于网安比赛、CTF、SRC 冲榜或其它时间受限场景时，对 Candidate 使用 0–12 分内部评分；分数只用于排序，不替代证据闸门：

| 维度 | 0 | 1 | 2 |
|---|---|---|---|
| `boundary` | 未跨边界 | 边界可疑 | 已有明确边界差分 |
| `capability_delta` | 无新增能力 | 有弱增量 | 获得真实新能力 |
| `evidence` | 只有状态码/报错 | 有单点证据 | 有稳定 A/B 差分 |
| `reproducibility` | 不稳定 | 条件化复现 | 可从干净状态稳定复现 |
| `impact` | 仅信息/表面 | 有限业务影响 | 跨主体/高价值业务影响 |
| `efficiency` | 成本高/依赖多 | 中等 | 可用少量受控请求证伪/证实 |

排序优先：总分 → `boundary` → `capability_delta` → `evidence` → `efficiency`。范围不明、需要破坏性验证、真实资损或无法回滚的候选直接 `Hold/Reject`，不能靠高分越过 `01-safety-boundary.md`。

候选评分必须随证据更新；新证据可升降分。连续两次受控验证都没有增加 `boundary / capability_delta / evidence` 任一项时，停止该分支并切换下一 Candidate，避免沉没成本。

## 全类型矩阵

有入口就测试，无入口写 N/A 和理由：未授权、越权/IDOR、注入、SSRF、RCE/执行链、凭证/密钥、敏感路径、XSS、上传、穿越、CSRF、提权/逻辑、认证/接管、GraphQL、WebSocket、协议与配置暴露。注入按栈和差分面选探针，禁止对每个 path 机械喷单引号；上传必须追到业务越权、可执行或 SSRF 链；凭证必须过认钥闸。CORS 不测试。

比赛模式不是跳过矩阵，而是改变顺序：先对高分 Candidate 闭环，再回到 `pending` 类型。状态中必须区分 `tested / pending / N/A / rejected`，防止高分线索掩盖尚未覆盖的高价值类型。

基线请求与探针请求必须可对照，记录状态码、条数、主体、租户、对象、时间差、回显或状态迁移差异。空列表、报错、超时不能直接等同于登录墙，也不能单独作为漏洞证据。