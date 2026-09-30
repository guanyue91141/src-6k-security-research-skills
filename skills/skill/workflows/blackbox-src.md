# Blackbox SRC

## 输入

- 授权范围内的 URL、域名、APP 或在线平台；
- 可选的可用账号或会话；
- 可选的用户给定清单或资产簇。

## 加载

读取 `rules/02-blackbox-workflow.md`、`rules/05-testing-policy.md`，并按目标信号从 `知识库/README.md` 定位专题后只加载命中文件。不得把本文件当作知识库总览。

## 产出与完成判据

- 接口清单、认证/授权判定、全类型矩阵状态（`tested / pending / N/A / rejected`）；
- 有差分面的受控验证结论与状态更新（写入 `{名}_dig/state/`）；
- 完成前必须回看是否存在未覆盖的高价值类型。

若用户明确处于网安比赛、CTF、SRC 冲榜或其它时间受限场景，同时进入 `competition-auto-hunt.md`：所有线索先进入 Candidate 队列，按边界、能力增量、差分证据、复现性、影响和验证成本排序，高分候选先闭环，失败候选快速止损后继续覆盖。
