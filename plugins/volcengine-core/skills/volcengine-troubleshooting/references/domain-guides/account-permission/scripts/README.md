# 账号与权限排障脚本

当前首版先以 CLI 为主，暂不提供可执行脚本。

后续优先补：

| 脚本 | 目的 |
|---|---|
| `collect_iam_user_context.py` | 聚合用户、组、直绑策略、组策略、项目授权 |
| `collect_role_context.py` | 聚合角色、信任策略、角色策略和 caller identity |

脚本必须只读，并优先读取：

- `VOLCENGINE_ACCESS_KEY`
- `VOLCENGINE_SECRET_KEY`
- `VOLCENGINE_SESSION_TOKEN`
