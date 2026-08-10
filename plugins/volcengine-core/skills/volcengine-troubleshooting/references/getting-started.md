# Getting Started

本地排障先确认工具链、凭证来源和场景归属，再进入具体产品域诊断。所有检查都应避免输出凭证值；需要修复时先给出证据、影响和最小变更建议，再等待用户确认。

## 本地依赖

必需：

- `VOLCENGINE_ACCESS_KEY`
- `VOLCENGINE_SECRET_KEY`
- `VOLCENGINE_REGION`

可选：

- `VOLCENGINE_SESSION_TOKEN`：仅 STS 临时凭证需要。

不要要求用户运行 `ve configure` 或把凭证写入文件。若用户只提供了旧变量名或项目私有变量名，应提示其映射到上述标准变量。

支持的本地命令：

- `ve`：火山引擎 CLI，优先用于 OpenAPI 只读查询。
- `tosutil`：TOS bucket、object、ACL、policy 和连通性排查。默认只允许 `ls`、`stat`、`du` 等读取动作，不下载大对象。
- `python3`：运行轻量只读聚合脚本和 SDK import 检查。

推荐先执行。`${SKILL_ROOT}` 是包含本 skill `SKILL.md` 的绝对目录：

```bash
bash "${SKILL_ROOT}/scripts/common_check.sh"
```

支持的 Python SDK：

- `volc-sdk-python`
- `volcengine-python-sdk`

除 `ve`、`tosutil` 和上述 Python SDK 外，不要建议或执行其他本地 CLI / SDK。用户已经提供的外部命令输出可以作为参考材料，但本 skill 不主动调用这些工具。

## Python SDK 检查

仅检查是否安装，不自动安装：

```bash
python3 -c "import volcenginesdkcore; print('volcengine-python-sdk available')"
```

如果缺失，向用户说明哪些高级排障会受影响，再询问是否允许安装。不要在未确认时执行 `pip install`。

## 场景路由

如果用户报错中缺少 `RequestId`、`ErrorCode`、`Action`、`Service`、`Region`、资源 ID、发生时间或调用方式，先问最少必要问题。问题边界不清楚时，先用下面的索引选择领域。

### 账号与权限

适用：登录身份异常、AK/SK 不可用、STS 过期、IAM 权限不足、跨账号角色、策略未生效。

只读命令：

```text
ve sts GetCallerIdentity
ve iam GetAccountSummary
ve iam GetUser --user-name USER_NAME
ve iam ListAccessKeys --user-name USER_NAME
ve iam GetAccessKeyLastUsed --AccessKeyId ACCESS_KEY_ID
ve iam ListAttachedUserPolicies --user-name USER_NAME
ve iam ListGroupsForUser --user-name USER_NAME
ve iam ListRoles
ve iam GetRole --role-name ROLE_NAME
ve iam ListAttachedRolePolicies --role-name ROLE_NAME
```

判据：先确认当前主体，再检查 AK 状态、最近使用记录、用户/组/角色策略和报错 Action 是否匹配。不要自动授予 `AdministratorAccess`。

### 计费与配额

适用：欠费、余额不足、代金券未抵扣、资源包用量、订单异常、实例创建失败但像是额度问题、服务配额不足。

只读命令：

```text
ve billing QueryBalanceAcct
ve billing ListCoupons
ve billing ListBill
ve billing ListResourcePackages
ve billing ListPackageUsageDetails
ve billing ListOrders
ve billing GetOrder --OrderNo ORDER_NO
ve quota ListProducts
ve quota ListProductQuotas --ProviderCode PROVIDER_CODE
```

判据：区分账户余额、冻结金额、代金券适用范围、资源包抵扣范围、按量后付费欠费和产品配额。输出账单时只给摘要。

### 计算、容器与网络

适用：ECS 创建/启动/登录失败、实例状态异常、VKE Pod 异常、CLB/ALB 后端不健康、VPC 网络不通、NAT/EIP/路由/安全组问题。

只读命令：

```text
ve ecs DescribeInstances --InstanceIds '["INSTANCE_ID"]'
ve ecs DescribeInstanceStatus --InstanceIds '["INSTANCE_ID"]'
ve ecs DescribeSystemEvents --InstanceId INSTANCE_ID
ve ecs GetConsoleOutput --InstanceId INSTANCE_ID
ve vpc DescribeVpcs
ve vpc DescribeSubnets --VpcId VPC_ID
ve vpc DescribeRouteTables --VpcId VPC_ID
ve vpc DescribeSecurityGroups --VpcId VPC_ID
ve clb DescribeLoadBalancers
ve clb DescribeListeners --LoadBalancerId LOAD_BALANCER_ID
ve clb DescribeHealthCheckLog --LoadBalancerId LOAD_BALANCER_ID
ve alb DescribeLoadBalancers
ve vke ListClusters
ve vke ListNodePools --ClusterId CLUSTER_ID
```

