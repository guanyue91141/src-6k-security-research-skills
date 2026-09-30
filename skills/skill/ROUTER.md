# 安全研究路由

本文件是 `SKILL.md` 的入口判定细则：只决定**进入哪个工作流**和**加载顺序**，不改变 `rules/00-core.md` 的优先级，也不改变 `rules/01-safety-boundary.md` 的边界。

## 入口判定

| 条件 | 入口 | 说明 |
| --- | --- | --- |
| 用户明确说明网安比赛、CTF、靶场、授权测试，给出固定 URL/域名/IP/资产，且要求自动或持续找漏洞 | `workflows/competition-auto-hunt.md` | 锁面模式上的增强调度层，维护候选队列与时间预算 |
| 普通 URL、域名、APP 或在线平台 | `workflows/blackbox-src.md` | 锁面黑盒 |
| 输入本地源码、GitHub 项目或 class/jar | `workflows/whitebox-audit.md` | 不加载黑盒资产发现 |
| 只给集团或品牌 | `workflows/discovery-target.md` | 自由跳，建立种子队列后回到黑盒 |
| 明确给固定资产清单 | `workflows/scoped-target.md` | 只跟随范围内资产簇 |
| 用户提到已废弃入口 `competition-mode` | `workflows/competition-mode.md` | 仅兼容跳转，统一转 `competition-auto-hunt.md` |

## 加载顺序

```text
rules/00-core.md              # 优先级、状态模型、证据与输出入口
rules/01-safety-boundary.md   # 边界与最小伤害（不可越过）
  → 入口工作流（上表）
  → rules/05-testing-policy.md + rules/07-tool-routing.md
  → 知识库/打穿短表.md → 知识库/README.md 定位专题 → 只加载命中文件
```

比赛自动模式是锁面黑盒工作流的增强调度层：具体测试继续继承 `rules/02-blackbox-workflow.md`、`rules/05-testing-policy.md` 和命中的知识专题。

## 不要做的事

- 不在入口层罗列全部知识专题——专题检索统一走 `知识库/README.md` 与 `知识库/registry.yaml`。
- 不因为「首页需要登录」「扫描器没有命中」「已确认一个漏洞」就结束流程。
- 不把状态码、版本号、报错、schema 或单次异常直接写成 Finding。
- 不加载 `disabled` 状态的专题；CORS 永久不挖。
