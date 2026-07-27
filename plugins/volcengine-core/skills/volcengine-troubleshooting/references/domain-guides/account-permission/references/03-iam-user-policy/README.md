# IAM 子账号与策略权限

用于处理子用户无权限、策略不生效、`IAM无权限诊断`。

## 前置输入

- `UserName`、失败 Action、Service、Resource、Project、Region。
- 是否通过用户组授权。

## 命令包

### 1. 用户与直绑策略

```text
ve iam GetUser --UserName <user-name>
ve iam ListAttachedUserPolicies --UserName <user-name>
```

### 2. 用户组链路

```text
ve iam ListGroupsForUser --UserName <user-name>
ve iam GetGroup --GroupName <group-name>
ve iam ListAttachedUserGroupPolicies --GroupName <group-name>
```

### 3. 项目授权

```text
ve iam20210801 ListProjects
ve iam20210801 ListProjectIdentities --ProjectName <project-name>
ve iam20210801 ListProjectResources --ProjectName <project-name>
```

## 关注字段

- 是否存在用户。
- 用户 `Status` 是否为 `active`。
- 策略是直绑还是通过组继承。
- 策略覆盖的 Action / Resource / Project 是否与失败请求一致。

真实验证提示：当前样本主体可用以下链路成功查询：

```text
ve iam GetUser --UserName <user-name>
ve iam ListAttachedUserPolicies --UserName <user-name>
ve iam ListGroupsForUser --UserName <user-name>
```

`ListGroupsForUser` 返回空数组不代表用户没有权限，仍需查看直绑策略。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 用户存在但没有相关策略 | 缺少授权 |
| 用户直绑没有、组里有 | 继续核对组策略范围，不能只看直绑 |
| 有 Action 但 Resource / Project 不匹配 | 不是“没策略”，而是授权范围不够 |

## 典型 case

```text
IAM无权限诊断: 用户 USER_NAME 服务 访问控制（iam） 操作 ListUsers
```

```text
User is not authorized to perform: CDN:ListPagesProject on resource
```
