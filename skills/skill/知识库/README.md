# 知识库索引

本目录是 security-research 技能的**按需知识层**：进站先看 `打穿短表.md`，再按目标信号在本索引定位专题，只加载命中的文件。知识库是增强材料，不是能力上限，**禁止每站通读全库**。

- 机器可读元数据（唯一元数据源）：`registry.yaml`
- 每个专题文件头部的 YAML frontmatter 是同一份元数据的快照
- 物理文件名保持扁平一层不变，以兼容 `给朋友的提示词.txt` 移交脚本与 `打穿短表.md` 的裸文件名指针

## 怎么检索

```text
目标信号（框架 / 协议 / 业务形态）
  → 在下文「分类路由表」找到候选专题
  → 只打开命中的文件（超长篇可先开点名节）
  → 需要机器可读字段时查 registry.yaml
```

## 怎么新增或修改

```text
1. 在 registry.yaml 的 topics 登记（id / file / title / category / status / purpose / triggers / inputs / outputs / related）
2. 运行 python3 tests/sync_knowledge_meta.py    # 元数据写进文件 frontmatter，并修正失效引用
3. 运行 python3 tests/validate_structure.py    # 校验索引、分类、元数据与数量声明
4. 如需在短表建立指针，先读现稿再改
```

`registry.yaml` 的 `topics[].file` 集合必须与实际目录文件集合完全一致，校验脚本会强制比对。

## 元数据字段

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定标识，跨文件引用用 id 而非路径 |
| `title` | 中文标题 |
| `category` | 分类 id，取值见「分类路由表」 |
| `status` | `current` / `mixed` / `legacy` / `disabled` |
| `purpose` | 一句话用途，说明这个专题回答什么问题 |
| `triggers` | 触发信号；出现这些信号才加载本专题 |
| `inputs` | 使用本专题前需要具备的目标信息 |
| `outputs` | 本专题应产出的证据或结论形态 |
| `related` | 关联或 companion 专题 |

## 状态口径

| 状态 | 含义 | 使用方式 |
| --- | --- | --- |
| `current` | 已按 2025–2026 标准或研究复核 | 当前主线，优先加载 |
| `mixed` | 主体仍有效，需结合目标版本与实现判断 | 结合现场版本使用 |
| `legacy` | 旧系统兼容与历史理解 | 命中具体信号才用，不作现代默认方案 |
| `disabled` | 项目明确停用 | 不进入路由，仅保留技术资料 |

## 分类路由表

### recon 侦察与资产发现

> 在进入具体测试前确认资产、接口、对象与暴露面。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `recon-methodology.md` | 资产测绘与侦察节奏：种子闭环、FOFA 限流与去噪 | 资产发现 / 种子队列 / FOFA | mixed |
| `subdomain-takeover-test.md` | 子域接管检测与验证 | CNAME 悬空 / 三方服务 404 | legacy |
| `insecure-scm-test.md` | 暴露的 SCM 与构建产物 | `.git` / `.svn` / 源码泄漏 | legacy |
| `info-leak-test.md` | 信息泄露与凭证暴露，过认钥闸 | health / actuator / 硬编码密钥 | mixed |
| `js-reverse-guide.md` | 从 JS 恢复隐藏路由、加密参数与盐 | 加密参数 / hidden 路由 | mixed |
| `spa-source-map-api-recovery-2026.md` | 从构建产物与 source map 恢复 route 与 API client | source map / Vite / SPA | current |
| `mobile-api-apk-discovery-2026.md` | 从 APK/IPA 与 deep link 恢复 mobile-only 接口 | APK / IPA / deep link | current |

### auth 认证与会话

> 登录、凭据、令牌与认证链的完整性与可绕过性。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `authbypass-test.md` | 认证链缺陷：会话、重置、改绑、换票、2FA、扫码 | 登录页 / SSO / 找回密码 / 换绑 | mixed |
| `oauth-jwt-test.md` | JWT/OAuth/SAML 令牌与断言安全 | JWT / OAuth / SAML / 断言 | mixed |
| `passkey-webauthn-security-2026.md` | WebAuthn ceremony、绑定与 RP/origin 校验 | Passkey / WebAuthn / 无密码登录 | current |
| `401-403-bypass.md` | 区分「绕登录页」与「对象授权」 | 401 / 403 / 登录墙 / SSO 壳 | mixed |
| `type-juggling-test.md` | 弱类型比较绕过（PHP） | 弱比较 / magic hash / token 校验 | legacy |

