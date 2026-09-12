# Web Cache 现代安全基线（2026）

> status: current  
> last_reviewed: 2026-09

本专题作为 `cache-poisoning-test.md` 的现代化 companion。传统 unkeyed header 与 cache deception 知识继续保留；现代重点是 cache、CDN、reverse proxy 与 origin 对 URL/路径/查询参数的规范化是否一致。

## 1. Cache Key 建模

记录实际参与 cache key 的维度：

- scheme / host / authority；
- normalized path；
- query 参数及排序；
- method；
- Vary headers；
- authentication / tenant context；
- device / locale 等变体。

缓存层和应用层对同一维度必须有一致理解。

## 2. Path / Delimiter 差异

现代 cache deception 重点不只是“加静态后缀”，而是不同组件对 delimiter、path parameter、encoded separator、suffix 和 rewrite 的理解差异。

审查目标是判断：缓存是否把一个响应归入与 origin 实际资源语义不同的 key，而不是机械尝试固定后缀列表。

## 3. Cache / Origin Normalization

检查：

- URL decode 次数；
- dot-segment；
- repeated slash；
- semicolon/path parameter；
- query 参数排序、忽略与归一化；
- host / authority；
- rewrite 前后使用哪一个 path 作为 cache key。

## 4. 私有响应缓存

- 登录态页面、账户数据、导出和 API 响应是否明确 private/no-store；
- CDN 是否忽略应用返回的 cache-control；
- tenant/user 维度是否进入 key 或完全禁止共享缓存；
- logout 后边缘缓存是否仍可能返回旧的私有对象。

## 5. Cache Poisoning

现代判断仍遵循两步：

1. 某输入影响 origin response；
2. 同一输入不在 cache key 或规范化方式不同。

仅发现某个 header 不在 key 并不足以确认风险。

## 6. API 与 SSR

对 Next.js/SSR/Edge rendering、GraphQL GET、API Gateway 和 Server Component cache，需额外确认用户/租户上下文是否参与缓存隔离。

## 7. 防御建议

- 敏感响应默认不进入共享缓存；
- cache 与 origin 统一 URL normalization；
- key 明确包含所有会改变响应身份/租户的维度；
- 不依赖文件扩展名猜测“静态资源”；
- CDN / reverse proxy / framework 升级后运行 cache regression tests；
- 对 rewrite、redirect 与 edge function 建立端到端缓存模型。
