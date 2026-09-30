# 工作流入口

五个入口文件只负责**加载顺序与完成判据**，详细方法论由 `rules/` 提供，专题细节由 `知识库/` 提供。

## 入口一览

| 文件 | 适用输入 | 触发条件 | 产出 |
| --- | --- | --- | --- |
| `blackbox-src.md` | URL、域名、APP、在线平台 | 给定资产且非比赛模式 | 接口清单、类型矩阵状态、受控验证结论 |
| `whitebox-audit.md` | 本地源码、GitHub 项目、class/jar | 输入为代码而非运行目标 | Phase 0-6 证据链、`state/findings.json` |
| `discovery-target.md` | 集团或品牌名 | 未给定具体资产 | `资产/种子队列.md`、存活资产清单 |
| `scoped-target.md` | 固定资产清单 | 范围已明确 | 范围内资产簇的测试结论 |
| `competition-auto-hunt.md` | 授权比赛/CTF/靶场固定目标 | 要求自动或持续找漏洞 | 候选队列、Finding/Reject 裁决、Coverage Gate |
| `competition-mode.md` | — | 仅兼容旧引用 | 跳转到 `competition-auto-hunt.md` |

## 共同契约

- 加载前先读 `rules/00-core.md`（优先级、状态、证据入口）与 `rules/01-safety-boundary.md`（边界）。
- 过程状态写入任务根 `{名}_dig/state/`；没有任务根时先按 `rules/04-target-discovery.md` 创建。
- 判定证据与 confidence 统一以 `rules/05-testing-policy.md` 为准，不在此复述。
- 正式报告只从 `rules/06-reporting.md` 进入。
