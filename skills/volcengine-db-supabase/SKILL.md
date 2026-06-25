---
name: volcengine-db-supabase
description: >-
  Manage Volcengine AI Native BaaS for Supabase (AIDAP) database workspaces as a deployment database provider.
  Use when the user asks for Volcengine Supabase, AIDAP PostgreSQL, AIDAP database workspace setup, branch management,
  API keys, endpoint or database connection information, service activation, enterprise real-name
  verification, SQL execution, migrations, Edge Functions, Storage buckets, TypeScript type
  generation, or using AIDAP as the database for a Volcengine deployment. Prefer `ve aidap`
  for control-plane operations; use bundled scripts only for Supabase data-plane APIs missing from
  the current `ve` CLI.
license: MIT
---

# Volcengine AIDAP Database Skill

AIDAP refers to Volcengine's `AI 原生 BaaS 平台 Supabase 版` product. This skill manages its deployment-relevant database workspace capabilities and wires them into applications. The stable deploy-facing AIDAP engine choices are `supabase` and `postgresql`; resolve current `CreateWorkspace` `EngineType` / `EngineVersion` enums from [`references/tool-reference.md`](./references/tool-reference.md) before creating a workspace. The control plane should use `ve aidap` directly whenever the action exists. For old-skill data-plane capabilities not exposed by `ve`, use `scripts/supabase_dataplane.py` only for Supabase-compatible workspace APIs.

## Boundaries

