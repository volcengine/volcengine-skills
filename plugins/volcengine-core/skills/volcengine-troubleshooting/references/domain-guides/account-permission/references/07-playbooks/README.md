# 权限问题 Playbook

## AccessDenied 通用卡片

1. `ve sts GetCallerIdentity`
2. 抽取 Action / Resource / Project。
3. IAM 用户场景查用户策略和组策略。
4. Role 场景查角色存在性、信任关系、角色策略。
5. 产品 Action 场景回到对应产品 skill 判断资源模型。

## IAM 无权限诊断卡片

1. 识别用户、服务、Action。
2. 判断是 IAM 自身管理权限，还是某产品 Action。
3. 用最小授权原则补 Action + Resource + Project，不要给整产品全权限。

## RoleNotExist 卡片

1. `ve iam GetRole --RoleName <role-name>`
2. 若确实不存在，区分自定义角色与服务角色。
3. 服务角色通常回产品控制台重新授权，不要手工猜角色策略。

## 账号风控卡片

1. 保留完整错误文本和 logid。
2. 不把风控错误误判成 IAM 策略缺失。
3. 升级账号侧工单。
