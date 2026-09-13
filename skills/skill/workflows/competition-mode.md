# Competition Mode

面向网安比赛、CTF、SRC 冲榜和其它时间受限的授权安全研究场景。目标不是减少覆盖，而是把验证顺序改成“高价值候选优先 + 快速证伪 + 证据闭环”。

## 1. 入口

同时读取：

- `rules/02-blackbox-workflow.md`
- `rules/05-testing-policy.md`
- `../知识库/competition-triage-evidence-2026.md`
- 当前目标特征对应的专题知识

建立 `candidate-board.md`，所有线索必须先成为 Candidate，不能从状态码、报错或版本信息直接写成 Finding。

## 2. 三层队列

### A 队列：立即验证

满足多数条件：

- 已出现明确身份、对象、租户或状态边界；
- 可构造稳定 A/B 对照；
- 成功后会获得真实新增能力；
- 验证成本低且可回滚；
- 结果能直接形成比赛答案或高质量报告证据。

### B 队列：补证据

已经有可信 Signal，但缺少第二主体、对象、稳定控制组或完整业务状态。保留最小下一动作，不允许反复做同类无增量请求。

### C 队列：快速证伪

只有版本、路径、banner、schema、错误文本、单次异常或其它弱信号。先做一组最小差分；没有能力增量就 Reject。

## 3. 每轮决策

每轮只回答四件事：

1. 当前最高分 Candidate 是什么？
2. 最小哪一步能让它“确认或死亡”？
3. 这一步是否增加 Boundary / Capability Delta / Evidence？
4. 如果没有，下一 Candidate 是谁？

禁止同时铺开大量没有明确判定条件的分支。

## 4. 候选卡

推荐状态格式：

```yaml
id: C-001
surface: api/profile
hypothesis: cross-subject authorization gap
score: 9
attacker: normal-user
boundary: user-object
baseline: own-object
variant: other-object
capability_delta: pending
evidence: partial
status: testing
next_action: build-minimal-differential-control
```

确认后补充 `impact / reproducibility / cleanup`；Reject 时必须写统一 reject reason。

## 5. 排序与止损

排序使用 `rules/05-testing-policy.md` 的 0–12 分模型。出现以下任一情况立即降级或停止当前分支：

- 连续两次验证没有增加边界、能力或证据；
- 只能证明组件存在，无法证明安全边界被跨越；
- 需要不可回滚或超范围动作才能继续；
- 结果依赖偶发超时、单次错误或无法复现的状态；
- 需要大量重复请求，但尚无稳定差分依据。

## 6. 赛题优先地图

按目标特征选专题，而不是按漏洞名机械轮询：

- 多租户/API：`api-security-review.md`、`shadow-api-inventory-2026.md`
- 移动端/旧客户端：`mobile-api-apk-discovery-2026.md`
- SPA/SSR：`spa-source-map-api-recovery-2026.md`、`nextjs-ssr-security-2026.md`
- 复杂业务流程：`business-state-machine-security-2026.md`
- gRPC/多协议：`grpc-security-2026.md`
- WebAuthn/Passkey：`passkey-webauthn-security-2026.md`
- Webhook/异步回调：`webhook-integrity-2026.md`
- 云原生：`k8s-security-review-2026.md`、`cicd-security-review-2026.md`
- AI/Agent：`llm-security-test.md`

## 7. 提交前闸门

准备比赛答案或正式报告前必须同时满足：

- 攻击者起点明确；
- 安全边界明确；
- A/B 差分明确；
- Capability Delta 明确；
- 可从干净状态复现；
- 影响不依赖猜测；
- 已记录最小验证与清理动作。

不满足时继续作为 Candidate，不把“疑似”包装成确认结果。

## 8. 比赛结束复盘

保留三类数据：

- confirmed：哪些信号最早预测到最终结果；
- rejected：哪些假阳性最浪费时间；
- hold：哪些候选只因环境/账号/时间不足未闭环。

下一场比赛优先调整 Candidate 评分，而不是简单增加更多知识文件。