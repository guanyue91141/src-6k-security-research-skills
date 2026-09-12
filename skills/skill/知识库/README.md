# 知识库索引

本目录采用“48 个原始兼容基线 + 持续扩展专题”的维护方式。长篇历史知识原则上保留，新标准与新研究优先通过 companion / overlay 文件接入。

## 维护约定

- `current`：已按 2025–2026 标准或研究复核，可作为当前主线。
- `mixed`：主体仍有效，但需要结合目标版本和实现判断。
- `legacy`：主要用于旧系统兼容和历史理解。
- 原始 48 个基线文件不得因扩展而删除。
- 新增专题必须登记在本索引，并通过 `tests/validate_structure.py`。
- 现代专题使用 `status`、`last_reviewed` 与可用时的 `sources` 元数据。
- 第三方 Skill 不整包复制；优先提取增量能力并按本项目 Evidence-First 架构重写。

## 2026 已完成更新/扩展

- `api-security-review.md`
- `cache-modern-2026.md`
- `deserialization-modern-2026.md`
- `graphql-modern-2026.md`
- `http-desync-modern-2026.md`
- `http2-attacks-test.md`
- `llm-security-test.md`
- `csp-bypass-test.md`
- `401-403-bypass.md`
- `clickjacking-test.md`
- `csv-formula-injection-test.md`
- `dns-rebinding-test.md`
- `email-header-injection-test.md`
- `xslt-injection-test.md`
- `grpc-security-2026.md`
- `shadow-api-inventory-2026.md`
- `nextjs-ssr-security-2026.md`
- `k8s-security-review-2026.md`
- `cicd-security-review-2026.md`
- `competition-triage-evidence-2026.md`
- `agent-skill-supply-chain-2026.md`

## 完整文件索引

```text
401-403-bypass.md
agent-skill-supply-chain-2026.md
agent-tool-exec-test.md
api-gateway-test.md
api-security-review.md
authbypass-test.md
cache-modern-2026.md
cache-poisoning-test.md
cicd-security-review-2026.md
clickjacking-test.md
cloud-ide-codex-rce-chain.md
competition-triage-evidence-2026.md
cors-test.md
crlf-injection-test.md
csp-bypass-test.md
csrf-test.md
csv-formula-injection-test.md
dangling-markup-test.md
dependency-confusion-test.md
deserialization-modern-2026.md
deserialization-test.md
dns-rebinding-test.md
el-injection-test.md
email-header-injection-test.md
file-upload-test.md
ghost-bits-cast-test.md
graphql-modern-2026.md
graphql-test.md
grpc-security-2026.md
hpp-test.md
http-desync-modern-2026.md
http-host-header-test.md
http-smuggling-test.md
http2-attacks-test.md
idor-test.md
info-leak-test.md
injection-test.md
insecure-scm-test.md
jndi-injection-test.md
js-reverse-guide.md
k8s-security-review-2026.md
llm-security-test.md
logic-test.md
nextjs-ssr-security-2026.md
oauth-jwt-test.md
open-redirect-test.md
path-traversal-lfi-test.md
prototype-pollution-test.md
race-condition-test.md
recon-methodology.md
shadow-api-inventory-2026.md
ssrf-test.md
subdomain-takeover-test.md
type-juggling-test.md
waf-bypass.md
websocket-test.md
xslt-injection-test.md
xss-test.md
xxe-test.md
打穿短表.md
```

**当前合计：60 个知识文件**（不含本 README）。
