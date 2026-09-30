# SRC-6K Skills 重构体检

## 体检范围

本次扫描覆盖 `rules/`、`skills/`、`docs/`、`mcp-servers/`、`bin/`、配置和根目录文档。体检基线为 2026-09-02；知识库组织与元数据规范化复核于 2026-09-30。

## 基线统计

| 项目 | 结果 |
| --- | ---: |
| 运行时 rules | 8 份（`rules/00-07`） |
| 历史规则归档 | 11 份（`docs/legacy-rules/`） |
| 知识库文件 | 65 份（不含 README 与 registry.yaml） |
| 入口技能 | `skills/skill/SKILL.md`，按需路由 |

## 已发现问题与处理

1. 原 `SKILL.md` 同时承担触发、黑盒、白盒、工具、报告和知识库索引，已改为短入口；细节移入分层 rules 和 workflows。
2. `researcher-blackbox-whitebox.md` 文件头重复包含完整 Playwright 规则，已归档并由 `rules/07-tool-routing.md` 统一持有工具路由。
3. 原 rules 存在网状“某文件压过某文件”描述，已改为 `00-core` 的 L0-L4 单向优先级。
4. 原项目缺少统一状态与 Evidence-First 数据结构，已在 `00-core`、`05-testing-policy` 中定义，并要求任务写入 `state/`。
5. `fofa_dual.ps1` 曾包含硬编码 FOFA 凭证，已改为环境变量读取；`.env` 和密钥类文件已加入 Git 忽略。
6. 未发现 `#U...` 编码目录或同内容 Unicode 重复目录；知识库正文全部保留。
7. `config.toml` 保留跨平台安装模板中的 `C:\Users\USER` 占位路径，安装提示会在目标机器上改写；该占位不视为本仓库凭证。

## 2026-09-30 知识库组织与元数据规范化

本轮针对「AI 更易理解、检索和调用」重组知识层，未删改任何挖洞技术正文。

| 问题 | 处理 |
| --- | --- |
| 65 个专题平铺一层，无分类，检索必须先读 README 清单 | 保持扁平文件名以兼容移交脚本与短表指针，新增 10 个分类的分类路由表（`知识库/README.md`）与机器可读元数据（`知识库/registry.yaml`） |
| 元数据三套写法混用（YAML frontmatter / `> status:` 引用块 / 完全没有） | 统一为同一 schema 的 YAML frontmatter；`> status:`、`> last_reviewed:`、`> scope:`、`> baseline:` 引用块被吸收进 frontmatter |
| 正文大量引用旧路径（`~/.grok/rules/`、`dig-scope`、`src-value-hunting`、`hunt-iter`、`vuln-report-format` 等），与现行 `rules/00-07` 不对应 | 按映射表修正到现行规则路径；`tests/sync_knowledge_meta.py` 固化该映射，可重复运行 |
| `SKILL.md` 用 22 条扁平路由列表承担知识库分发，与 README、比赛 Dispatch 表三处重复维护 | `SKILL.md` 收敛为用途 / 触发场景 / 两步路由 / 输入输出契约 / 约束；专题检索下沉到索引层，`ROUTER.md` 只保留入口判定表 |
| companion 关系（cache / graphql / deserialization / http-smuggling）只在正文一句话声明，易被同时当主线 | README 增加「companion 主从关系与冲突消解」表，逐簇声明优先文件与边界规则 |
| 各专题的输入输出无统一位置 | 每个专题 frontmatter 增加 `purpose / triggers / inputs / outputs / related`；工作流入口统一补「输入 / 加载 / 产出」三段 |
| 校验无法发现元数据缺失或索引漂移 | `validate_structure.py` 新增 frontmatter 字段完整性、`category`/`status` 合法性、`registry` 与文件集及 `id` 集合一致性检查 |

## 验收命令

```bash
python3 tests/sync_knowledge_meta.py --check   # 元数据应与 registry.yaml 一致，输出 0 个待同步
python3 tests/validate_structure.py            # 结构、元数据、分类与索引校验
git grep -nE 'credential-prefix|AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|known-leaked-key' -- . ':!docs/legacy-rules'
```

前两条应通过；第三条除匹配到本条命令自身的字面量外应无输出。归档规则只用于历史追溯，不参与运行时加载。
