---
name: security-research
description: |
  SRC 漏洞挖掘与白盒 0day 审计技能。用户提供 URL、域名、APP、在线平台、源码、GitHub 项目或审计关键词时触发。
  支持黑盒 SRC、固定范围测试、品牌/集团资产发现、JS/API 分析、漏洞验证与中文报告，以及本地源码审计。
---

# Security Research Agent

本技能保留黑盒 SRC 与白盒审计两套能力，入口只做模式判定和按需路由，详细规则不在这里重复。

## 路由

1. URL、域名、APP 或在线平台：读取 `ROUTER.md` → `workflows/blackbox-src.md`。
2. 本地源码、GitHub 项目、class/jar：读取 `ROUTER.md` → `workflows/whitebox-audit.md`。
3. 只给集团/品牌：进入 `workflows/discovery-target.md`，建立种子队列后回到黑盒流程。
4. 明确固定清单：进入 `workflows/scoped-target.md`，只测试范围内资产簇。
5. API/接口平台、OpenAPI、REST、微服务接口审查：除对应漏洞专题外，优先加载 `知识库/api-security-review.md` 建立身份—对象—动作—租户—数据模型。

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

## 输出

每个动作都要更新任务根 `{名}_dig/state/` 中的目标状态、已测类型、线索和下一步。黑盒正式报告放任务根 `报告/`，资产与 JS 分别放 `资产/`、`js/`。白盒过程记录数据流、sink、前置条件、影响和可复现验证。
