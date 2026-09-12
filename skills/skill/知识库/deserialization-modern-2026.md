# 反序列化现代安全基线（2026）

> status: current  
> last_reviewed: 2026-09

本专题作为 `deserialization-test.md` 的现代化 companion。旧文件中的 Java/PHP/Python 历史案例继续保留；新系统审查优先关注“是否仍允许不可信数据进入通用对象反序列化器”和运行时提供的过滤机制。

## 1. Java

Java 现代基线应优先检查 `ObjectInputFilter` 与反序列化过滤策略，而不是默认依赖 gadget 黑名单。

重点包括：

- JVM-wide filter 与 stream-specific filter 是否存在；
- 允许的类集合是否按业务场景收窄；
- graph depth、array length、references、stream bytes 是否设合理上限；
- RMI/JMX/消息队列等入口是否使用独立过滤策略；
- 第三方库升级后是否新增可序列化类型或改变过滤行为；
- 对象输入是否有明确的认证、完整性与来源边界。

Java 25 仍提供基于 JEP 290 / JEP 415 的 serialization filtering 机制，因此“JDK 新版本自动解决 Java 反序列化风险”是不成立的。

## 2. Python

Python 审查重点从“能否构造 pickle gadget”前移到数据格式选择：

- 不可信输入不使用 `pickle` / `dill` / `cloudpickle`；
- ML/AI 模型文件加载区分纯权重与任意 Python 对象；
- 模型仓、缓存、对象存储中的 artifact 需要来源校验；
- YAML、jsonpickle 等扩展格式采用安全加载模式；
- 异步任务和消息队列不要把外部输入直接反序列化为任意对象。

## 3. .NET

新系统不应依赖 BinaryFormatter。审查：

- 是否仍存在历史兼容入口；
- 是否迁移到明确 schema 的序列化格式；
- 类型信息是否由服务端固定，而不是由输入控制；
- 迁移层是否为了兼容而重新开启危险行为。

## 4. PHP

PHP `unserialize()` 仍应视为高风险入口。优先：

- 只处理服务端可信数据；
- 必须兼容时使用严格 `allowed_classes`；
- 对 session/cache/queue 数据做完整性保护；
- 评估 PHAR、框架缓存和历史数据迁移路径。

## 5. 通用审查模型

```yaml
format: java-serialization | pickle | php-serialize | yaml | custom
source: internal | user | queue | cache | artifact
integrity_protected: true | false
allowed_types: explicit | broad | none
resource_limits: configured | absent
version_migration: reviewed | unknown
```

## 6. 现代优先级

优先排查：

1. 外部可控对象流；
2. CI/CD、模型、插件、缓存和消息系统中的 artifact；
3. 跨版本兼容层；
4. “为了方便”关闭过滤器的局部代码；
5. 对象图资源消耗与拒绝服务风险。

## 7. Legacy

经典 ysoserial、旧 JDK remote class loading、历史 WebLogic/Shiro 链仍保留用于遗留系统识别，但应加目标版本条件，不作为所有 Java 应用的默认判断路径。

## 8. 防御建议

- 优先使用无任意类型语义的数据格式；
- 对象类型 allowlist 而非 denylist；
- 使用 Java ObjectInputFilter 等运行时防护；
- 对 artifact 做签名、来源和完整性校验；
- 设置对象图资源上限；
- 将反序列化入口纳入版本升级与依赖变更回归。
