---
status: current
last_reviewed: 2026-09
sources:
  - https://www.w3.org/TR/webauthn-3/
  - https://fidoalliance.org/passkeys/
  - https://fidoalliance.org/white-paper-displace-password-otp-authentication-with-passkeys/
---

# Passkey / WebAuthn Security 2026

面向 WebAuthn Level 3、passkey 注册/登录/恢复流程的授权安全审查专题。2026-08-25，WebAuthn Level 3 已成为 W3C Recommendation，因此新系统不应再只按“传统 MFA”思路审查。

## 核心判断

Passkey 本身以公钥凭据提供强认证，真正高价值的问题往往出现在：

- 注册/绑定流程；
- 账户恢复与 fallback；
- RP ID / origin 边界；
- credential 与账号绑定；
- 多设备/同步与 device-bound 策略；
- step-up / 高风险动作；
- 服务端 challenge 生命周期；
- 老密码/OTP 通道把整体安全强度降回去。

证据模型：

`Identity → Ceremony → Credential Binding → RP/Origin → Recovery → Capability Delta`

## 1. 建模对象

每个 passkey 流程至少记录：

```text
account_id
rp_id
origin
challenge
credential_id
user_handle
user_verification
resident/discoverable
attestation_policy
synced_or_device_bound
fallback_methods
recovery_methods
```

不要把 WebAuthn 视为一个“登录接口”，它是注册 ceremony、认证 ceremony 和恢复策略的组合。

## 2. Registration Ceremony

重点审查服务端是否确认：

- challenge 由服务端生成且一次性；
- challenge 与当前会话/用户绑定；
- RP ID 与预期域一致；
- origin 在允许集合；
- credential 不可被错误绑定到另一账号；
- user handle 与账号映射稳定；
- 注册新 passkey 前是否需要足够强的当前身份确认；
- 高风险账号是否有明确的 attestation / authenticator policy。

比赛里最值得追的是“已有低权限会话能否给别的账号绑定新凭据”或“恢复流程能否直接引导到新 credential enrollment”。

## 3. Authentication Ceremony

检查：

- challenge 是否短生命周期且不可重放；
- assertion 是否只对预期 RP/origin 有效；
- credential ID 是否必须属于当前目标账号；
- user verification 要求是否与业务风险匹配；
- discoverable credential 登录后的账号选择是否由服务端可信映射完成；
- 登录成功后 session 是否正确轮换；
- 高风险操作是否需要重新认证或 step-up。

不要把“WebAuthn 返回成功”本身当成业务授权，认证成功后仍要继续检查对象/租户/动作授权。

## 4. RP ID / Origin Boundary

WebAuthn 的强度高度依赖 RP 边界。重点复核：

- 主域与子域之间是否有预期共享；
- staging/dev 是否意外共用生产 RP；
- reverse proxy/多域部署是否把 origin 判定做得过宽；
- app/web 混合登录是否有正确的关联域配置；
- callback/redirect 逻辑是否把强认证结果带到错误 origin。

结论必须基于真实配置和 ceremony 行为，不因“存在多个子域”就直接判断风险。

## 5. Passkey Registration as Sensitive Action

把“新增 passkey”当成与“修改密码、修改 MFA、绑定新设备”同级敏感操作。

检查前置条件：

- 是否要求最近一次强认证；
- 仅凭长期 session 是否能添加凭据；
- 添加后是否有通知和审计；
- 是否支持撤销指定 credential；
- 是否能看到 credential 创建时间/设备信息；
- 管理员/客服流程是否能绕开正常验证。

## 6. Recovery / Fallback

FIDO 明确强调：认证体系的安全性取决于最弱恢复路径。若 passkey 登录很强，但恢复仍依赖可钓鱼的弱因子，整体账号安全仍可能降级。

审查矩阵：

| 场景 | 要点 |
|---|---|
| 丢失单设备 | 是否还有安全的备用 credential |
| synced passkey | provider 恢复后是否自动恢复可用性 |
| device-bound | 是否要求备用 authenticator 或高强度恢复 |
| 邮箱恢复 | 是否能直接覆盖 passkey 安全等级 |
| SMS/OTP fallback | 是否成为永久弱入口 |
| 客服人工恢复 | 是否有身份核验、审计、冷却/通知 |

核心原则：恢复机制不应明显弱于被恢复的凭据。

## 7. Synced vs Device-bound

不要笼统认为某一种绝对安全。需要根据目标威胁模型区分：

### Synced passkey

优势：设备丢失恢复更友好，多设备使用便利。

关注：

- passkey provider 账号成为上游信任；
- 新设备 bootstrap；
- provider account recovery；
- 企业是否允许所有 provider。

### Device-bound passkey

优势：更强的设备/硬件绑定。

关注：

- 丢失设备后的恢复；
- 是否配置备用 authenticator；
- 是否因恢复困难重新启用弱密码/OTP。

## 8. Username-less / Discoverable Credentials

检查：

- 服务端是否从 credential/userHandle 可靠映射用户；
- 不得信任客户端提供的 account id 覆盖最终主体；
- 多账号共存时是否出现 credential/account 混淆；
- UI 展示账号和服务端实际会话主体是否一致。

## 9. Step-up 与高风险动作

Passkey 不应只停在“登录成功”。对以下操作建议单独建模：

- 添加/删除 passkey；
- 修改恢复邮箱/手机号；
- 修改支付/提现信息；
- 管理 API token；
- 提权/管理员动作；
- 关闭安全控制。

验证是否有 recent-auth / user verification / transaction context。

## 10. 误报控制

以下通常不能单独报告：

- 网站支持 synced passkey；
- 允许多枚 passkey；
- 未强制 attestation；
- 存在密码兼容登录但没有证明会降低目标安全保证；
- 前端暴露 credential ID（若其本身非秘密且服务端正确授权）。

需要证明真正的新能力，例如：错误账号绑定、弱恢复覆盖强认证、跨 RP/origin 信任、无足够身份确认即可新增 credential。

## 11. 比赛快速检查

时间有限时优先：

1. 注册新 passkey 的前置认证；
2. 修改/恢复账号后能否直接 enrollment；
3. passkey 与 account/userHandle 绑定；
4. RP ID/origin；
5. fallback 是否显著更弱；
6. 删除/撤销 passkey 是否需要 recent-auth；
7. 登录后高风险动作是否继续要求强认证。

## 12. 防御基线

- server-generated one-time challenge；
- challenge 与会话/用户绑定；
- 严格验证 RP ID 与 origin；
- credential 与账号绑定仅由服务端决定；
- 注册/删除凭据属于高风险操作；
- 恢复流程采用不低于目标凭据的保证等级；
- 高风险动作支持 recent-auth / step-up；
- 完整 credential 管理、通知与审计；
- 明确 synced/device-bound 策略。

## References

- W3C Web Authentication Level 3 Recommendation
- FIDO Alliance Passkeys
- FIDO Alliance Passkey Recovery / Deployment Guidance
