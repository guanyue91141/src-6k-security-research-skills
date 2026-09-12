# 知识库索引

实战方法论 / 测试清单 / 场景矩阵。与 `SKILL.md` 流程配合使用。

## 使用约定

- 进站先读 `打穿短表.md`；对得上再打开对应模块看细节。文件不长就整篇开；超长篇可先开点名节，不够就继续开。禁止每站通读本目录
- 磁盘有 `*src经验.md` 才开专篇，没有不算缺。开 `SKILL.md` 不会再带集团日记
- 短表和「注入/SSRF/XSS/RCE」都不是上限。本站过全类型矩阵；四件套打在有差分面上（防空窗），不是只测这四类，也不是每个 path 喷 `'`。有会话时越权/逻辑与四件套同硬
- 方便和能力优先；省 token 是顺带，不挡开模块
- 篇内跳转使用本目录真实文件名；与运行时 `rules/` 冲突时以分层规则为准
- `cors-test.md` 保留作兼容与分流；`llm-security-test.md` 已升级为 2026 LLM/Agent 安全审查入口
- 正式 SRC 报告统一由 `rules/06-reporting.md` 进入
- 原始 48 个专题是兼容基线，不得因扩展而删除；新增专题必须在本索引登记

## 2026 现代化状态

- `current`：已按 2025–2026 标准/研究更新，可作为当前主线。
- `mixed`：主体仍有效，但混有旧协议、旧框架或历史技巧，需要结合版本判断。
- `legacy`：仅用于兼容旧系统或理解历史攻击面，不应作为现代默认方案。
- 长篇历史知识原则上不删除；通过 companion/overlay 专题补充新标准，避免重写时丢失实战经验。

已完成第一批：

- `http2-attacks-test.md`：升级到 HTTP/2、HTTP/3、协议降级与 parser consistency 审查。
- `http-desync-modern-2026.md`：补 0.CL、TE.0、TE.TE、Expect、H2/H3→H1、误报控制与防御基线。
- `llm-security-test.md`：从占位分流升级为 LLM / Agent / RAG / Tool / Memory 安全审查。

## 文件清单

| 文件 | 说明 |
|------|------|
| `打穿短表.md` | 挖洞手法索引（一行/指针；正文仍在各模块） |
| `401-403-bypass.md` | 业务 API 401/403 分流 |
| `api-gateway-test.md` | API 网关 |
| `api-security-review.md` | API 对象/功能授权、Mass Assignment、批量与异步任务、Token 生命周期与证据模型 |
| `agent-tool-exec-test.md` | 对话口工具执行边界 |
| `authbypass-test.md` | 认证绕过 |
| `cache-poisoning-test.md` | 缓存投毒/欺骗 |
| `clickjacking-test.md` | 点击劫持 |
| `cloud-ide-codex-rce-chain.md` | 云 IDE/Codex 系审查专题 |
| `cors-test.md` | CORS 兼容占位/分流 |
| `crlf-injection-test.md` | CRLF 注入 |
| `csp-bypass-test.md` | CSP 绕过相关参考 |
| `csrf-test.md` | CSRF |
| `csv-formula-injection-test.md` | CSV 公式注入 |
| `dangling-markup-test.md` | Dangling Markup |
| `dependency-confusion-test.md` | 依赖混淆 |
| `deserialization-test.md` | 反序列化 |
| `dns-rebinding-test.md` | DNS Rebinding |
| `el-injection-test.md` | EL / 表达式注入 |
| `email-header-injection-test.md` | 邮件头注入 |
| `file-upload-test.md` | 文件上传 |
| `ghost-bits-cast-test.md` | Ghost Bits |
| `graphql-test.md` | GraphQL |
| `hpp-test.md` | HTTP 参数污染 |
| `http-desync-modern-2026.md` | HTTP Desync 2026 overlay：0.CL / TE.0 / TE.TE / Expect / H2-H3→H1 |
| `http-host-header-test.md` | Host Header |
| `http-smuggling-test.md` | HTTP 请求走私经典与实战知识 |
| `http2-attacks-test.md` | HTTP/2 / HTTP/3 与协议转换安全审查 |
| `idor-test.md` | 越权 / IDOR / BOLA / BFLA |
| `info-leak-test.md` | 信息泄露 |
| `injection-test.md` | 注入总览 |
| `insecure-scm-test.md` | 不安全源码管理暴露 |
| `jndi-injection-test.md` | JNDI 注入 |
| `js-reverse-guide.md` | JS/API 分析 |
| `llm-security-test.md` | LLM / Agent / RAG / Tool / Memory 2026 安全审查 |
| `logic-test.md` | 业务逻辑 |
| `oauth-jwt-test.md` | OAuth/JWT/SAML/OIDC |
| `open-redirect-test.md` | Open Redirect |
| `path-traversal-lfi-test.md` | 路径穿越 / LFI |
| `prototype-pollution-test.md` | Prototype Pollution |
| `race-condition-test.md` | 竞态 |
| `recon-methodology.md` | 侦察方法论 |
| `ssrf-test.md` | SSRF |
| `subdomain-takeover-test.md` | 子域接管 |
| `type-juggling-test.md` | Type Juggling |
| `waf-bypass.md` | WAF 场景参考 |
| `websocket-test.md` | WebSocket |
| `xslt-injection-test.md` | XSLT 注入 |
| `xss-test.md` | XSS |
| `xxe-test.md` | XXE |

**当前合计：50 个知识文件**（不含本 README），其中原始 48 个为兼容基线，后续允许持续扩展；结构测试会阻止误删基线文件并检查新增专题是否完成索引。
