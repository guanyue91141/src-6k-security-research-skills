# GraphQL 现代安全基线（2026）

> status: current  
> last_reviewed: 2026-09  
> baseline: GraphQL September 2025 Specification

本专题作为 `graphql-test.md` 的现代化 companion。旧文件中的 introspection、字段授权、批量查询等知识继续保留；现代部署还需要覆盖 Federation、persisted query、subscription、复杂度控制与 schema 生命周期。

## 1. Schema 与可见性

- Introspection 是否开放应由部署场景决定，不能把“可 introspect”本身直接等同漏洞。
- 内部字段、deprecated 字段与实验字段仍必须执行完整授权。
- Schema registry、SDL、生成文档和客户端缓存应按敏感度治理。
- 自定义 scalar、directive 和 resolver 需要独立输入验证。

## 2. 对象与字段授权

GraphQL 授权至少分三层：

1. operation / resolver 功能权限；
2. object / tenant 所有权；
3. field / property 级敏感字段访问。

授权应放在服务端业务/数据层，而不是依赖前端隐藏字段或只在顶层 resolver 检查一次。

## 3. Query Cost / Resource Consumption

现代 GraphQL 防护不能只看 query depth。建议组合：

- depth；
- field count；
- list multiplier；
- resolver cost；
- pagination limit；
- timeout / cancellation；
- per-user / per-tenant budget。

对 alias、fragment 和嵌套 list 的成本应按实际 resolver 工作量计算。

## 4. Persisted Queries

APQ / persisted query 可减少任意查询面，但需要审查：

- query hash 与正文绑定；
- registry 写入权限；
- 生产环境是否允许任意客户端注册新 query；
- 旧 query 的撤销和版本生命周期；
- CDN/cache key 是否包含影响响应身份的上下文。

## 5. Federation

GraphQL Federation / supergraph 场景重点检查：

- gateway 与 subgraph 的信任边界；
- 身份/租户上下文是否可靠传递；
- subgraph 是否假定“来自 gateway 就自动可信”；
- `_entities` 等实体解析仍需对象级授权；
- schema composition 后是否出现原本未暴露的字段组合。

## 6. Subscription

subscription / live query 需要持续授权，而不是只在连接建立时认证一次。角色、租户或对象权限变化后，已有 subscription 应按设计更新或终止。

## 7. OneOf 与输入类型

GraphQL September 2025 规范包含 OneOf Input Objects 等能力。采用新输入模型时应确认：

- 服务端库与 schema 版本一致；
- validation、codegen 与运行时行为一致；
- input coercion 不会绕过业务字段白名单。

## 8. 防御建议

- resolver 与数据层集中授权；
- 对敏感字段做 property-level authorization；
- 查询复杂度按真实成本限制；
- persisted query registry 有严格写权限；
- Federation 保留端到端主体/租户上下文；
- subscription 定期重新验证授权状态；
- schema 变更进入安全回归。
