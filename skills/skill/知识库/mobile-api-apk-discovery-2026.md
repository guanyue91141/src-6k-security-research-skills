---
status: current
last_reviewed: 2026-09
sources:
  - https://mas.owasp.org/MASTG-TEST-0233/
  - https://mas.owasp.org/
---

# Mobile API / APK Endpoint Discovery 2026

面向授权测试、CTF 与比赛环境的移动端攻击面恢复专题。目标不是“反编译越多越好”，而是把 APK/IPA 中真正能映射到后端 API 的信息恢复成结构化资产，再交给 API、授权、业务逻辑和版本差分专题继续判断。

## 核心原则

移动端包通常是后端接口目录、旧版本兼容逻辑和环境信息的重要来源，但静态字符串本身不等于真实攻击面。OWASP MASTG 也明确指出：APK 中出现 URL 只说明存在字符串或引用，是否真正被使用还取决于运行时条件和应用配置。

因此证据链统一采用：

`Artifact → Reference → Runtime Reachability → Identity/Role → API Behavior → Impact`

任何只停留在“APK 里搜到一个 URL”的结果都只能记为 Signal。

## 1. 需要恢复的资产

优先提取：

- API base URL、备用域名、region endpoint；
- `/v1`、`/v2`、`beta`、`legacy`、`internal` 等版本线索；
- GraphQL endpoint、WebSocket/SSE 地址；
- gRPC / protobuf service 名称与 `.proto` 资源；
- OAuth/OIDC issuer、client_id、redirect URI；
- deep link / app link / custom scheme；
- 文件上传、对象存储、CDN、预签名 URL 相关主机；
- feature flag、remote config、environment 名称；
- debug/staging/dev host；
- WebView 加载地址和 JS bridge 名称。

## 2. 静态分析入口

Android 常见观察面：

- `AndroidManifest.xml`；
- `res/xml/network_security_config.xml`；
- `assets/`、`res/raw/`；
- native library 字符串；
- Retrofit/OkHttp client 定义；
- GraphQL query/mutation 文本；
- protobuf descriptor；
- BuildConfig、flavor、remote config key；
- deep link intent-filter。

不要把如下内容直接判定为漏洞：

- hardcoded public API base URL；
- public OAuth client_id；
- analytics endpoint；
- SDK 内部测试 URL；
- 已废弃但运行时不可达的字符串。

## 3. URL 与 Endpoint 去噪

对提取结果至少记录：

```text
source_file
string_or_symbol
host
path
version
protocol
reference_count
runtime_observed
notes
```

优先级建议：

1. 运行时真实访问；
2. 被业务 client 代码直接引用；
3. 出现在配置/descriptor；
4. 仅存在于第三方 SDK；
5. 无引用的孤立字符串。

## 4. Runtime Correlation

静态恢复后，应与受控运行时行为对齐：

- 真实启动后是否连接该 host；
- 登录前后 endpoint 是否变化；
- 不同账号/角色是否调用不同 API；
- 新旧 app 版本是否使用不同 API version；
- 某 endpoint 是否只在特定 feature flag 下出现；
- 请求是否经过 mobile gateway/BFF；
- 响应是否包含服务版本或后端路由提示。

这一步用于防止把 dead code、SDK 示例、旧资源误认为活跃接口。

## 5. Mobile → Shadow API

移动端最有价值的场景通常不是“发现一个接口”，而是发现浏览器端已经不再使用的旧后端。

当 APK/IPA 提取到：

- 较旧 `/v1`；
- legacy hostname；
- deprecated path；
- 旧 GraphQL operation；
- 旧 protobuf service；

应联动 `shadow-api-inventory-2026.md`，对比当前 Web/新版本 App 的认证、授权、字段暴露和业务约束。

## 6. API 模型重建

将恢复到的接口映射成：

```text
身份 Identity
对象 Object
动作 Action
租户 Tenant
数据 Data
客户端版本 Client Version
服务版本 API Version
```

然后交给 `api-security-review.md` 做 BOLA/BFLA/Mass Assignment/异步任务/字段授权检查。

## 7. Deep Link / App Link

重点不是枚举 scheme，而是检查边界：

- link 是否只完成导航，还是能触发敏感动作；
- 是否需要已登录会话；
- 参数是否再次经服务端授权；
- callback state 是否绑定到当前会话；
- universal/app link 是否有可信域绑定；
- WebView 或跨应用跳转是否改变身份上下文。

比赛中只有在能够证明“跨过服务端安全边界”时，才把 deep link 问题升级为 finding。

## 8. WebView / Hybrid App

看到 WebView、React Native、Flutter、Capacitor/Cordova 时补查：

- 加载来源是否固定；
- JS bridge 暴露能力是否最小化；
- Web 内容和本地能力是否有清晰信任边界；
- 业务 token 是否被暴露给不需要的前端上下文；
- deep link → WebView → API 是否形成跨层状态链。

## 9. Secrets 判断

移动包里的值分三类：

### Public-by-design

- API base URL；
- OAuth public client_id；
- telemetry/project identifier。

### Sensitive only if privilege-bearing

- API token；
- service credential；
- signing/private key；
- 长期可复用的 bearer credential。

### Context dependent

- Firebase/云服务配置；
- object storage identifier；
- map/service key。

判断标准不是“字符串长得像 Key”，而是它是否能带来新的服务端能力。

## 10. 比赛快速流程

```text
APK/IPA
  ↓
manifest/config/resources
  ↓
URL/API/proto/deeplink inventory
  ↓
runtime correlation
  ↓
current Web / new App diff
  ↓
API authz + business state review
  ↓
capability delta
```

时间有限时，优先追：

- 老 API 版本；
- 内部/管理 service 名；
- debug/staging 仍活跃入口；
- GraphQL/gRPC descriptor；
- deep link 到敏感业务动作；
- mobile-only endpoint。

## 11. 误报控制

以下不能单独成立：

- APK 可反编译；
- 找到 base URL；
- 发现 public client_id；
- 发现旧路径但无法访问；
- App 使用 HTTP 字符串但实际不允许 cleartext；
- 第三方 SDK 包含测试 host。

至少证明：真实可达 + 当前有效 + 跨越了认证/授权/业务/数据边界之一。

## 12. 防御基线

- 后端永远不信任客户端版本或客户端 UI；
- 所有对象和动作在服务端重新授权；
- 下线旧 API，而不是只从新客户端删除调用；
- debug/staging 与生产凭据/数据隔离；
- secret 不嵌入客户端；
- mobile gateway/BFF 与内部服务继续实施方法级授权；
- 对深链和跨应用回调做会话/状态绑定。

## References

- OWASP Mobile Application Security Testing Guide / MASTG
- OWASP MASTG-TEST-0233 Hardcoded HTTP URLs
