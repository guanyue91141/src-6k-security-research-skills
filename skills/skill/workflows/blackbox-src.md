# Blackbox SRC

读取 `rules/02-blackbox-workflow.md`、`rules/05-testing-policy.md` 和目标特征对应的 `知识库/*.md`。先建立接口清单和目标状态，再按证据闸门验证；不得把本文件当作知识库总览。

若用户明确处于网安比赛、CTF、SRC 冲榜或其它时间受限场景，同时进入 `competition-mode.md`：所有线索先进入 Candidate 队列，按边界、能力增量、差分证据、复现性、影响和验证成本排序，高分候选先闭环，失败候选快速止损后继续覆盖。