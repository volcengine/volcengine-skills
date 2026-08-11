# 高频 Playbook

## SignatureDoesNotMatch

1. `ve sts GetCallerIdentity`
2. 核对 Host、Service、Region、Endpoint。
3. 核对时间戳、SignedHeaders、Body hash、Query 编码。
4. STS 场景确认 SessionToken 已传入。
5. 如果 CLI 成功而手写 HTTP 请求失败，优先认为手写签名过程有误。

## InvalidAction / InvalidActionOrVersion

1. 抽取 Action、Version、Service。
2. `ve <service> <Action> --help`
3. 如果 unsupported，检查 CLI 版本、ServiceName、API 文档版本。
4. 如果 Action 属于具体产品，转产品 skill 做业务解释。

## InvalidParameter / MissingParameter

1. `ve <service> <Action> --help`
2. 判断展开参数还是 `--body` JSON。
3. 检查参数大小写、数组/对象类型、时间格式、枚举值。
4. 如果参数合法但产品状态不允许，转产品 skill。

## SDK 初始化失败

1. 确认 SDK 来源：`volcengine-python-sdk` 或 `volc-sdk-python`。
2. 确认 Region、Endpoint、AK/SK/SessionToken 注入方式。
3. 用 CLI 同 Action 最小调用对照。
4. 提取异常对象里的 ResponseMetadata。

## CLI/API Explorer 复现失败

1. `ve version`
2. `ve <service> <Action> --help`
3. 对复杂参数使用 `--body`。
4. 手写 HTTP 场景只比较脱敏字段，不输出 Authorization 或 Signature。

## API Gateway 鉴权/路由失败

1. `ve apig ListGateways --body '{"PageNumber":1,"PageSize":10}'`
2. `ve apig GetGateway --body '{"Id":"<gateway-id>"}'`
3. 查 Service、Upstream、CustomDomain、PluginBinding。
4. `ve apig20221112 ListRoutes --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'`
5. 后端网络、域名、证书或 WAF 转产品 skill。
