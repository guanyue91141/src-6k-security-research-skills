# HTTP/2 / HTTP/3 安全审查（2026）

> status: current  
> last_reviewed: 2026-09

本专题不再只作为“请求走私教材的跳转页”。2026 年应把 HTTP/2、HTTP/3 与 HTTP/1.1 上游之间的协议转换本身纳入架构审查。

## 重点检查

- 边缘代理到上游是否仍降级为 HTTP/1.1；若是，应记录为独立风险面。
- HTTP/2 的 `:authority` 与应用层 Host/虚拟主机规则是否一致。
- 代理、WAF、网关、应用服务器对路径、查询参数、Content-Length、Transfer-Encoding、Expect 等语义是否采用一致的规范化策略。
- H2C、Extended CONNECT、WebSocket over HTTP/2 等功能是否仅在预期边界开放。
- HTTP/3/QUIC 前端转换到 H2/H1 时，安全策略是否与直接访问路径一致。
- 遇到解析差异时，先做最小、无副作用的差分确认，并转 `http-smuggling-test.md` 与 `http-desync-modern-2026.md` 做进一步审查。

## 设计建议

1. 优先保持端到端 HTTP/2+，减少 H2/H3 → H1 降级。
2. 在每个协议边界统一请求规范化策略。
3. 对异常或矛盾的消息边界信息采取拒绝而非猜测。
4. 将代理、WAF、应用服务器升级纳入同一兼容性矩阵，避免单组件修复后出现新的解析差异。
5. 针对连接复用场景加入回归测试，避免把普通 keep-alive/pipelining 行为误判为 desync。

## Legacy

经典 CL.TE / TE.CL / H2 downgrade 技巧继续保留在 `http-smuggling-test.md` 作为历史和兼容性知识，但不再代表全部 HTTP 协议攻击面。
