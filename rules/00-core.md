# 核心规则与优先级

<!-- Scope: 全部安全研究任务。Priority: L1。Owns: 规则层级、加载边界、状态与证据入口。Does Not Own: 具体漏洞打法和报告版式。 -->

## 规则层级

按以下顺序裁决冲突，低层不得覆盖高层：

```text
L0 用户当前指令
L1 研究边界与数据安全（01-safety-boundary.md）
L2 工作流（02-blackbox-workflow.md / 03-whitebox-workflow.md / 04-target-discovery.md）
L3 测试策略（05-testing-policy.md）与工具路由（07-tool-routing.md）
L4 知识库与历史经验（skills/skill/知识库/）
```

旧版长规则仅作为迁移归档，位于 `docs/legacy-rules/`，不作为运行时规则加载。知识库按需打开，不要求每次通读。

## 统一状态

每个目标都维护一个状态对象；任何动作必须至少改变一个字段，否则视为空转：

```yaml
target: {status: queued} # queued | recon | active | blocked | completed
surface: {frontend: false, api: false, authenticated: false,
  object_ids: [], upload: false, callback: false, search: false,
  websocket: false, graphql: false}
tested: {auth: pending, authorization: pending, injection: pending,
  ssrf: pending, xss: pending, upload: pending, logic: pending,
  exposure: pending}
findings: []
next_actions: []
```

任务级状态文件放在任务根的 `{名}_dig/state/`；没有任务根时先按 04-target-discovery 创建。

## 输出入口

- 黑盒正式漏洞：只按 `06-reporting.md` 及其引用的报告规则落盘。
- 白盒审计：按 `03-whitebox-workflow.md` 输出证据链，除非用户要求，不把低置信点写成正式 SRC 报告。
- 未确认线索进入状态文件的 `findings`，不得伪装成漏洞结论。
