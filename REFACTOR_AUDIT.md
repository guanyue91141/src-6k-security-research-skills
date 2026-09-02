# SRC-6K Skills 重构体检

## 体检范围

本次扫描覆盖 `rules/`、`skills/`、`docs/`、`mcp-servers/`、`bin/`、配置和根目录文档。体检基线为 2026-09-02。

## 基线统计

| 项目 | 结果 |
| --- | ---: |
| 运行时 rules | 8 份（`rules/00-07`） |
| 历史规则归档 | 11 份（`docs/legacy-rules/`） |
| 知识库文件 | 48 份（不含 README） |
| 入口技能 | `skills/skill/SKILL.md`，按需路由 |

## 已发现问题与处理

1. 原 `SKILL.md` 同时承担触发、黑盒、白盒、工具、报告和知识库索引，已改为短入口；细节移入分层 rules 和 workflows。
2. `researcher-blackbox-whitebox.md` 文件头重复包含完整 Playwright 规则，已归档并由 `rules/07-tool-routing.md` 统一持有工具路由。
3. 原 rules 存在网状“某文件压过某文件”描述，已改为 `00-core` 的 L0-L4 单向优先级。
4. 原项目缺少统一状态与 Evidence-First 数据结构，已在 `00-core`、`05-testing-policy` 中定义，并要求任务写入 `state/`。
5. `fofa_dual.ps1` 曾包含硬编码 FOFA 凭证，已改为环境变量读取；`.env` 和密钥类文件已加入 Git 忽略。
6. 未发现 `#U...` 编码目录或同内容 Unicode 重复目录；知识库正文全部保留。
7. `config.toml` 保留跨平台安装模板中的 `C:\Users\USER` 占位路径，安装提示会在目标机器上改写；该占位不视为本仓库凭证。

## 验收命令

```bash
python3 tests/validate_structure.py
git grep -nE 'credential-prefix|AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|known-leaked-key' -- . ':!docs/legacy-rules'
```

第一条应通过；第二条应无输出。归档规则只用于历史追溯，不参与运行时加载。
