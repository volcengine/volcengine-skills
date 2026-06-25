# Volcengine Supabase Tool Reference

## CLI Coverage

Current `ve aidap` coverage includes:

- Workspace: `DescribeWorkspaces`, `DescribeWorkspaceDetail`, `DescribeWorkspaceOverview`, `CreateWorkspace`, `DeleteWorkspace`, `StartWorkspace`, `StopWorkspace`, `ModifyWorkspaceSettings`, `ModifyWorkspaceName`
- Branch: `DescribeDefaultBranch`, `DescribeBranches`, `CreateBranch`, `DeleteBranch`, `ResetBranch`, `RestartBranch`, `SetAsDefaultBranch`, `UpdateBranch`
- Database and account: `DescribeDatabases`, `CreateDatabase`, `DropDatabase`, `DescribeDBAccounts`, `CreateDBAccount`, `DeleteDBAccount`, `ResetDBAccountPassword`, `DescribeDBAccountConnection`
- Endpoint and key: `DescribeWorkspaceEndpoint`, `DescribeAPIKeys`, `DescribeSupabaseDeployEnvVars`, `CreateEndpointPublicAddress`, `DeleteEndpointPublicAddress`, `CreateAccessControlList`, `ModifyAccessControlList`
- Schema diff: `CreateSchemaDiff`, `DescribeSchemaDiffJobStatus`, `DescribeSchemaDiffResultSQLText`, `DescribeSchemaDiffResultSQLTextAll`

Run `ve aidap <Action> --help` before composing a command because parameter names and body shapes are authoritative there.

Some AIDAP list/read actions use a JSON body instead of flat CLI flags. For example, current `DescribeWorkspaces` help exposes `--body`:

```bash
ve aidap DescribeWorkspaces --body '{"Limit":20,"Offset":0}'
```

Branch-scoped operations require an explicit `BranchId`. This includes `DescribeWorkspaceEndpoint`, `DescribeAPIKeys`, `DescribeSupabaseDeployEnvVars`, `DescribeDBAccounts`, `DescribeDatabases`, `CreateDBAccount`, `CreateDatabase`, `DescribeDBAccountConnection`, and related endpoint/account/database actions. A real `DescribeWorkspaceEndpoint` call without `BranchId` returned `InvalidParameter`, so do not omit it even when the workspace has a default branch.

For PostgreSQL workspaces, endpoint and account-connection reads are also compute-scoped. Resolve the primary database compute first:

```bash
ve aidap DescribeWorkspaceDetail --WorkspaceId ws-xxxx
ve aidap DescribeDefaultBranch --WorkspaceId ws-xxxx
ve aidap DescribeComputes --WorkspaceId ws-xxxx --BranchId br-xxxx
```

Use the `ComputeId` whose compute has `ComputeName=Primary`, `ComputeRole=Primary`, `ServiceType=Database`, and `ComputeStatus=Active`:

```bash
ve aidap DescribeWorkspaceEndpoint --WorkspaceId ws-xxxx --BranchId br-xxxx --ComputeId cp-xxxx
ve aidap DescribeDBAccountConnection --WorkspaceId ws-xxxx --BranchId br-xxxx --ComputeId cp-xxxx --DatabaseName postgres --AccountName user_admin
```

A verified PostgreSQL `DescribeWorkspaceEndpoint` call with only `BranchId` returned `InvalidParameter: 参数ComputeId值无效`; do not retry unrelated branch IDs for that symptom.

## PostgreSQL Workspace Bootstrap Notes

For `database_engine=postgresql`, prefer explicit networking in `CreateWorkspace`: pass `NetworkSettings.VpcId` and `NetworkSettings.SubnetId`, reusing an existing `Available` default VPC/subnet when appropriate. Do not begin with shared public/shared-network-only creation as the default path.

After creation, wait in this order:

1. `DescribeWorkspaceDetail` until `WorkspaceStatus=Running`.
2. `DescribeDefaultBranch` until `BranchStatus=Ready`.
3. `DescribeComputes` until the primary database compute is `Active`; save its `ComputeId`.