### access 授权与接口安全

> 对象、租户与方法级授权边界，以及接口模型本身。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `idor-test.md` | 越权与对象级授权，读/列表差分取证 | 对象 ID / user_id / 列表接口 / 越权 | mixed |
| `api-security-review.md` | 「身份—对象—动作—租户—数据」五维建模与验证 | REST / OpenAPI / 微服务接口 | current |
| `shadow-api-inventory-2026.md` | Shadow/旧版本接口的鉴权与行为差分 | API 版本漂移 / legacy endpoint | current |
| `graphql-test.md` | GraphQL 经典测试：introspection、字段授权、批量查询 | GraphQL / introspection | mixed |
| `graphql-modern-2026.md` | GraphQL 现代基线：Federation、persisted query、subscription | Federation / persisted query | current |
| `grpc-security-2026.md` | gRPC/Protobuf 方法级授权与网关鉴权断层 | gRPC / Protobuf / grpc-web | current |
| `api-gateway-test.md` | 网关与后端路径/编码规范化不一致导致的绕过 | API 网关 / 路径规范化 | legacy |

### injection 注入与解析

> 可控数据进入解析器、执行器或文件系统后导致的越界。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `injection-test.md` | SQL / 命令 / SSTI 按栈选探针 | 参数过滤 / 405 / 搜索框 | mixed |
| `xss-test.md` | 按输出上下文选择与变形 payload | 回显 / 富文本 / DOM / 存储型 | mixed |
| `xxe-test.md` | XXE 外部实体注入 | XML 解析 / DOCTYPE / 实体 | legacy |
| `el-injection-test.md` | 表达式语言注入（EL/SpEL/OGNL） | EL / SpEL / OGNL / Java 模板 | legacy |
| `jndi-injection-test.md` | JNDI 注入与远程类加载 | JNDI / RMI / LDAP / lookup | legacy |
| `xslt-injection-test.md` | XSLT/XML 转换安全（按需） | XSLT / 报表生成 / 文档流水线 | mixed |
| `prototype-pollution-test.md` | 原型链污染与打到模板的 gadget 链 | `__proto__` / 深合并 / Node | mixed |
| `deserialization-test.md` | 不安全反序列化（Java/PHP/Python/.NET） | 反序列化 / gadget / pickle | mixed |
| `deserialization-modern-2026.md` | 反序列化现代基线：通用反序列化器与运行时过滤 | 缓存或队列对象 / artifact | current |
| `ghost-bits-cast-test.md` | Java 字符窄化导致的校验绕过 | char 收窄 / Ghost Bits | legacy |
| `path-traversal-lfi-test.md` | 路径穿越与本地文件包含 | file 参数 / alias / LFI | mixed |
| `ssrf-test.md` | SSRF、内网探测与云元数据路径差 | url 参数 / callback / 云元数据 | mixed |
| `file-upload-test.md` | 上传追到越权/执行/SSRF 链 | 上传点 / 附件 / 导入 / 对象存储 | mixed |
| `http-host-header-test.md` | Host/XFH 污染与重置投毒 | Host / X-Forwarded-Host / 密码重置 | mixed |
| `hpp-test.md` | HTTP 参数污染（只作成因，不单独交） | 参数污染 / 重复参数 | legacy |
| `dependency-confusion-test.md` | 依赖混淆（现场识别内部包名后打） | 内部包名 / 私有 registry | legacy |
| `crlf-injection-test.md` | CRLF 头注入（默认不单独交） | CRLF / 响应拆分 | legacy |
| `email-header-injection-test.md` | 邮件生成与 Header 边界 | 邮件 / 邀请 / 账号恢复 | mixed |
| `csv-formula-injection-test.md` | CSV/表格导出公式注入 | CSV 导出 / Excel / 报表 | mixed |

### client 客户端与浏览器

