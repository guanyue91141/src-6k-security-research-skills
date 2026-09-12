# API Security Review

面向授权安全评估、代码审计与上线前检查的 API 安全专题。目标不是机械扫描，而是建立“身份—对象—动作—租户—数据”五维模型，并用最小影响方式验证边界是否正确。

## 一、建模

对每个 API 记录：

- 身份：匿名、普通用户、管理员、服务账号、第三方应用。
- 对象：资源主键、租户 ID、组织 ID、项目 ID、父子资源关系。
- 动作：读、创建、更新、删除、导出、审批、绑定、分享。
- 数据：敏感字段、凭证、内部标识、审计字段。
- 约束：状态机、角色、租户、来源、时间窗、一次性令牌。

推荐最小状态表：

```yaml
endpoint: /api/example
method: GET
authn: required
authz_dimension: [owner, tenant, role]
object_ids: [id]
state_constraints: []
sensitive_fields: []
rate_limit: unknown
observed_errors: []
```

## 二、重点审查面

### 1. 对象级授权

确认服务端是否对每次对象访问重新绑定当前主体，而不是仅依赖前端隐藏、路径难猜、对象 ID 非连续等弱约束。

代码审计时重点看：

- ORM 查询是否只有 `id = ?`，没有 owner/tenant 条件。
- Service 层是否存在“先查对象，后鉴权”但错误分支仍返回数据。
- 批量接口是否只校验第一个对象。
- 导出、附件、历史版本、异步任务等旁路是否复用相同授权逻辑。

### 2. 功能级授权

检查后台功能、审批、运营接口、批量接口、内部接口是否仅依赖路由前缀或前端角色判断。

### 3. Mass Assignment

对更新/创建接口确认是否使用显式字段白名单。重点关注：

- role / isAdmin / status / ownerId / tenantId
- balance / quota / price / discount
- verified / approved / enabled
- createdBy / updatedBy / audit 字段

白盒优先检查 DTO、schema、serializer、ORM model bind、`Object.assign`、自动映射器。

### 4. 分页与过滤

验证分页、排序、过滤条件不能跨租户放大数据范围；注意 total/count 与列表正文可能走不同 SQL，导致侧信道或统计越权。

### 5. 导出与异步任务

CSV/PDF/ZIP 导出、报表任务、消息队列任务经常绕过同步 API 的授权层。检查任务创建时和真正执行时是否都绑定主体与租户。

## 三、认证与会话

- Token 是否区分访问令牌、刷新令牌、一次性令牌。
- 登出、改密、禁用账号后旧会话是否按设计失效。
- Refresh Token 是否旋转并检测重放。
- OAuth/OIDC 回调是否严格校验 state、nonce、redirect URI。
- 服务到服务凭证是否限制 audience、scope 和有效期。

## 四、速率与业务约束

速率限制不是只看 HTTP 429，还要确认限制维度：IP、账号、设备、租户、目标对象、验证码会话。对支付、优惠、库存、审批、邀请码等高价值动作，应有幂等、状态机和并发保护。

## 五、证据要求

结论至少应包含：

1. 基线请求；
2. 变体请求；
3. 主体/租户/对象差异；
4. 服务端响应差异；
5. 是否可稳定复现；
6. 最小影响说明；
7. 修复建议对应到具体授权层或数据查询条件。

没有差分证据时只记录为 hypothesis，不写成 confirmed finding。

## 六、修复建议

- 统一在服务端集中鉴权，不依赖前端。
- 查询层显式绑定主体/租户。
- DTO/serializer 使用字段白名单。
- 批量接口逐项鉴权或先构造可访问集合。
- 导出、异步任务复用统一授权上下文。
- 高风险状态变更加入幂等、审计、风控与二次确认。
