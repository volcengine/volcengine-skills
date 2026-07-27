# 安全风控与合规限制

用于账号风控、业务风险识别、云信任中心、可信隐私计算、多云安全平台、攻击面管理等问题。

## 前置输入

- 产品名和错误码。
- 账号状态、风控/风险 ID、设备 ID、任务 ID。
- 资源 ID、发生时间、RequestId。

## 查询入口

多云安全平台：

```text
ve mcs GetOverviewCard
ve mcs GetApiV1OverviewSecurityScores
ve mcs GetRisk
ve mcs GetRiskStat
```

可信隐私计算：

```text
ve tis GetQuotaInfo
ve tis GetPoolDetailList
ve tis GetAgentList
```

高级网络威胁检测：

```text
ve nta GetFileDetection
```

## Agent 使用方式

- 如果错误指向账号风险状态、实名认证、冻结或风控限制：保留安全产品上下文后转账号权限 skill。
- 如果错误指向配额或购买资格：转计费 skill。
- 如果只是产品控制台/任务状态查询：使用本 ref 的只读命令。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 风控/账号状态异常 | 不是 KMS 参数问题，转账号权限/工单 |
| 安全评分或风险任务异常 | 多云安全风险治理问题 |
| 配额不足 | 转计费/配额 |
| 文件检测任务异常 | 高级网络威胁检测产品问题 |

## 变更边界

不要自动提交风控解除、策略变更、风险处置动作。
