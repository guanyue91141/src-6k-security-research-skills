---
status: current
last_reviewed: 2026-09
sources:
  - murrtada/bug-bounty-agent-skills:hunt-cicd
  - GitHub Actions security hardening guidance
---

# CI/CD / GitHub Actions / Build Pipeline 安全审查 2026

> 面向授权比赛、SRC、开源项目和白盒审计。重点是识别“低信任输入 → 高权限流水线”的边界错误，不主动触发真实组织的高权限流水线做破坏性验证。

## 1. 核心模型

CI/CD 风险统一建模成：

`untrusted source → workflow trigger → checkout/build step → token/secrets/cloud identity → artifact/deploy target`

高价值问题通常不是“工作流存在”，而是低信任数据进入了高权限执行上下文。

## 2. GitHub Actions

重点审查：

- `pull_request` 与 `pull_request_target` 的权限差异；
- `workflow_run` 是否消费不可信上游产物；
- workflow 是否 checkout fork/PR 代码后在高权限上下文执行；
- `${{ github.event.* }}` 是否直接进入 shell/script；
- `permissions:` 是否最小化；
- `GITHUB_TOKEN` 是否拥有不必要写权限；
- environment / required reviewers 是否真正隔离生产部署；
- reusable workflow 与 composite action 是否固定到可信 commit；
- third-party action 是否仅用 mutable tag。

## 3. OIDC / Cloud Federation

现代流水线更常用 OIDC，而不是长期云密钥。审查：

- trust policy 是否约束 repo、ref、environment、workflow；
- `sub` / `aud` 条件是否过宽；
- 是否允许整个 org 或任意 branch 假定生产角色；
- PR/fork 场景是否能进入同一 OIDC 信任路径；
- cloud role 是否最小权限；
- role chaining 是否绕开初始限制。

## 4. Self-hosted Runner

重点看：

- 公共/低信任 PR 是否会落到 self-hosted；
- runner 是否一次性/ephemeral；
- job 间 workspace、credential、Docker layer 是否残留；
- runner 是否同时可访问内网、云 metadata、部署凭据；
- runner group / label 是否真正限制 repository；
- 宿主机是否使用长期静态凭据。

“用了 self-hosted”不是漏洞；必须形成跨任务或跨信任域能力差分。

## 5. Artifact / Cache

特别关注 2025–2026 常见供应链问题：

- 低权限 workflow 是否能写入高权限 workflow 后续读取的 cache；
- artifact 下载是否验证来源 run/repo/ref；
- 同名 artifact 是否可能被错误 run 覆盖/选中；
- build output 是否携带 `.env`、kubeconfig、debug dump；
- cache key 是否遗漏 commit/ref/trust level；
- release/deploy job 是否消费未经签名/校验的构建产物。

## 6. Jenkins / GitLab / 其他 CI

统一审查模型：

- 匿名与低权限用户能否配置/触发高权限 job；
- script/console 类管理功能是否有强认证；
- runner/agent registration 是否有生命周期与项目绑定；
- secret masking 是否只保护日志，而 artifact 仍含明文；
- pipeline-as-code 是否允许低信任分支修改部署逻辑；
- job token 是否能跨项目/跨 namespace。

针对具体 CVE 必须按产品版本验证，不把“看起来像 Jenkins”直接映射历史漏洞。

## 7. Terraform / IaC / State

检查：

- state 是否进入 public artifact/bucket/repo；
- remote backend 是否强认证、加密、版本化；
- state 中是否含敏感 output/provider credential；
- plan artifact 是否暴露 secret；
- IaC PR 是否能修改 trust policy、runner、OIDC、network boundary；
- deploy job 是否对 plan/apply 做职责分离。

## 8. Secrets 与日志

重点看**秘密的生命周期**：

- 长期 credential 是否可换成 OIDC；
- mask 之前是否被打印；
- base64/派生格式是否绕过日志脱敏；
- artifact / test report / crash dump 是否含 secret；
- fork/PR 是否有读取 org/repo secret 的路径；
- secret 是否绑定 environment 和最小 scope。

## 9. 静态工具路由

适合 Agent 优先调用/建议的低风险检查：

- `actionlint`：workflow 语法/表达式；
- `zizmor`：GitHub Actions 安全模式；
- secret scanner：只在授权代码/产物中使用；
- dependency/SBOM/provenance 检查；
- IaC policy scanner。

静态发现先形成 hypothesis，再决定是否需要运行时验证。

## 10. Evidence Gate

以下只是 Signal：

- 发现 `pull_request_target`；
- 使用 self-hosted runner；
- workflow 有 secrets；
- 找到 Terraform state；
- Jenkins 暴露登录页。

升级 Finding 必须明确：

`攻击者控制什么输入 → 哪个高权限 job 消费 → 获得了什么原本没有的能力`

比赛环境可按题目授权做完整验证；真实 SRC 默认使用最小影响证明。

## 11. 联动

- 供应链/依赖 → `insecure-scm-test.md`
- K8s / deploy identity → `k8s-security-review-2026.md`
- Secret 泄露 → `info-leak-test.md`
- API token / OAuth → `oauth-jwt-test.md`
- 候选漏洞判定 → `competition-triage-evidence-2026.md`
