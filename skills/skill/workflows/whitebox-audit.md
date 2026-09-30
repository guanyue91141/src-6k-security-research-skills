# Whitebox Audit

## 输入

- 本地源码、GitHub 项目或反编译产物（class/jar）；
- 可选的构建方式与可运行验证条件；
- 可选的已知历史 CVE 或修复 commit 线索。

## 加载

读取 `rules/03-whitebox-workflow.md`，并按实际语言/框架从 `知识库/README.md` 定位专题后只加载命中文件。不加载黑盒资产发现流程。

## 产出与完成判据

- 信任边界与数据流模型（入口 → 处理 → sink）；
- 每个发现回答输入可控性、前置条件、绕过、影响与可复现 PoC；
- 审计记录写入 `state/findings.json`，按 confidence 归档，确认项才进入正式报告。
