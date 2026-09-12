---
status: current
last_reviewed: 2026-09
sources:
  - theinfosecguy/razin
---

# Agent Skill / Prompt Supply Chain 安全审查 2026

> 用于引入第三方 Skill、MCP、规则包、安装脚本前的静态审查。这个专题保护“安全 Agent 本身”，防止把高权限恶意规则或供应链风险带进比赛环境。

## 1. 为什么需要

安全类 Skill 往往拥有：

- shell / Python / Node 执行能力；
- 浏览器与登录态；
- MCP 工具；
- GitHub / 云环境 / FOFA 等凭据；
- 大量自动批准或连续执行规则。

因此第三方 `SKILL.md`、`AGENTS.md`、安装脚本和 MCP 配置都应按代码供应链处理，而不是“Markdown 所以无害”。

## 2. 引入前五层检查

### 2.1 来源与许可证

记录：

- upstream 仓库；
- commit/tag；
- LICENSE；
- 是否 fork/镜像；
- 是否有可验证维护者；
- 是否直接复制了第三方受限内容。

优先采用 MIT/Apache/BSD 等许可清晰的内容，并以“重写/归纳”方式整合。

### 2.2 Prompt / Rule 行为

重点查：

- “忽略系统/用户限制”类指令；
- 强制默认授权；
- 禁止询问确认；
- 自动扩大 scope；
- 修改全局 Agent 身份；
- 覆盖 `AGENTS.md`、rules、config；
- 把失败解释为“继续申请更高权限”。

安全研究知识可以强，但运行权限不应因此无限放大。

### 2.3 可执行代码

审查：

- `curl|bash` / `wget|sh`；
- `npx ...@latest`、未固定 pip/npm/git 依赖；
- `subprocess` / `os.system` / PowerShell；
- 下载后执行；
- 自更新；
- 修改 shell profile；
- 写 SSH key / cron / systemd；
- 隐蔽外联、遥测、webhook。

## 3. Secrets / Credential

禁止第三方 Skill 把真实 secret 写入：

- Markdown；
- `config.toml`；
- shell/PowerShell；
- `.env` 示例；
-测试 fixture；
- commit history。

统一采用环境变量/secret store，并在日志和报告中脱敏。

## 4. MCP / Tool Trust

对每个 MCP/tool 建表：

| 项 | 内容 |
|---|---|
| 来源 | package/repo/version |
| 权限 | filesystem/network/browser/account |
| 可写范围 | repo / home / system |
| credential | 读取哪些 token |
| network | 可连接哪些外部服务 |
| approval | ask / restricted / auto |

第三方 Tool 的输出是**外部数据**，不能自动当可信指令执行。

## 5. Dependency Pinning

推荐：

- npm/pip/uv 固定可复核版本；
- Git dependency 固定 commit SHA；
- 保存 lockfile；
- 记录 hash / provenance；
- 定期升级，但升级前重新审查 diff。

比赛环境尤其不建议在开赛当天首次执行 `@latest` 安装。

## 6. 静态检查规则

可借鉴 Razin 一类 Skill scanner 的思路，至少扫描：

- frontmatter / YAML 异常；
- 外链和远程下载；
- shell execution；
- secret pattern；
- prompt injection / privilege escalation 文案；
- scope expansion；
- absolute path / 用户目录覆盖；
- auto-approve / yolo 模式；
- package latest / unpinned git。

扫描结果只是 Signal，仍需人工读上下文。

## 7. 引入流程

```text
Discover
  → License check
  → Static scan
  → Manual review
  → Extract useful concepts
  → Rewrite into local style
  → Add source attribution
  → Run structure tests
  → Diff review
```

不要直接执行第三方 `install.sh` 后再审计。

## 8. 本项目规则

向本仓库引入第三方内容时：

- 原始 48 个兼容基线不删；
- 新专题登记 `status` / `last_reviewed` / `sources`；
- 不原样复制超长 payload 库；
- 不引入硬编码凭据；
- 不把全局权限切换成 `always-approve`；
- 先接路由，再投入日常使用；
- 通过 `tests/validate_structure.py`。