- Supported by `ve aidap`: workspace, branch, compute, database, DB account, endpoint, API key, ACL, schema diff, start/stop, and deletion operations.
- AIDAP deploy engine choices are `supabase` and `postgresql`. Preserve the user's selected engine instead of treating Supabase as an RDS PostgreSQL provider.
- Real-name verification requires the `volcengine-cli` skill's `GetVerifyInfo` extension API capability; activate that skill first to use it.
- Not covered by current `ve` CLI: SQL execution, migration application, Supabase Edge Function management, Supabase Storage bucket management, and TypeScript type generation. Use `scripts/supabase_dataplane.py` for those old-skill capabilities.
- `scripts/supabase_dataplane.py` uses `ve aidap` only to resolve endpoint, default branch, and API keys. The data-plane calls use the Supabase service-role key in `apikey` and `Authorization` headers, not Volcengine AK/SK.
- Service activation is a console flow. If the service is not enabled, direct the user to `https://console.volcengine.com/aidap`.
- A successful `ve aidap DescribeWorkspaces --body '{"Limit":1,"Offset":0}'` response with `Total: 0` or `Workspaces: []` only means no workspaces exist; do not treat it as a service-disabled signal.
- AIDAP workspace creation requires the service-linked role `ServiceRoleForAIDAP`. If `CreateWorkspace` fails with `RoleNotExist`, follow the [Service-Linked Role Repair](#service-linked-role-repair) procedure.

## Initial Checks

1. Verify authentication with `ve sts GetCallerIdentity`.
2. Confirm AIDAP support in the installed CLI:

```bash
ve aidap --help
```

3. When creating a workspace or troubleshooting creation failure, activate the `volcengine-cli` skill and use its `GetVerifyInfo` extension API capability to check real-name verification. Personal verification is `IsVerified=true` with `IdentityType="individual"`; enterprise verification is `IsVerified=true` with `IdentityType="enterprise"`.

## Workspace Bootstrap

When the user has no workspace:

1. Ensure the AIDAP service is enabled. If not, ask the user to open:

```text
https://console.volcengine.com/aidap
```

2. Ensure the service-linked role `ServiceRoleForAIDAP` exists. If `CreateWorkspace` fails with `RoleNotExist`, follow the [Service-Linked Role Repair](#service-linked-role-repair) procedure below, then retry once.
3. Activate the `volcengine-cli` skill and use its `GetVerifyInfo` extension API capability to check enterprise verification.
4. Create the workspace with `ve aidap CreateWorkspace`, using the selected AIDAP engine and the current official enum mapping from [`references/tool-reference.md`](./references/tool-reference.md).

Minimal explicit-network body shape:

```bash
ve aidap CreateWorkspace --body '{
  "WorkspaceName": "demo-supabase",
  "EngineType": "<current EngineType for database_engine>",
  "EngineVersion": "<current EngineVersion for database_engine>",
  "BranchSettings": {
    "BranchName": "main",
    "DatabaseName": "postgres"
  },
  "ComputeSettings": {
    "AutoScalingLimitMinCU": 0.25,
    "AutoScalingLimitMaxCU": 1,
    "SuspendTimeoutSeconds": 300
  },
  "NetworkSettings": {
    "VpcId": "vpc-xxxx",
    "SubnetId": "subnet-xxxx",
    "SharedPublicNetwork": false
  },
  "WorkspaceSettings": {
    "DeletionProtection": "Disabled",
    "PublicConnection": "Disabled"
  },
  "WorkspaceTags": [
    {"Key": "publish-by", "Value": "deploy-skill"}
  ]
}'
```

Use a subnet in the same region as the workspace. For `database_engine=postgresql`, prefer an explicit `VpcId` and `SubnetId` from an existing `Available` VPC/subnet, such as the account's default VPC/subnet. Do not start with shared public/shared-network-only creation and then retry into explicit networking; the explicit network path is the verified low-friction path for PostgreSQL workspaces.

Do not invent or hard-code stale `EngineType` / `EngineVersion` values. Check the current API enum table in [`references/tool-reference.md`](./references/tool-reference.md), then refresh it from the official `CreateWorkspace` documentation or CLI/API evidence before live creation if the table may be stale.

After `CreateWorkspace`, verify readiness in dependency order:

1. Poll `DescribeWorkspaceDetail` until `WorkspaceStatus=Running`.
2. Poll `DescribeDefaultBranch` until the branch has `BranchStatus=Ready`; keep its `BranchId`.
3. Run `DescribeComputes` for that branch and keep the `Primary` database compute's `ComputeId` when `ComputeStatus=Active`.

For PostgreSQL workspaces, pass both `BranchId` and `ComputeId` to endpoint and database connection queries. A verified `DescribeWorkspaceEndpoint` call with only `BranchId` returned `InvalidParameter: 参数ComputeId值无效`.

## Common Commands

Use `ve aidap <Action> --help` before writing command arguments; AIDAP is evolving and the CLI help is the local source of truth.

```bash
ve aidap DescribeWorkspaces --body '{"Limit":20,"Offset":0}'
ve aidap DescribeWorkspaceDetail --WorkspaceId ws-xxxx
ve aidap DescribeDefaultBranch --WorkspaceId ws-xxxx
ve aidap DescribeBranches --WorkspaceId ws-xxxx
ve aidap DescribeComputes --WorkspaceId ws-xxxx --BranchId br-xxxx
ve aidap CreateBranch --WorkspaceId ws-xxxx --BranchSettings.Name dev
ve aidap DescribeWorkspaceEndpoint --WorkspaceId ws-xxxx --BranchId br-xxxx --ComputeId cp-xxxx
ve aidap DescribeAPIKeys --WorkspaceId ws-xxxx --BranchId br-xxxx
ve aidap DescribeDBAccounts --WorkspaceId ws-xxxx --BranchId br-xxxx
ve aidap CreateDBAccount --WorkspaceId ws-xxxx --BranchId br-xxxx --AccountName app --AccountPassword '<secret>'
ve aidap CreateDatabase --WorkspaceId ws-xxxx --BranchId br-xxxx --DatabaseName appdb --DatabaseOwner app
ve aidap DescribeDBAccountConnection --WorkspaceId ws-xxxx --BranchId br-xxxx --ComputeId cp-xxxx --DatabaseName appdb --AccountName app
ve aidap DescribeSupabaseDeployEnvVars --WorkspaceId ws-xxxx --BranchId br-xxxx
```

Branch-scoped actions must pass the explicit `BranchId`; do not rely on an implicit default branch for endpoint, API key, DB account, database, connection, or deploy-env-var operations. `DescribeWorkspaceEndpoint` without `BranchId` has been observed to fail with `InvalidParameter`. For PostgreSQL endpoint and account connection queries, also pass the resolved primary `ComputeId`.

If `CreateDBAccount` or `CreateDatabase` reports `PrimaryComputeNotFound`, first compare `DescribeDefaultBranch`, `DescribeBranches`, and `DescribeComputes` for the same workspace and branch. If the branch is the default branch and `DescribeComputes` shows a `Primary` database compute in `Active` state, stop guessing branch IDs and record the case as an AIDAP control-plane inconsistency. Use the PostgreSQL fallback in [`references/deploy-provider.md`](./references/deploy-provider.md) only when a credential-bearing admin `POSTGRES_URL` is available and the user accepts using it.

Never print passwords, API keys, JWT secrets, service-role keys, or connection strings containing credentials in final answers. Write `DATABASE_URL` into a local env file with mode `600`, then verify it with `psql` (`select 1` or a table-list query). Summarize the host/port, resource IDs, verification result, and credential file path, not the full connection string.

## Service-Linked Role Repair

If `ve aidap CreateWorkspace` fails with a message like:

```text
RoleNotExist: Role 'trn:iam::<account-id>:role/ServiceRoleForAIDAP' does not exist
```

do not immediately classify it as a service-disabled condition. Repair the missing AIDAP service-linked role through IAM:

```bash
ve iam GetServiceLinkedRoleTemplate --ServiceName aidap
ve iam CreateServiceLinkedRole --ServiceName aidap
ve iam GetRole --RoleName ServiceRoleForAIDAP
```

After `GetRole` confirms `RoleName=ServiceRoleForAIDAP` and `IsServiceLinkedRole=1`, retry `CreateWorkspace` once. If the retry returns `NotVerifiedAccount` or `账号未实名认证`, stop and ask the user to complete real-name verification at `https://console.volcengine.com/user/authentication/detail/`.

`CreateAccessControlList` currently has fragile CLI array parameter handling and has returned `InvalidParameterFormat` for common array forms. Do not tell the user that an ACL has been tightened until you verify the effective `AllowHost` from `DescribeDBAccountConnection`. If `AllowHost` still includes broad ranges such as `0.0.0.0/0` or `::/0`, warn clearly and recommend tightening in the console or with a separately verified API call.

## Data-Plane Commands

Use `scripts/supabase_dataplane.py` for old-skill capabilities that `ve aidap` does not expose. The script accepts either `--workspace-id ws-...` or `--workspace-id br-...`; when only a workspace is supplied it resolves the default branch with `ve aidap DescribeDefaultBranch`.

```bash
python3 scripts/supabase_dataplane.py execute-sql --workspace-id ws-xxxx --query "select * from pg_tables limit 5"
python3 scripts/supabase_dataplane.py apply-migration --workspace-id ws-xxxx --name create_todos --query-file ./migration.sql
python3 scripts/supabase_dataplane.py generate-typescript-types --workspace-id ws-xxxx --schemas public
python3 scripts/supabase_dataplane.py deploy-edge-function --workspace-id ws-xxxx --function-name hello --source-file ./index.ts
python3 scripts/supabase_dataplane.py create-storage-bucket --workspace-id ws-xxxx --bucket-name uploads --public
```

Set `READ_ONLY=true` to block data-plane write actions. If `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are already set, the script can skip `ve aidap` key lookup.

## Deploy Integration

When `volcengine-deploy` needs an AIDAP database, it passes `database_product=aidap` plus `database_engine=supabase|postgresql`. Read [`references/deploy-provider.md`](./references/deploy-provider.md) for the wiring loop and environment variables.

## References

- CLI action map and bootstrap notes: [`references/tool-reference.md`](./references/tool-reference.md)
- Application integration patterns: [`references/app-integration-guide.md`](./references/app-integration-guide.md)
- Schema and RLS guidance: [`references/schema-rls-guide.md`](./references/schema-rls-guide.md)
- SQL playbook: [`references/sql-playbook.md`](./references/sql-playbook.md)
- Edge Function development: [`references/edge-function-dev-guide.md`](./references/edge-function-dev-guide.md)
- Deployment database-provider wiring: [`references/deploy-provider.md`](./references/deploy-provider.md)
