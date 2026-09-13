# 黑盒 SRC 工作流

<!-- Scope: URL、域名、APP 和在线平台。Priority: L2。Owns: 锁面/自由跳/比赛模式判定、进站顺序、完成判据。Does Not Own: 具体测试细节与报告版式。 -->

## 模式判定

- 固定 URL、文档或清单：锁面，只跟随该资产簇的业务 host、子域和 path，不主动扩展到无关集团。
- 只有品牌/集团：自由跳，进入 `04-target-discovery.md` 的种子闭环。
- 用户明确说网安比赛、CTF、SRC 冲榜、限时赛或要求尽快产出有效结果：在锁面/自由跳之上启用**比赛模式**，进入 `skills/skill/workflows/competition-auto-hunt.md`，并加载 `skills/skill/知识库/competition-triage-evidence-2026.md`。
- 已登录目标先建立对象与权限关系；未登录目标先确认关键业务面和认证边界。

## 进站顺序

1. 确认业务面、信任边界和当前会话；登录壳不是不可测结论，继续寻找同资产簇真实业务入口。
2. 抽取前端与接口暴露的 path、参数、对象 ID、hidden 路由和版本信息，形成接口清单；回包中新出现的对象和 URL 进入队列。
3. 对清单执行 `05-testing-policy.md` 的全类型矩阵；只有存在真实业务差分的输入才进入深入验证。
4. 比赛模式下，把 Signal 先转成 Candidate 并评分；优先闭环高分候选。候选连续两次受控验证没有增加边界、能力或证据时停止该分支，切换下一条；死亡 Candidate 不等于目标安全。
5. 一个目标完成后再换站；发现与状态必须去重并持续更新。

## 比赛状态板

比赛模式维护 `{名}_dig/state/candidate-board.md` 或等价结构，至少记录：

```text
candidate_id | surface | hypothesis | score | boundary | capability_delta | evidence | status | next_action
```

`status` 只使用 `queued / testing / confirmed / rejected / hold`。每次验证后更新分数与下一动作；不允许只积累 URL、报错和截图而没有候选状态。

## 完成判据

每个存活目标至少完成：接口清单、认证/授权判定、全类型矩阵状态（`tested/pending/N/A/rejected`）、有差分面的受控测试、证据状态更新。瘦壳、同构壳或纯登录 HTML 只做快速证伪，不耗时空转。

比赛模式下优先保证：高分 Candidate 已闭环或明确 Reject/Hold；尚未覆盖的高价值类型保留为 `pending`，不能因为确认一个发现就把整个目标标记 completed。