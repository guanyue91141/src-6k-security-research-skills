# Scoped Target

## 输入

- 用户明确给出的固定资产清单或网段；
- 可选的可用账号或会话。

## 加载

固定范围只跟随给定资产簇及其业务流 host/path，**不主动扩展到无关集团**；进入站内后执行 `rules/02-blackbox-workflow.md` 和 `rules/05-testing-policy.md`。

## 产出

- 范围内资产簇的接口清单与认证/授权判定；
- 差异面受控验证结论，写入 `{名}_dig/state/`。
