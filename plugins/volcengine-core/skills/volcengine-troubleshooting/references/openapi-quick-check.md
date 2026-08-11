# OpenAPI Quick Check

本手册用于快速检查 VolcEngine OpenAPI 报错问题，包括签名鉴权、权限不足、参数校验、资源状态、限流、服务端错误，以及由 `ve`、`tosutil`、`volc-sdk-python`、`volcengine-python-sdk` 暴露出的 OpenAPI 调用失败。默认只做只读诊断；产品运行态问题仍应回到 `references/getting-started.md` 的场景路由和 `references/domain-guides/`。

## 第一阶段：上下文获取

在判断原因前，先收集最小上下文：

- `RequestId`、`ErrorCode`、HTTP 状态码和完整错误摘要。
- `Service`、`Action`、`Version`、`Region`、调用时间窗口和调用方式。
- 关键请求参数的结构、资源 ID、分页参数和过滤条件。不要要求用户提供 SecretKey 或 SessionToken。
- 当前本地工具版本：`ve --version`、`tosutil version`、受支持 Python SDK 版本。

可用的只读检查：

```text
ve sts GetCallerIdentity
ve SERVICE --help
ve SERVICE ACTION --help
ve cloudtrail LookupEvents --lookup-attributes AttributeKey=EventName,AttributeValue=ACTION --max-results 10
```

如果用户没有提供 `RequestId`，不要凭空猜测。先用 Action 和时间窗口查 CloudTrail；仍无法定位时，询问缺失的 Action、Region、资源 ID 和发生时间。

## 错误分类

### 凭证与签名

常见错误：`AuthFailure`、`SignatureDoesNotMatch`、`InvalidAccessKeyId.NotFound`、`InvalidSecurityToken`、`RequestExpired`。

检查顺序：

1. 确认本地环境变量存在：`VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，临时凭证还需要 `VOLCENGINE_SESSION_TOKEN`。
2. 运行 `ve sts GetCallerIdentity`，只报告认证是否成功和必要身份摘要。
3. 如果怀疑 AK 状态，且用户已确认可查询对应用户，再使用 IAM 只读接口查询：

   ```text
   ve iam ListAccessKeys --user-name USER_NAME
   ve iam GetAccessKeyLastUsed --AccessKeyId ACCESS_KEY_ID
   ```

4. 对 Python SDK 或手写 HTTP 请求，重点检查签名区域、服务名、时间偏移、CanonicalQueryString 编码、Header 参与签名范围和 Body 哈希。

不要运行 `ve configure` 修复凭证；应让用户用环境变量或其本地密钥管理方式更新凭证。

### 权限不足

常见错误：`AccessDenied`、`Forbidden`、`UnauthorizedOperation`、`NoPermission`。

检查顺序：

1. 通过 `ve sts GetCallerIdentity` 确认当前调用主体是账号、用户还是角色。
2. 根据主体类型执行只读 IAM 查询：

   ```text
   ve iam ListAttachedUserPolicies --user-name USER_NAME
   ve iam ListGroupsForUser --user-name USER_NAME
   ve iam ListAttachedRolePolicies --role-name ROLE_NAME
   ve iam ListPolicies --scope Local
   ```

3. 对比报错 Action、资源 ARN、Condition、Region 和账号边界。
4. 如果需要修复权限，只给出最小权限建议和影响说明。不要自动执行 `AttachUserPolicy`、`PutUserPolicy`、`CreatePolicy` 等写操作。

### 参数与资源状态

常见错误：`InvalidParameter`、`MissingParameter`、`InvalidParameterValue`、`ResourceNotFound`、`InvalidResourceState`。

检查顺序：

1. 用 `ve SERVICE ACTION --help` 对齐必填参数、枚举值和地域支持。
2. 用 Describe/List/Get 查询资源是否存在、地域是否正确、状态是否允许当前操作。
3. 注意分页、过滤器字段名、大小写、时间格式、ID 前缀和跨地域资源关系。
4. Python SDK 调用失败时，打印结构化请求参数但隐藏凭证和敏感业务字段。

### 限流与服务端错误

常见错误：`Throttling`、`RequestLimitExceeded`、`TooManyRequests`、`InternalError`、`ServiceUnavailable`。

处理原则：

- 先判断是否是单接口、单地域、单账号或全局异常。
- 查 CloudTrail 或服务监控确认请求频率和失败时间。
- 建议指数退避、抖动、分页限速和幂等重试；不要建议无脑并发重试。
- 如果错误稳定复现且参数正确，整理 `RequestId`、时间、Action、Region 和最小复现参数，建议用户提交工单。

### CLI 与 Python SDK

- CLI：只支持 `ve` 和 `tosutil`。确认版本、环境变量、`ve SERVICE ACTION --help` 或 `tosutil help`，不要依赖交互式配置。
- Python SDK：只支持 `volc-sdk-python` 和 `volcengine-python-sdk`。确认 SDK 可导入，并记录包版本、Region/Endpoint、异常对象和 ResponseMetadata。
- API 网关/HTTP：检查 Host、Path、Query、签名版本、Content-Type、X-Date、Region 和 Service；只分析用户提供的脱敏请求信息，不主动调用其他本地命令。
