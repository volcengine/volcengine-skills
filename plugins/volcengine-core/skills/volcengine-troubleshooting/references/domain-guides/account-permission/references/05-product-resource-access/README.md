# 产品资源访问权限

用于把 ECS、TOS、CDN、大模型等产品里的权限报错，翻译回 IAM / 项目 / 资源范围。

## 前置输入

- 产品、Action、Resource ID / TRN、Project、Region。
- 失败主体、是否跨账号、是否涉及关联资源。

## 命令包

```text
ve iam20210801 ListProjects
ve iam20210801 GetProject --ProjectName <project-name>
ve iam20210801 ListProjectResources --ProjectName <project-name>
```

产品自身资源状态和资源模型仍由对应产品 skill 查询。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| Action 已授权但资源不在项目内 | 项目范围不匹配 |
| 主资源有权，关联资源无权 | 需要补关联资源权限 |
| 跨账号资源 | 还要检查资源策略或信任关系 |

## 产品回跳

| 产品 | 回跳 skill |
|---|---|
| ECS / VPC / EIP | compute-container-network |
| TOS | storage-database |
| CDN / 域名 | domain-cdn-ingress |
| 大模型 | llm-ecosystem |
