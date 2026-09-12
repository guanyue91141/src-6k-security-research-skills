# HTTP Desync 现代化补充（2026）

> status: current  
> last_reviewed: 2026-09

本专题用于补充 `http-smuggling-test.md` 的经典 CL.TE / TE.CL 内容。重点是 2024–2026 的协议边界与代理解析差异，不提供批量化利用步骤。

## 1. 现代问题模型

HTTP desync 的核心仍是两个组件对“一个请求在哪里结束、下一个请求从哪里开始”理解不一致。2026 年需要关注的不只是 `Content-Length` 与 `Transfer-Encoding`：

- 0.CL / CL.0 / H2.0 等消息体长度认知差异；
- TE.0、TE.TE 与 chunk extension 解析差异；
- `Expect: 100-continue` 带来的前后端状态不一致；
- HTTP/2 或 HTTP/3 在边缘被降级到 HTTP/1.1；
- 前端、WAF、CDN、反向代理与应用服务器之间的连接复用；
- 提前响应、请求体丢弃、重写和规范化顺序差异。

## 2. 审查顺序

### 架构层

先画出完整链路：

```text
Client
  -> CDN/WAF
  -> Load Balancer / Reverse Proxy
  -> API Gateway
  -> App Server
```

记录每跳实际使用 H1/H2/H3 中哪一种协议，以及是否发生降级、解 chunk、重新计算长度或重写头部。

### 配置层

检查：

- 是否允许矛盾或重复的消息长度信息；
- 是否允许异常 `Transfer-Encoding` 组合；
- 是否对带 body 的 GET/HEAD/OPTIONS 有一致策略；
- `Expect` 是否在每跳被一致处理；
- 是否复用前端到后端连接；
- 错误请求是否 fail closed。

### 证据层

发现异常时，优先建立可重复的差分证据。普通 HTTP keep-alive、pipelining、偶发超时和 400/502 都不能单独证明 request smuggling。

## 3. 2025+ 研究要点

经典 CL.TE / TE.CL 之后，现代审查应增加：

- 0.CL 类：一端认为请求没有 body，另一端仍读取 body；
- TE.0 类：一端按 chunked 处理，另一端忽略消息体；
- TE.TE 类：不同组件对 chunk extension 或 Transfer-Encoding 语法理解不同；
- Expect 类：`100-continue` 与提前响应使前后端状态机分裂；
- H2/H3 downgrade：二进制协议在边缘安全，但转换到 H1 后重新引入长度歧义。

## 4. 误报控制

- 只有连接复用时出现异常，先排除正常 pipelining。
- 单次延迟或网关 5xx 不足以确认。
- 需要稳定的基线/变体差分，并确认异常来自前后端解析而不是应用业务逻辑。
- 对生产环境采用低频、无副作用验证，不做会影响其他用户请求的确认方式。

## 5. 防御基线

1. 优先端到端使用 HTTP/2+；
2. 能避免时，不在内部链路降级到 HTTP/1.1；
3. 对矛盾消息边界信息直接拒绝；
4. 前端与后端采用一致且严格的 HTTP parser；
5. 持续升级 CDN/WAF/代理/应用服务器，并做组合回归；
6. 必要时关闭上游连接复用作为临时缓解，但应评估性能影响；
7. 对不需要 body 的方法明确拒绝异常 body；
8. 将 desync 回归测试加入网关和代理升级流程。

## 6. 与其它专题的关系

- 经典案例：`http-smuggling-test.md`
- H2/H3：`http2-attacks-test.md`
- WAF / parser differential：`waf-bypass.md`
- 网关 normalization：`api-gateway-test.md`
