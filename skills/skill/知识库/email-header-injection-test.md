# 邮件生成与 Header 安全（2026）

> status: mixed  
> last_reviewed: 2026-09

传统邮件头注入优先级较低，但账号恢复、邀请、通知和多租户邮件系统仍需要正确区分地址、显示名、主题、正文与 transport header。

## 审查重点

- 使用成熟邮件库构造 message，不手工拼 SMTP/MIME 原始文本；
- To/Cc/Bcc/Reply-To/From 等字段采用结构化地址 API；
- 显示名与实际邮箱地址分别校验；
- Unicode / SMTPUTF8 场景保持规范化策略一致；
- 重置、邀请和验证链接由可信 origin 生成；
- 邮件模板变量按正文格式正确编码；
- 多租户系统避免租户 A 控制租户 B 的 sender identity、reply-to 或品牌模板。

## 判断原则

单纯能在主题或显示名中输入特殊字符并不等于协议级注入。应确认最终邮件结构是否真的出现额外字段、错误收件人或错误的安全链接语义。

## 联动专题

- 账号恢复：`authbypass-test.md`
- Host/URL 生成：`http-host-header-test.md`
- OAuth/OIDC 邮件链：`oauth-jwt-test.md`
