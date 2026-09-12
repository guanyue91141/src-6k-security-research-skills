# XSLT / XML Transformation 安全审查（2026）

> status: mixed  
> last_reviewed: 2026-09

仅在业务确实存在 XML/XSLT 转换、报表或文档生成流水线时按需加载，不作为常规开场项。

现代审查重点：

- stylesheet 是否来自可信来源；
- 参数与 stylesheet 本体是否分离；
- processor 是否启用 extension function；
- URI resolver 与外部资源访问是否受限；
- Saxon、libxslt、JAXP 等实现的安全配置是否明确；
- XML parser 与 XSLT processor 的外部实体/外部资源策略是否一致。

不同 XSLT 版本和 processor 能力差异很大，结论必须记录实际实现与配置。

相关专题：`xxe-test.md`、`injection-test.md`、`ssrf-test.md`。