> 浏览器侧信任边界、跨站行为与前端防御架构。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `csrf-test.md` | CSRF 与跨站写取证 | CSRF / token / 扫码登录 | mixed |
| `clickjacking-test.md` | 嵌框防护与敏感界面匹配度 | X-Frame-Options / 嵌框 | mixed |
| `csp-bypass-test.md` | CSP/Trusted Types 防御架构审查 | CSP / Trusted Types / nonce | current |
| `open-redirect-test.md` | 开放重定向 | redirect / 跳转参数 | legacy |
| `dangling-markup-test.md` | 悬空标记抽 token（默认不交） | 悬空标记 / token 抽取 | legacy |

### protocol 协议与传输

> 协议解析差异、长连接与传输层信任边界。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `http-smuggling-test.md` | HTTP 请求走私（经典 CL.TE/TE.CL） | 走私 / Transfer-Encoding / 解析差 | mixed |
| `http-desync-modern-2026.md` | Desync 现代补充：代理与协议转换边界 | desync / 代理 / HTTP/1.1 上游 | current |
| `http2-attacks-test.md` | HTTP/2、HTTP/3 与协议转换架构审查 | HTTP/2 / HTTP/3 / h2c | current |
| `websocket-test.md` | WebSocket 握手、Origin、CSWSH 与越权消息 | WebSocket / Origin / Socket.IO | mixed |
| `dns-rebinding-test.md` | DNS Rebinding 与本地服务边界（按需） | DNS rebinding / 内网 WebUI | mixed |

### logic 业务逻辑与状态机

> 业务流程的状态迁移、不变量与并发正确性。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `logic-test.md` | 支付/流程/验证码中的跳步与加字段 | 订单流程 / 验证码 / 优惠券 | mixed |
| `business-state-machine-security-2026.md` | 状态机与不变量：Skip/Reorder/Replay/Parallel | 订单 / 审批 / 积分 / 异步任务 | current |
| `race-condition-test.md` | 支付/券/库存竞态与单包手法 | 竞态 / 并发 / 库存超卖 | mixed |
| `webhook-integrity-2026.md` | Webhook 签名、新鲜度、去重与幂等 | webhook / callback / 支付回调 | current |

### platform 现代应用与基础设施

> 框架、缓存、云原生与 AI 平台的专项边界。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `cache-poisoning-test.md` | 缓存投毒与欺骗（经典 unkeyed/deception） | 缓存 / X-Cache / 缓存欺骗 | mixed |
| `cache-modern-2026.md` | 现代缓存基线：cache/CDN/proxy/origin 规范化一致性 | CDN / 共享缓存 / cache key | current |
| `nextjs-ssr-security-2026.md` | RSC、Server Actions、SSR/ISR 与缓存边界 | Next.js / RSC / Server Actions | current |
| `k8s-security-review-2026.md` | RBAC、ServiceAccount、容器边界 | Kubernetes / RBAC / ServiceAccount | current |
| `cicd-security-review-2026.md` | 流水线、OIDC、Runner、artifact/cache 信任边界 | GitHub Actions / Jenkins / OIDC | current |
| `llm-security-test.md` | LLM/Agent 边界：身份、数据、工具、执行 | LLM / RAG / Agent / MCP | current |
| `agent-tool-exec-test.md` | 对话口工具真实执行（需先确认执行边界） | 工具执行 / 对话口 | mixed |
| `agent-skill-supply-chain-2026.md` | 第三方 Skill/MCP/rules 供应链审查 | 第三方 Skill / install script | current |
| `cloud-ide-codex-rce-chain.md` | 云 IDE 弱口令到 RCE 的组合链路 | 云 IDE / Codex / 编程台 RPC | mixed |

### method 方法与索引

> 跨专题的检索入口、规避手法与候选筛选方法。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `打穿短表.md` | 进站首选索引，按目标特征指向具体专题 | 进站 / 开场 | current |
| `waf-bypass.md` | WAF 绕过手法（确认存在 WAF 后按需） | WAF / 拦截 / 编码混淆 | legacy |
| `competition-triage-evidence-2026.md` | 候选筛选与差分证据，筛掉假阳性 | 比赛 / CTF / 时间受限 | current |

### disabled 停用

> 项目明确不挖不写，仅保留技术资料，不进入路由。

| 文件 | 用途 | 触发信号 | 状态 |
| --- | --- | --- | --- |
| `cors-test.md` | CORS（永久停用） | 不加载 | disabled |