判据：按“资源存在与地域 -> 运行状态 -> 控制面事件 -> 网络路径 -> 安全组/ACL -> 后端健康”的顺序定位。VKE 排障只采集 VolcEngine 控制面证据；Pod 日志、事件和应用侧现象由用户提供，不主动调用集群侧工具。

### 存储与数据库

适用：TOS 访问失败、对象不存在、ACL/Policy 拒绝、EBS 挂载异常、EFS/CFS 挂载失败、RDS/Redis 连接失败、备份异常。

只读命令：

```text
tosutil ls tos://BUCKET
tosutil stat tos://BUCKET/OBJECT_KEY
ve ebs DescribeVolumes
ve efs DescribeFileSystems
ve efs DescribeMountTargets --FileSystemId FILE_SYSTEM_ID
ve rdsmysqlv2 DescribeDBInstances
ve rdsmysqlv2 DescribeDBInstanceDetail --InstanceId INSTANCE_ID
ve redis DescribeDBInstances
ve redis DescribeDBInstanceDetail --InstanceId INSTANCE_ID
ve cbr DescribeVaults
```

判据：先确认地域、实例状态、网络白名单/安全组、存储挂载目标和访问身份。不要默认下载对象、导出数据库或读取 Secret。

### 域名、CDN 与安全边界

适用：CDN 回源失败、缓存未命中、证书异常、域名解析问题、Ingress 到 CLB/ALB 链路、WAF/DDoS/CFW 拦截。

只读命令：

```text
ve cdn DescribeCdnData
ve cdn DescribeCdnAccessLog
ve dns DescribeZones
ve dns DescribeRecords --ZID ZONE_ID
ve certificateservice ListCertificates
ve clb DescribeLoadBalancers
ve alb DescribeLoadBalancers
ve waf ListInstances
ve ddosbgp DescribeInstances
ve cfw DescribeVpcFirewallAclRules
```

判据：区分 DNS 解析、证书、边缘缓存、回源、负载均衡、后端健康和安全策略拦截。不要默认刷新/预热 CDN、修改 DNS 记录或变更证书。

### 通信与媒体

适用：短信发送失败、模板/签名审核、RTC 房间或音视频质量、VOD/Live 处理失败、CV/OCR API 调用失败。

只读命令：

```text
ve sms DescribeSmsAccount
ve sms QuerySendDetails
ve vod GetMediaInfos
ve vod GetWorkflowExecution
ve live DescribeLiveStreamState
ve rtc GetRecordTask
```

判据：先确认账号/应用/模板/签名/区域，再查请求时间窗口、回执、工作流状态和错误码。不要发送测试短信或触发媒体处理任务，除非用户确认。若当前 CLI 无对应 service/action，不要编造命令，转官方文档、SDK 或领域手册确认。

### AI 与大模型生态

适用：Ark 模型调用失败、API Key 权限、限流、向量库检索异常、AgentKit/Coze 工作流失败、机器学习平台任务异常。

只读命令：

```text
ve ark ListEndpoints
ve ark GetEndpoint --EndpointId ENDPOINT_ID
ve vikingdb ListCollections
ve mlplatform ListJobs
ve llmscan ListScanTasks
```

判据：关注模型/endpoint 状态、地域、配额、并发限制、向量索引状态、请求体字段和插件/工作流权限。不要输出 API Key 明文。

### 安全、KMS 与加密

适用：KMS 加解密失败、密钥状态异常、Secret 访问失败、证书或安全策略导致业务失败。

只读命令：

```text
ve kms DescribeKeys
ve kms DescribeKey --KeyringName KEYRING_NAME --KeyName KEY_NAME
ve kms ListKeyVersions --KeyringName KEYRING_NAME --KeyName KEY_NAME
ve seccenter DescribeAlarmEventList
ve waf ListInstances
ve cfw DescribeVpcFirewallAclRules
```

判据：检查密钥状态、版本、授权主体、Region、别名和策略。不要默认执行 `Decrypt`、`GetSecretValue`、密钥轮转、禁用/删除密钥等动作。

## 安全输出

- SecretKey 和 SessionToken 永不输出。
- AccessKeyId 仅可显示前后少量字符，例如 `AKLT****abcd`。
- 账号 ID、角色名、用户名、资源 ID 可在必要时输出，但避免批量暴露无关资源。
- 账单、短信、对象、日志和数据库查询结果只展示与排障有关的摘要。
