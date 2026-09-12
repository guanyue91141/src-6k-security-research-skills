---
status: current
last_reviewed: 2026-09
sources:
  - murrtada/bug-bounty-agent-skills:hunt-k8s
---

# Kubernetes / Container 安全审查 2026

> 面向授权比赛、CTF、SRC 与白盒审计。默认采用权限枚举、配置审查与只读证据，不把“端口开放”或“接口 200”直接写成集群接管。

## 1. 核心边界

Kubernetes 要分清五层：

1. API Server 身份与 RBAC；
2. Kubelet / Node 权限；
3. Pod ServiceAccount 与 workload identity；
4. etcd / Secret / ConfigMap 数据面；
5. 容器运行时与宿主机边界。

比赛里最常见的误判，是把“能访问某接口”直接等价为“cluster-admin”。

## 2. 识别信号

- `kubernetes.default.svc`、ServiceAccount 路径、`KUBERNETES_*` 环境变量；
- 6443、10250、2379 等服务只作为线索；
- Helm、Argo、Dashboard、Ingress、service mesh；
- 容器内 `/var/run/secrets/kubernetes.io/serviceaccount/`；
- 镜像、Pod 名、namespace、nodeName、cluster domain。

## 3. API Server / RBAC

审查重点：

- 当前主体是谁；
- 能对哪些 resource / subresource 执行哪些 verb；
- namespace 权限与 cluster 权限是否混淆；
- `impersonate`、`bind`、`escalate`、`create pods`、`pods/exec`、`nodes/proxy` 等高影响权限；
- wildcard resource/verb 是否过宽；
- service account 是否被误绑高权限 ClusterRole。

优先使用授权 API / SelfSubject* 类能力确定**实际授权**，不要根据列表为空/不为空猜测权限。

## 4. ServiceAccount / Workload Identity

现代集群大量使用 projected/bound token，审查：

- `aud` 是否只面向预期服务；
- `exp` 是否短时并轮换；
- token 是否绑定 Pod/Node；
- 是否仍使用长期 legacy token；
- 云 workload identity 是否把 K8s SA 映射成过宽云角色；
- 应用是否把 SA token 暴露给不需要访问 API 的工作负载。

发现 token 后必须先确认其真实权限，不根据文件存在就宣称集群接管。

## 5. Kubelet / Node

区分：

- 只读信息面；
- 需要认证的管理面；
- API Server 代理到 node 的 subresource；
- 调试/exec 能力。

验证原则：

- 优先权限检查；
- 如比赛规则允许验证执行，只做无副作用标记或测试 Pod；
- 不在真实生产 Pod 里执行破坏性命令。

## 6. etcd / Secrets

重点不是“2379 开放”，而是：

- 是否真正允许未认证/错误认证读取 keyspace；
- Secret 是否启用 encryption at rest；
- backup/snapshot 是否暴露；
- 读出的 credential 是否仍有效；
- etcd 网络是否只对 control-plane 可达。

## 7. Pod Security / Container Boundary

白盒/配置审查：

- privileged；
- hostPID/hostNetwork/hostIPC；
- hostPath；
- dangerous Linux capabilities；
- writable runtime socket；
- seccomp/AppArmor/SELinux；
- root user 与 readOnlyRootFilesystem；
- ephemeral/debug container 权限；
- imagePullPolicy、镜像 provenance。

## 8. Admission 与 Policy

检查：

- Pod Security Admission / Kyverno / Gatekeeper 是否只在部分 namespace 生效；
- exception/namespace label 是否形成策略空洞；
- mutation webhook 是否引入额外凭据或 sidecar 权限；
- webhook fail-open / fail-close 行为；
- CRD/controller 是否把用户输入转成高权限资源。

## 9. Ingress / Service Mesh

结合 API 网关专题：

- 外部 ingress 与内部 service 是否授权一致；
- Envoy/Istio identity metadata 是否可信；
- mTLS 是否只在部分 namespace/port 生效；
- sidecar bypass、direct pod IP、NodePort 是否形成第二入口；
- gRPC/HTTP 转换是否绕开原有 policy。

## 10. Evidence Gate

以下是 Signal，不直接算高危：

- `/version` 可读；
- namespace 列表可达；
- 10255/metrics 暴露；
- Pod 名、Node 名泄露；
- SA token 文件存在。

升级 Finding 需要证明**额外能力**：越权读取敏感资源、越权创建/执行、跨 namespace/cluster 边界、获得高权限云身份等。

## 11. 联动

- 云元数据 / workload identity → `ssrf-test.md`
- CI/CD / 镜像供应链 → `cicd-security-review-2026.md`
- gRPC/service mesh → `grpc-security-2026.md`
- API 授权 → `api-security-review.md`
- 信息泄露/Secret → `info-leak-test.md`