## companion 主从关系与冲突消解

同一主题同时存在现代基线与经典手册时，按此表确定加载顺序与职责边界，**不要同时把两份当主线**：

| 主题簇 | 现代主文件（优先） | 经典兼容文件 | 边界规则 |
| --- | --- | --- | --- |
| 缓存 | `cache-modern-2026.md` | `cache-poisoning-test.md` | 先建缓存键与规范化模型；经典 unkeyed/deception 手法按需补 |
| GraphQL | `graphql-modern-2026.md` | `graphql-test.md` | 现代部署先看 Federation/persisted query；经典 introspection/字段授权按需补 |
| 反序列化 | `deserialization-modern-2026.md` | `deserialization-test.md` | 先判不可信数据是否进通用反序列化器；经典 gadget 链按需补 |
| HTTP 协议 | `http2-attacks-test.md`、`http-desync-modern-2026.md` | `http-smuggling-test.md` | 有代理/协议转换先做协议层审查；经典 CL.TE/TE.CL 按需补 |
| LLM/Agent | `llm-security-test.md` | `agent-tool-exec-test.md` | 先做边界审查；仅在确认真实工具执行边界后验证执行差 |
| 401/403 | `401-403-bypass.md` | `authbypass-test.md` | 先分流判断是登录墙还是对象授权，再决定加载哪一份 |
| 授权模型 | `api-security-review.md` | `idor-test.md`、`api-gateway-test.md` | 先建五维模型定位边界，再针对对象/网关层取证 |
| CORS | —（停用） | `cors-test.md` | 永久 N/A，不进入路由；跨站写转 `csrf-test.md`，跨权读转 `idor-test.md` |

职责边界统一口径：`打穿短表.md` 只做索引；`recon-methodology.md`、`js-reverse-guide.md`、`spa-source-map-api-recovery-2026.md` 负责“怎么发现”；各 `*-test.md` 负责“怎么测”；是否落盘成正式报告只认 `rules/06-reporting.md`，本目录不复述报告格式。

## 完整文件索引（65）

`401-403-bypass.md`、`agent-skill-supply-chain-2026.md`、`agent-tool-exec-test.md`、`api-gateway-test.md`、`api-security-review.md`、`authbypass-test.md`、`business-state-machine-security-2026.md`、`cache-modern-2026.md`、`cache-poisoning-test.md`、`cicd-security-review-2026.md`、`clickjacking-test.md`、`cloud-ide-codex-rce-chain.md`、`competition-triage-evidence-2026.md`、`cors-test.md`、`crlf-injection-test.md`、`csp-bypass-test.md`、`csrf-test.md`、`csv-formula-injection-test.md`、`dangling-markup-test.md`、`dependency-confusion-test.md`、`deserialization-modern-2026.md`、`deserialization-test.md`、`dns-rebinding-test.md`、`el-injection-test.md`、`email-header-injection-test.md`、`file-upload-test.md`、`ghost-bits-cast-test.md`、`graphql-modern-2026.md`、`graphql-test.md`、`grpc-security-2026.md`、`hpp-test.md`、`http-desync-modern-2026.md`、`http-host-header-test.md`、`http-smuggling-test.md`、`http2-attacks-test.md`、`idor-test.md`、`info-leak-test.md`、`injection-test.md`、`insecure-scm-test.md`、`jndi-injection-test.md`、`js-reverse-guide.md`、`k8s-security-review-2026.md`、`llm-security-test.md`、`logic-test.md`、`mobile-api-apk-discovery-2026.md`、`nextjs-ssr-security-2026.md`、`oauth-jwt-test.md`、`open-redirect-test.md`、`passkey-webauthn-security-2026.md`、`path-traversal-lfi-test.md`、`prototype-pollution-test.md`、`race-condition-test.md`、`recon-methodology.md`、`shadow-api-inventory-2026.md`、`spa-source-map-api-recovery-2026.md`、`ssrf-test.md`、`subdomain-takeover-test.md`、`type-juggling-test.md`、`waf-bypass.md`、`webhook-integrity-2026.md`、`websocket-test.md`、`xslt-injection-test.md`、`xss-test.md`、`xxe-test.md`、`打穿短表.md`

**当前合计：65 个知识文件**（不含本 README 与 `registry.yaml`）。