Only after those checks should you fetch endpoints or database-account connection strings.

## AIDAP Service-Linked Role

`CreateWorkspace` may fail even when `DescribeWorkspaces` succeeds if the AIDAP service-linked role is missing:

```text
RoleNotExist: Role 'trn:iam::<account-id>:role/ServiceRoleForAIDAP' does not exist
```

Repair the service-linked role through IAM only for the verified AIDAP service name:

```bash
ve iam GetServiceLinkedRoleTemplate --ServiceName aidap
ve iam CreateServiceLinkedRole --ServiceName aidap
ve iam GetRole --RoleName ServiceRoleForAIDAP
```

Expected role properties after repair:

```text
RoleName: ServiceRoleForAIDAP
IsServiceLinkedRole: 1
Trust principal: aidap
```

Retry `CreateWorkspace` once after the role exists. If the next failure is `NotVerifiedAccount` or `账号未实名认证`, the control-plane dependency is fixed and the remaining blocker is account real-name verification.

## Verified Control-Plane Failure Pattern

`CreateDBAccount` can return `PrimaryComputeNotFound` even when the default branch is ready. Before changing IDs, verify the same workspace and branch with:

```bash
ve aidap DescribeDefaultBranch --WorkspaceId ws-xxxx
ve aidap DescribeBranches --WorkspaceId ws-xxxx
ve aidap DescribeComputes --WorkspaceId ws-xxxx --BranchId br-xxxx
```

If `DescribeComputes` shows `ComputeName=Primary`, `ComputeRole=Primary`, `ServiceType=Database`, and `ComputeStatus=Active` for the target branch, record the case as a control-plane inconsistency. Use the `POSTGRES_URL` fallback described in `deploy-provider.md` instead of trying unrelated branch IDs.

## Connection Secret Handling

Do not print complete PostgreSQL passwords or credential-bearing connection strings. Store `DATABASE_URL` in a local env file with directory mode `700` and file mode `600`, then verify with a PostgreSQL client:

```bash
mkdir -p .aidap
chmod 700 .aidap
umask 077
printf 'DATABASE_URL=%q\n' "$DATABASE_URL" > .aidap/ws-xxxx-postgres.env
psql "$DATABASE_URL" -Atc "select 1"
```

For final answers, report only the host/port, database/user names, resource IDs, local file path, and verification outcome.

## ACL Verification

`CreateAccessControlList` exposes `--IPList array`, but common CLI array forms have returned `InvalidParameterFormat` in real PostgreSQL workspace testing. Do not assume the allowlist has been narrowed just because a create/modify command was attempted.

Always re-check the effective sources through `DescribeDBAccountConnection`:

```bash
ve aidap DescribeDBAccountConnection --WorkspaceId ws-xxxx --BranchId br-xxxx --ComputeId cp-xxxx --DatabaseName postgres --AccountName user_admin
```

Inspect `Result.AllowHost`. If it includes `0.0.0.0/0` or `::/0`, warn that public access is broad and recommend tightening it in the console or with a separately verified API invocation.

## Engine Model

AIDAP deploy-facing database engine choices are stable product-level choices:

- `database_engine=supabase`
- `database_engine=postgresql`

Current official `CreateWorkspace` API enum mapping from the Volcengine docs:

| Deploy choice | `EngineType` | `EngineVersion` | API description |
| --- | --- | --- | --- |
| `database_engine=postgresql` | `PostgreSQL` | `PostgreSQL_17` | PostgreSQL 17 |
| `database_engine=supabase` | `Supabase` | `Supabase_1_24` | Supabase 1.24 |
| Not a deploy default | `veDB_MySQL` | `veDB_MySQL_8_0` | veDB MySQL 8.0 |

Source: official `CreateWorkspace` docs, `https://www.volcengine.com/docs/87275/2105881?lang=zh`.

