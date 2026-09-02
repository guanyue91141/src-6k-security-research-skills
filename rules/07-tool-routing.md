# 工具路由

<!-- Scope: 浏览器、FOFA、脚本和辅助工具。Priority: L3。Owns: 工具选择与凭证注入。Does Not Own: 漏洞结论。 -->

- 浏览器交互、JS 渲染页面、截图和多步流程优先使用 Playwright MCP；静态 HTTP 读取可用普通请求工具。浏览器规则正文只维护在本文件，旧版见 `docs/legacy-rules/playwright-browser-mcp.md`。
- FOFA 只通过项目内 MCP `mcp-servers/fofa_MCP/fofa.py`，账号从环境变量读取，禁止把 key 写进代码、规则或提交记录；限流按 04-target-discovery 处理。
- nuclei 仅用于已知 CVE、actuator、swagger 等明确暴露面辅助验证，不替代全类型矩阵。
- JS 分析优先记录接口 path、参数和密文/盐/演示号来源；Burp 用于抓包重放，脚本只做可复现的小范围验证。
