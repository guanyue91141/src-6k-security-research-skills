# DNS Rebinding / Local Service 边界（2026）

> status: mixed  
> last_reviewed: 2026-09

DNS Rebinding 不作为默认独立专题；在浏览器访问本地服务、设备管理页、开发工具或内网 WebUI 时按需参考。

现代审查重点：

- 本地服务是否依赖 Host/Origin 以外的真实身份认证；
- 浏览器 Private Network Access 等机制是否影响访问模型；
- DNS 结果是否在安全检查后再次解析导致前后结果不一致；
- IPv4、IPv6、localhost 和 link-local 地址是否采用一致的访问策略；
- 本地管理 API 是否只监听必要接口并要求显式认证。

若问题本质属于服务端 URL 获取，转 `ssrf-test.md`；若属于浏览器跨源策略，结合 `cors-test.md` / `csrf-test.md` 判断。