`EngineVersion` is required. `EngineType` supports `PostgreSQL`, `veDB_MySQL`, and `Supabase`; include it in generated bodies to avoid ambiguity even though the API marks it optional. For `EngineVersion=veDB_MySQL_8_0` or `EngineVersion=Supabase_1_24`, the official docs require `NetworkSettings`.

Before a live workspace creation, re-check the current `CreateWorkspace` documentation, console payload, or CLI/API evidence if this table may be stale. Keep enum values centralized here; do not repeat version labels throughout prepare/deploy selection docs.

## Data-Plane Coverage

Current `ve aidap` does not expose these old-skill capabilities for Supabase-compatible workspaces. Use `scripts/supabase_dataplane.py`:

- Database: `execute-sql`, `list-tables`, `list-migrations`, `list-extensions`, `apply-migration`, `generate-typescript-types`
- Edge Functions: `list-edge-functions`, `get-edge-function`, `deploy-edge-function`, `delete-edge-function`
- Storage: `list-storage-buckets`, `create-storage-bucket`, `delete-storage-bucket`, `get-storage-config`

The script keeps the old action names. It resolves workspace endpoint, default branch, and service-role key through `ve aidap`; the actual data-plane request is a Supabase REST request with:

```text
apikey: <service-role-key>
Authorization: Bearer <service-role-key>
```

It does not sign data-plane requests with Volcengine AK/SK.

Examples:

```bash
python3 scripts/supabase_dataplane.py execute-sql --workspace-id ws-xxxx --query "select 1"
python3 scripts/supabase_dataplane.py execute-sql --workspace-id ws-xxxx --query-file ./query.sql
python3 scripts/supabase_dataplane.py apply-migration --workspace-id ws-xxxx --name add_table --query-file ./migration.sql
python3 scripts/supabase_dataplane.py generate-typescript-types --workspace-id ws-xxxx --schemas public
python3 scripts/supabase_dataplane.py list-edge-functions --workspace-id ws-xxxx
python3 scripts/supabase_dataplane.py deploy-edge-function --workspace-id ws-xxxx --function-name hello --source-file ./index.ts
python3 scripts/supabase_dataplane.py list-storage-buckets --workspace-id ws-xxxx
python3 scripts/supabase_dataplane.py create-storage-bucket --workspace-id ws-xxxx --bucket-name uploads --public
```

Environment:

- `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` can be set to skip endpoint/key lookup.
- `DEFAULT_WORKSPACE_ID` is used when `--workspace-id` is omitted.
- `SUPABASE_WORKSPACE_SLUG` defaults to `default` for Edge Function routes.
- `SUPABASE_ENDPOINT_SCHEME` defaults to `http` to match the old skill's endpoint URL behavior.
- `READ_ONLY=true` blocks data-plane write actions.

## Real-Name Verification

Activate the `volcengine-cli` skill and use its `GetVerifyInfo` extension API capability for real-name verification checks. 

- Personal verification is `IsVerified=true` with `IdentityType="individual"`.
- Enterprise verification is `IsVerified=true` with `IdentityType="enterprise"`.

## Service Activation

When the account has not enabled AIDAP, ask the user to open:

```text
https://console.volcengine.com/aidap
```

After the console flow completes, rerun a read action such as:

```bash
ve aidap DescribeWorkspaces --body '{"Limit":1,"Offset":0}'
```

A successful response with `Total: 0` or an empty `Workspaces` list only means the account has no AIDAP workspaces. Do not treat an empty list as a service-disabled signal.

## Safety

- Treat `Create*`, `Modify*`, `Reset*`, `Start*`, `Stop*`, and `Delete*` as write operations. Show the exact command and wait for user confirmation unless the user already explicitly asked to perform that change.
- Treat `DeleteWorkspace`, `DeleteBranch`, `DropDatabase`, and password/key reset actions as destructive.
- Treat `apply-migration`, Edge Function deploy/delete, and Storage bucket create/delete as write or destructive data-plane operations.
- Do not expose complete API keys, service-role keys, account passwords, or credential-bearing database URLs in final output.
