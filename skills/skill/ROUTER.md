# 安全研究路由

用户明确说明网安比赛、CTF、靶场、授权测试，并给出固定 URL、域名、IP 或资产，且要求自动/持续找漏洞 → `workflows/competition-auto-hunt.md`。

普通 URL、域名、APP 或在线平台 → `workflows/blackbox-src.md`。

输入本地源码、GitHub 项目或 class/jar → `workflows/whitebox-audit.md`。

只给集团/品牌 → `workflows/discovery-target.md`；明确给固定清单 → `workflows/scoped-target.md`。

比赛自动模式仍属于锁面黑盒工作流的增强调度层：具体测试继续继承 `rules/02-blackbox-workflow.md`、`rules/05-testing-policy.md` 和对应知识专题。

路由只决定入口，不改变 `rules/00-core.md` 的优先级和 `rules/01-safety-boundary.md` 的边界。
