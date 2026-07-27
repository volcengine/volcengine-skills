# 账号与实名认证状态

用于处理实名认证异常、风控拦截、账号状态不同步。

## 前置输入

- 原始错误文本、logid、账号主体、产品名、发生时间。
- 用户是否已完成实名认证、服务是否已开通。

## 典型 case

```text
Your verification status is abnormal, we can not provide you with service base on risk system decision.
```

```text
account status abnormal: unsynchronized
```

## 判断方式

- 这类问题优先依赖错误文本、账号主体和产品开通状态。
- 当前公共 CLI / SDK 中没有足够稳定的“账号认证状态查询”能力，不要假装能自动查到风控判定。
- 如果产品已经开通但账号状态不同步，保留产品上下文并升级工单。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 风控明确拒绝 | 需要账号侧处理或工单，不是 IAM 策略缺失 |
| 实名已通过但产品仍报状态未同步 | 可能是状态同步链路问题，需产品 + 账号联合处理 |

## 变更边界

本 ref 不执行账号信息修改、认证提交或风控申诉动作。
