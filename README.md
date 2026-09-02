# SRC-6K Security Research Skills

一套面向授权安全研究的 Grok/Codex 身份包，覆盖黑盒 SRC 挖掘、固定范围测试、品牌/集团资产发现、JS/API 分析、漏洞验证、中文报告和白盒 0day 审计。

## 目录

```text
rules/                    # 00-07 分层运行时规则
skills/skill/             # 兼容现有安装路径的安全研究技能入口
skills/skill/知识库/       # 48 个按需加载的专题模块
docs/legacy-rules/        # 重构前规则归档，不参与运行时加载
tests/                    # 结构与回归检查
mcp-servers/fofa_MCP/     # FOFA MCP 服务（凭证仅从环境变量读取）
```

## 设计要点

- `rules/00-core.md` 定义 L0-L4 单向优先级和统一目标状态模型。
- 黑盒、白盒、资产发现和测试策略分离，入口技能仅负责路由和按需加载。
- 所有发现遵循 Evidence-First：`Signal → Hypothesis → Controlled Test → Differential Evidence → Impact → Finding`。
- 知识库正文全部保留；CORS 按当前研究策略标记为 N/A。
- `.env`、私钥和密钥类文件默认被 Git 忽略，FOFA 脚本不包含硬编码凭证。

## 验证

```bash
python3 tests/validate_structure.py
```

## 本地配置

复制 `mcp-servers/fofa_MCP/.env.example` 为 `.env`，按需填写 FOFA 环境变量。不要把凭证写入规则、知识库、配置模板或 Git 提交。

详细重构记录见 [REFACTOR_AUDIT.md](REFACTOR_AUDIT.md)。
