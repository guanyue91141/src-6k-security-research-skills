# Upstream Skill Sources / 第三方 Skill 来源记录

> 本文件记录用于“研究、对照、重写”的公开 Agent Skill 项目。默认不直接整包复制；新增专题应在 frontmatter 的 `sources` 中标记具体来源。

## 已吸收增量能力

### murrtada/bug-bounty-agent-skills

- 类型：Bug Bounty / Offensive Security Agent Skills
- 规模：93 个 Skills
- License：MIT（仓库 LICENSE 明确声明，并注明上游 Agentic-Bug-Hunter 为 MIT）
- 本项目参考：
  - `hunt-grpc` → `grpc-security-2026.md`
  - `hunt-shadow-api` → `shadow-api-inventory-2026.md`
  - `hunt-nextjs` → `nextjs-ssr-security-2026.md`
  - `hunt-k8s` → `k8s-security-review-2026.md`
  - `hunt-cicd` → `cicd-security-review-2026.md`
  - `triage-validation` → `competition-triage-evidence-2026.md`
- 整合原则：保留方法论和现代攻击面分类，删除大批量/破坏性默认动作，改成 Evidence-First 与低影响验证。

### MoonFuji/invariant-first-bug-bounty

- 类型：Evidence-gated Bug Bounty Agent Skill
- License：MIT
- 本项目参考：
  - target/candidate ledger 思路；
  - invariant-first；
  - capability delta；
  - finding 关闭不等于 target clean；
  - 独立/新鲜上下文 review 概念。
- 整合到：`competition-triage-evidence-2026.md`。

### theinfosecguy/razin

- 类型：SKILL.md 静态安全扫描器
- License：MIT
- 本项目参考：
  - 把 Markdown Skill 当供应链代码审查；
  - 检查 Prompt privilege escalation、远程执行、secret、未固定依赖；
  - 引入第三方 Skill 前先静态扫描。
- 整合到：`agent-skill-supply-chain-2026.md`。

## 已审查但暂未直接吸收

### whisper-sec/whisper-skills

- License：MIT
- 方向：Threat Intelligence / OSINT / bulk triage / Cypher / brand protection。
- 判断：架构和 Agent Skill 工程化质量较好，但当前分支优先服务 Web/API/网安比赛，暂不增加威胁情报专题。

### Eyadkelleh/awesome-skills-security

- 方向：将 SecLists 的 fuzzing/password/payload/pattern 等资源包装成 Agent Skills。
- 判断：资源型价值高，但与现有知识库中的 payload/wordlist 使用方式重叠较多；不把大词典复制进知识库。后续可做 `references/wordlists` 外挂层。

### akashrpatil/awesome-offensive-security-skills / CyberSkills Elite 类集合

- 方向：大型 Offensive Security Skill catalog，覆盖 Web、API、云、AD、AI Red Team、IR 等。
- 判断：覆盖广但超出当前项目目标较多；只作为“缺口雷达”，不整包合入，避免 AD/C2/持久化等内容污染 SRC/比赛路由。

## 引入规则

1. 先查 License，再读 Skill 正文；
2. 不因“公开 GitHub”就假定可任意复制；
3. 优先重写方法论、模型与检查表，而非复制原文；
4. 保留来源仓库与具体 Skill 名；
5. 不导入真实 credential、token、目标数据；
6. 不导入默认无限 scope、自动批准、高破坏性动作；
7. 每个新专题必须进入知识库 README；
8. 结构修改后运行 `tests/validate_structure.py`；
9. 比赛环境使用前固定依赖版本，避免临场拉取 `latest`。
