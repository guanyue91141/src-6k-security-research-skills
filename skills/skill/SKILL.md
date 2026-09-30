---
name: security-research
description: |
  授权安全研究与 SRC 漏洞挖掘技能。当用户提供 URL、域名、IP、APP、在线平台、源码、
  GitHub 项目、class/jar、APK/IPA，或要求做 SRC 挖洞、CTF/靶场/网安比赛、白盒代码审计、
  API/GraphQL/gRPC/LLM/K8s/CI-CD 专项审查时触发。覆盖资产发现、JS/API 分析、访问控制、
  注入、SSRF、XSS、RCE 链、业务逻辑与白盒 Phase 0-6 审计，产出可复核证据与中文报告。
---

# Security Research Agent

## 用途

在用户授权的 SRC / 白盒研究语境下，把分散的安全专题组织成可执行的挖洞与审计流程：先判定入口，再按目标信号加载最少必要知识，最后用差分证据决定是否成文。

本文件只负责**入口判定、输入输出契约与不可违反约束**；分层方法论在 `rules/00-07`，专题细节在 `知识库/`，两者都不在此复述。

## 触发场景

满足任一即进入本技能：

- 给出 URL、域名、IP、APP 或在线平台，要求找漏洞或做安全测试；
- 只给集团或品牌，要求发现资产；
- 给出本地源码、GitHub 项目、class/jar，要求代码审计；
- 明确说明网安比赛、CTF、靶场、SRC 冲榜或时间受限；
- 要求针对 API、GraphQL、gRPC、WebSocket、LLM/Agent、K8s、CI/CD 等特定技术面审查；
- 要求把已确认且达到门槛的问题写成中文报告。

只有品牌或范围模糊时**不要**先追问，按入口判定先建立资产面。

## 路由

### 第一步：判定入口

| 用户输入 | 入口 |
| --- | --- |
| 比赛 / CTF / 靶场 / 授权固定目标，且要求自动持续找漏洞 | `ROUTER.md` → `workflows/competition-auto-hunt.md` |
| URL / 域名 / APP / 在线平台 | `ROUTER.md` → `workflows/blackbox-src.md` |
| 本地源码 / GitHub 项目 / class/jar | `ROUTER.md` → `workflows/whitebox-audit.md` |
| 只给集团或品牌 | `workflows/discovery-target.md`，建种子队列后回到黑盒 |
| 明确给出固定资产清单 | `workflows/scoped-target.md` |

入口只决定加载顺序，不改变规则优先级与安全边界。判定细则见 `ROUTER.md`。

### 第二步：按信号加载专题

入口**不罗列全部专题**，检索走索引层：

```text
知识库/打穿短表.md       # 进站首选，按目标特征定位专题
知识库/README.md         # 分类路由表 + companion 主从关系与冲突消解
知识库/registry.yaml     # 机器可读元数据：用途 / 触发信号 / 输入输出 / 关联
```

加载纪律：只打开命中专题，禁止每站通读全库；`current` 优先，`mixed` 结合目标版本判断，`legacy` 仅在命中具体信号时使用，`disabled` 不加载。

## 输入输出契约

| 环节 | 约定 |
| --- | --- |
| 输入 | 授权范围（目标或清单）、可用会话/账号、可选的源码或客户端产物 |
| 过程状态 | 每个动作更新任务根 `{名}_dig/state/` 的目标状态、已测类型、线索与下一步 |
| 落盘 | 资产 `资产/`、JS `js/`、脚本与状态 `{名}_dig/`、黑盒报告 `报告/` |
| 证据链路 | Signal → Hypothesis → Controlled Test → Differential Evidence → Capability Delta → Finding |
| 结论门槛 | 只有 `confirmed` 进入正式报告；未确认线索进 `findings`，不得写成漏洞 |

白盒审计额外记录输入可控性、sink、前置条件、绕过、影响与可复现验证。

## 不可违反约束

- 规则优先级、任务状态与证据格式以 `rules/00-core.md` 为总入口。
- 研究边界与最小伤害以 `rules/01-safety-boundary.md` 为准。
- 黑盒节奏见 `rules/02-blackbox-workflow.md`，白盒见 `rules/03-whitebox-workflow.md`，资产发现见 `rules/04-target-discovery.md`。
- 全类型矩阵、差分证据与 confidence 以 `rules/05-testing-policy.md` 为准。
- 正式 SRC 报告只从 `rules/06-reporting.md` 进入；其他文件不得重新定义报告等级或格式。
- 工具选择与凭证注入以 `rules/07-tool-routing.md` 为准，凭证只能从环境变量注入。
- CORS 永久 N/A：不测试、不写报告、不打开 `知识库/cors-test.md`；跨站写转 CSRF，跨权读转授权。
