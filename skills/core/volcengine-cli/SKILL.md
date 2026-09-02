---
name: volcengine-cli
description: >-
  Create and manage Volcengine cloud resources using the Volcengine CLI (`ve` command). Supports all
  Volcengine services including ECS, VPC, CLB, RDS, Redis, and more. Trigger this skill whenever the
  user asks to create, query, modify, or delete cloud resources on Volcengine, mentions the `ve` command,
  says "volcengine CLI", or describes infrastructure tasks such as "create an ECS instance",
  "set up a VPC", "list security groups", "allocate an EIP". Also trigger on Chinese prompts
  mentioning "火山引擎" or "火山" (e.g., "火山引擎上有哪些 ECS"、"查一下我火山的云服务器"、
  "火山引擎创建一个 VPC"、"火山的 Redis 实例列一下"). Also trigger when the user encounters
  errors from `ve` commands and needs troubleshooting help.
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - ve
    install:
      - kind: node
        package: "@volcengine/cli"
        bins: [ve]
    envVars:
      - name: VOLCENGINE_ACCESS_KEY
        required: false
        description: AccessKey for AK/SK auth path (alternative to `ve login`)
      - name: VOLCENGINE_SECRET_KEY
        required: false
        description: SecretKey for AK/SK auth path
      - name: VOLCENGINE_SESSION_TOKEN
        required: false
        description: Optional STS session token for temporary credentials
      - name: VOLCENGINE_REGION
        required: false
        description: Default region; falls back to cn-beijing if unset
      - name: VOLCENGINE_ENDPOINT
        required: false
        description: Optional fallback endpoint for `--force` calls and extension-helper calls that do not define a product endpoint
      - name: VOLCENGINE_PROFILE
        required: false
        description: Optional Volcengine CLI profile name used by extension helper credential fallback
      - name: VOLCSTACK_PROFILE
        required: false
        description: Legacy alias of VOLCENGINE_PROFILE honoured by the extension helper credential fallback
      - name: VOLCENGINE_CLI_CONFIG_FILE
        required: false
        description: Optional full path to the Volcengine CLI config file; defaults to ~/.volcengine/config.json when unset
      - name: VOLCENGINE_LOGIN_CACHE_DIRECTORY
        required: false
        description: Optional console-login cache directory used by extension helper credential fallback
      - name: VOLCENGINE_CLI_DOWNLOAD_BASE_URL
        required: false
        description: Base URL (or local mirror directory) that scripts/install_ve.sh downloads release archives from; defaults to https://cloudcache.volccdn.com/ve
      - name: VOLCENGINE_CLI_SKIP_SKILLS
        required: false
        description: Set to 1 to stop scripts/install_ve.sh from running `ve skills update` after installing
      - name: VE_VERSION
        required: false
        description: Pin the ve version scripts/install_ve.sh installs instead of reading the CDN latest file
      - name: VE_INSTALL_DIR
        required: false
        description: Directory scripts/install_ve.sh installs `ve` into; defaults to /usr/local/bin when writable, else ~/.local/bin
      - name: VE_LOGIN_URL_TIMEOUT
        required: false
        description: Seconds scripts/ve_login_remote.sh waits for `ve login` to print its URL (default 30)
---

# Volcengine CLI Skill

Create and manage Volcengine cloud resources by calling Volcengine OpenAPIs through the `ve` command.

---

## 0. Install or upgrade the ve CLI

Always run the latest release. This skill assumes the current `ve`: device-code `ve login`, `--output`/`--query`, `--force`, `--detail`, and double-dash system flags. There is no support path for older builds — upgrade instead.

**Option 1: npm (preferred)**

```bash
npm i -g @volcengine/cli
```

**Option 2: CDN installer (no Node.js, or npm unreachable)**

```bash
curl -fsSL https://cloudcache.volccdn.com/ve/install.sh | sh
# or
wget -qO- https://cloudcache.volccdn.com/ve/install.sh | sh
```

The same script ships as `scripts/install_ve.sh`. It reads the latest version from the CDN, downloads the archive for the host's OS/CPU, verifies it against the published `SHA256SUMS`, installs to `/usr/local/bin` when writable (else `~/.local/bin`, never `sudo`), removes the macOS quarantine flag, and runs `ve skills update`. `--version <ver>`, `--install-dir <dir>`, `--dry-run` and the `VE_VERSION` / `VE_INSTALL_DIR` / `VOLCENGINE_CLI_DOWNLOAD_BASE_URL` / `VOLCENGINE_CLI_SKIP_SKILLS` variables are documented in its header. Windows: use npm or the release page.

**Option 3: GitHub Releases** — https://github.com/volcengine/volcengine-cli/releases

**Capability check** (instead of comparing version numbers): `ve login --help` must list `--no-browser`, and `ve ecs DescribeInstances --help` must list `--output` under *System Flags*. If either is missing, upgrade with `npm i -g @volcengine/cli@latest` or rerun the CDN installer, then continue.

---

## 1. Initialization (run at the start of every session)

### CLI system flags

Every `ve <service> <Action>` call accepts these **after the Action**, all with two hyphens:

| Flag | Purpose |
| --- | --- |
| `--profile <name>` | Use a configured profile for this call only |
| `--region <region>` | Override the region for this call only |
| `--endpoint <host>` | Override the endpoint for this call only |
| `--lang EN\|ZH` | Display language for this call |
| `--version <YYYY-MM-DD>` | API version; metadata default when omitted (required with `--force`) |
| `--method GET\|POST` | HTTP method; metadata default, else GET |
| `--force` | Skip metadata validation (§3); presence-only, never `--force true` |
| `--output <fmt>` / `--query <jmespath>` | Response formatting and projection (§4) |
| `--header Name=Value`, `--body '{...}'` | Custom header / raw JSON body |

API parameters are PascalCase (`--Region`, `--InstanceIds.1`), system flags are lowercase (`--region`), so they do not normally collide. Only when an API parameter is spelled exactly like a system flag in lowercase (an API with its own `--query` or `--lang` field), write the **system** flag with three hyphens (`---query`) and leave the API parameter with two. Do not use three-hyphen flags anywhere else.

CLI management commands (`ve configure ...`, `ve login`, `ve sso login`) and the helper scripts take their own two-hyphen flags as shown by `--help`.

### Profile Selection (fixed for the conversation)

`ve` can use different credentials through profiles, but the agent must not choose a profile by itself.

- If the user did not explicitly select a profile, use the CLI default resolution: run `ve sts GetCallerIdentity` directly. Do not list all profiles first and choose one yourself.
- If the user explicitly selected a profile, keep using that same profile for all later commands in this conversation: `ve ecs DescribeInstances --profile prod`, `python3 scripts/call_extend_api.py --profile prod ...`.
- Do not infer the desired profile from profile name, region, list order, recent availability, success rate, or task content.
- If the default identity does not match the task risk, or a profile choice is required, tell the user the current default identity, list candidate profile names only, and wait for the user to choose.
- Once a profile is fixed for this conversation, do not switch to another profile unless the user explicitly asks to switch.

Run the identity verification command to confirm that credentials are usable:

```bash
ve sts GetCallerIdentity
```

**Success** — inform the user of the current account identity and region, then proceed with the task.

> **Switching regions later**: `--region` on a service API call **does** override the region for that single call (the response `Region` changes accordingly), and `VOLCENGINE_REGION` sets the default when the profile has none. What does **not** change is the profile's bound login session/account — a region override only redirects where the request goes, not who you are. Do not switch regions or profiles on your own initiative: only pass `--region` or switch profiles (`ve configure profile --profile <name>`) when the user explicitly asks. Use `ve configure list` only to show candidate profile names; after listing, do not choose a profile yourself. This is separate from the `--region` flag on `ve login` itself, which is required (see below).

**Failure** — no usable profile. Default plan: use `ve login` (Console Login). Announce this to the user up front, and tell them they can say "use AK/SK", "use STS token", or "use SSO" to switch.

The same plan applies when a previously working session expires **mid-task**: any `ve` command failing with `failed to refresh session token. Please run 've login' to re-authenticate` (or similar refresh-token/session-expired text) is this exact failure, no matter which skill issued the command. The error text tells the human to run `ve login` — do **not** relay that instruction to the user or ask them to run `ve login` in their own terminal; run the Console Login procedure below yourself and only hand the user the sign-in link. Re-login must target the profile that was in use: if a profile was fixed earlier in the conversation, pass it to `start` so both the login and its verification hit that profile — omitting it refreshes `default`, leaves the fixed profile broken, and pollutes the default account context.

### Default: Console Login via `scripts/ve_login_remote.sh`

**NEVER call `ve login` directly. ALWAYS use `scripts/ve_login_remote.sh`.** `ve login` is a device-code flow: ve prints a verification URL and user code, then polls until the user approves in a browser on any device. The device code lives only in that ve process, so the helper detaches it (`setsid`) to survive tool-call boundaries, records the URL/code, answers ve's prompts, and verifies the result. Calling `ve login` yourself orphans the process and kills the link.

**Before the first `start` of a conversation, read [references/console-login.md](references/console-login.md) completely** — it holds the step-by-step procedure, every exit code, the `start-wait` variant, tuning, and the full list of things that break the flow. The shape is:

```text
scripts/ve_login_remote.sh start <region> [profile]   # prints URL= CODE= LINK= EXPIRES_IN= NEXT=
scripts/ve_login_remote.sh url                        # same block, never blocks (11 = not yet, 3 = process gone)
# hand the user LINK (fallback: URL + CODE), end the turn, wait for "done"
scripts/ve_login_remote.sh verify [profile]           # 0 ok · 11 still pending · 13 logged in but API unreachable · 10 start over
scripts/ve_login_remote.sh abort                      # on user interrupt / expired code, then start again
```

Region: the one the user named, else `VOLCENGINE_REGION`, else `cn-beijing`. Pass `[profile]` only when the user fixed one earlier, and pass the same value to `start` and `verify`.

Invariants that must hold even without reading the reference:

- Announce the plan and the off-ramp ("say 'use AK/SK' to switch"), then start — do not present a menu of login methods.
- A hung or killed `start` proves nothing: call `url`/`status` before concluding anything; never retry `start`, `abort`, or switch to `nohup` because of it.
- Nothing is pasted back by the user; there is no authorization code. Run `verify` when they say they approved.
- `verify` exit 13 means the login **worked** and the host cannot reach `open.volcengineapi.com` — do not restart the login.
- Use `LINK` exactly as printed; never build `signin.volcengine.com` URLs or reuse one from an earlier process.
- `start` exit 4 = `ve` missing or too old for device-code login → install/upgrade (§0), then retry.

If `ve login` fails (network error, `start` exit 4, no browser on any device), or the user asks for another method, fall back to the alternatives below.

### Alternative: AK/SK (long-term credentials, for CI/CD or scripting)

Ask the user for AccessKey and SecretKey, then:

```text
ve configure set --profile default --region cn-beijing \
  --endpoint open.volcengineapi.com \
  --access-key <AK> --secret-key <SK>
```

For STS (temporary) credentials, also pass `--session-token <TOKEN>`.

Alternative for the current shell only: export `VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY`, `VOLCENGINE_REGION`, optionally `VOLCENGINE_SESSION_TOKEN`.

### Alternative: SSO / Cloud Identity Center (for enterprise federation)

Three-step setup; ask the user for the SSO start URL and session name first:

```text
ve configure sso-session --name <session-name> \
  --start-url https://<sso-host>/userportal \
  --region cn-beijing \
  --registration-scopes cloudidentity:account:access,offline_access

ve configure sso --profile <profile-name> --sso-session <session-name>

ve configure profile --profile <profile-name>
```

Then `ve sso login --sso-session <session-name>` (use `--no-browser` on headless machines).

### Credential safety

- **Never read `~/.volcengine/config.json`** — it contains AK/SK and session tokens.
- When running `ve configure set` with `--secret-key`, prefer letting the **user** paste and run the command in their own shell rather than executing it via Claude — secrets passed as command-line arguments end up in shell history and process listings.
- Never echo AK/SK, secret keys, or session tokens back to the user in plain text.

---

## 2. Safety Rules (mandatory)

### Read/Write Classification

| Level | Operation Types | Behavior |
|-------|----------------|----------|
| **Read-only** | Describe\* / List\* / Get\* / Query\* | Execute directly, no confirmation needed |
| **Write** | Create\* / Run\* / Allocate\* / Attach\* / Associate\* / Authorize\* | Show the full command and wait for user confirmation |
| **Destructive** | Delete\* / Terminate\* / Release\* / Revoke\* / Modify\* / Stop\* / Detach\* | Show command + impact summary; **require** user confirmation |

### Core Principles

1. **Default to read-only** — unless the user explicitly requests a change, execute in read-only mode
2. **DryRun first** — if a write/destructive operation supports `--DryRun true`, run a DryRun to preview the plan, then confirm before executing
3. **Confirm before executing** — show the full command for write operations and wait for approval
4. **Protect credentials** — never read `~/.volcengine/config.json`; never expose access-key, secret-key, or session-token in output

### DryRun Notes

A successful DryRun validation returns **exit code 1** (non-zero) with `DryRunOperation` in stderr. This is expected behavior:

```text
output=$(ve <svc> <action> --DryRun true ... 2>&1)
if echo "$output" | grep -q "DryRunOperation"; then
  echo "Parameter validation passed"
fi
```

---

## 3. Locate APIs and Retrieve Parameters

### Locate the API (find the service name + Action name)

```text
Step 1: Service name + Action known? -> Use them directly; skip to "Retrieve parameters"
Step 2: Service name known, Action unknown?
  -> ve <service> 2>&1 | grep -i <keyword>
Step 3: Service name also unknown?
  -> ve 2>&1 | grep -i <service keyword>
Step 4: None of the above work?
  -> python3 scripts/find_api.py <keyword>   (returns Service, Action, Version)
```

### Retrieve parameters (once the Action is known)

`--help` is concise (names, types, Required/Optional). `--help --detail` adds the full description, enum values, constraints and examples for every parameter — it is the CLI's own copy of the API documentation, so no external fetch is needed.

| Situation | Command |
|---|---|
| **Read-only** (Describe/List/Get) | `ve <svc> <Action> --help` — names alone are usually enough |
| **Write/destructive** (Create/Run/Delete…) | `ve <svc> <Action> --help --detail` — required fields, nested structures, examples |
| **Still unclear after `--help`** | `--help --detail`; add `--lang ZH` for the Chinese text |
| **Errors like `Invalid*` / `Missing*`** | Recheck names, required fields and ranges with `--help --detail` |

```text
ve ecs DescribeInstances --help
ve ecs RunInstances --help --detail
ve ecs RunInstances -h --detail --lang ZH
```

The `Parameter Form` / `--body` sections of the same output tell you whether the action takes flat parameters or a JSON body (§4).

For API questions that go beyond one action's parameters (comparisons, error-code semantics, pagination behaviour, whether a batch variant exists), load the `volcengine-api` skill, which queries the API Explorer directly.

### ve command name and API version relationship

- Default version -> ve command = base service name (e.g., `iam`)
- Non-default version -> ve command = `service name + version without hyphens` (e.g., `iam` v2021-08-01 -> `iam20210801`)
- When in doubt: `ve 2>&1 | grep <service>` to confirm

### Calling an API the CLI metadata does not list: `--force`

When `ve` answers `unknown service "<svc>"` or `unknown action`, but the API exists (the user provided it, `find_api.py` found its Service/Action/Version, or the docs describe it), call it with `--force`. `--force` skips the local metadata check, so **you** must supply what the metadata would have: the version, and — for a service the CLI does not know — the endpoint.

```bash
ve newservice DescribeNewResource \
  --version 2024-01-01 \
  --endpoint open.volcengineapi.com \
  --SomeParam value \
  --force
```

- `--version` is mandatory (`--version is required when using --force`); `--endpoint` is mandatory for an unknown service unless the profile or `VOLCENGINE_ENDPOINT` already sets one.
- `--method POST` for POST APIs (default GET); `--body '{...}'` for a JSON body (cannot be mixed with `--Param` values); `--region` when the service signs in a fixed region.
- `--force` is a presence flag: `--force`, not `--force true`.
- Parameters are unvalidated: take them from the user's material, the `volcengine-api` skill, or [references/extend-apis.md](references/extend-apis.md) — never guess them. `find_api.py` only locates Service/Action/Version; it does not return parameters, method, or endpoint.
- The read/write/destructive rules in §2 apply exactly as for a listed action.

[references/extend-apis.md](references/extend-apis.md) carries the service-code / version / endpoint / signing-region recipes for the extension services that were previously wrapped by a helper script (CDN, DCDN, domain, Flink, GA, IoT, Live, MCDN, Metrics, sec_agent, trademark, VEEN, VKE).

### Extension helper (query + body in one request only)

`ve --force` cannot send URL query parameters *and* a request body in one POST. A handful of APIs (VMP Prometheus queries, Flink GWS) need exactly that; use the helper for those and nothing else:

```bash
python3 scripts/call_extend_api.py --list
python3 scripts/call_extend_api.py --api QueryMetrics --params '{"workspace":"<id>","query":"up"}'
```

After upgrading `ve`, run `python3 scripts/audit_extend_apis.py` — it lists which recipes/helper entries the new metadata now covers natively, so they can be dropped.

It also has a free mode (`--service/--version/--query-keys`) for unregistered APIs with the same shape. Credentials, options and the registered list are in [references/extend-apis.md](references/extend-apis.md). Do not pass `--profile` unless the user has explicitly selected one for this conversation.

---

## 4. Execute API Calls

### Basic Format

```text
ve <ServiceCode> <ActionName> --ParamName "value" [system flags]
```

System flags (`--profile`, `--region`, `--endpoint`, `--output`, `--query`, …) go after the Action, in any order relative to the parameters.

### Parameter Passing Rules

Determine the format from `--help` output:
- **Flat parameter format**: `--help` lists individual `--Key type` entries (e.g., ECS, VPC, IAM) -> pass with `--Key "value"`
- **Array parameters**: prefer the numbered CLI form shown by `--help`, such as `--InstanceIds.1 "$instance_id"` or `--SubnetIds.1 "$subnet_id"`. Do not assume JSON-array strings are accepted by every action.
- **JSON format**: `--help` only shows `--body '{...}'` (e.g., Redis, CR, and other POST APIs) -> pass with `--body '{...}'`

```bash
# Flat parameters — nested fields use dot notation; arrays use .N index (starting from 1)
ve ecs RunInstances --ZoneId "cn-beijing-a"
ve ecs RunInstances --NetworkInterfaces.1.SubnetId "subnet-xxxx"
ve ecs RunInstances --Tags.1.Key "publish-by" --Tags.1.Value "deploy-skill"

# JSON format (when --help only shows --body)
ve redis CreateDBInstance --body '{"InstanceName":"demo","RegionId":"cn-beijing","ConfigureNodes":[{"AZ":"cn-beijing-a"}],"ShardedCluster":0,"NodeNumber":2,"ShardCapacity":1024,"ShardNumber":1,"EngineVersion":"6.0","SubnetId":"subnet-xxxx","VpcId":"vpc-xxxx","Password":"<secret>","Tags":[{"Key":"publish-by","Value":"deploy-skill"}]}'
```

### Output format and querying

Every API call accepts `--output` and `--query`; they replace ad-hoc `grep`/`jq` over the JSON.

| `--output` | Use |
| --- | --- |
| `json` (default) | Full response; the form to parse programmatically |
| `table` / `table-num` | Human-readable list; `table-num` adds a row-number column — good for showing the user a resource list |
| `text` | Plain values, one per line — good for capturing a single field or ID list in a shell variable |
| `yaml` | Human-readable nested detail |
| `off` | Run the call but print nothing (skips response-dependent `--query` evaluation). Only for calls whose response you genuinely do not need — never for `Create*`/`Run*`/`Allocate*`, whose response is the only place the new resource ID appears |

`--query` takes a JMESPath expression evaluated on the **full** response before formatting, so paths start at `Result.` (or `ResponseMetadata.`):

```bash
# Single field
ve sts GetCallerIdentity --query 'Result.AccountId' --output text

# Project a list for the user
ve ecs DescribeInstances --query 'Result.Instances[].{Id:InstanceId,Name:InstanceName,Status:Status,Zone:ZoneId}' --output table

# Filter, then pick IDs into a shell variable
ids=$(ve ecs DescribeInstances --query "Result.Instances[?Status=='RUNNING'].InstanceId" --output text)

# Length / existence checks
ve vpc DescribeVpcs --query 'length(Result.Vpcs)' --output text
```

Rules of thumb:
- Keep `json` when you (the agent) need to read the response; switch to `table`/`yaml` only for what you show the user.
- Do not `--query` a write/destructive call into silence before you have seen `ResponseMetadata.Error`; on failure the error object is still printed.
- `--query` filters what is printed, not what is requested — pagination (`NextToken`, `PageNumber`) is unchanged.

### Response Format

```json
// Success
{ "ResponseMetadata": { "RequestId": "..." }, "Result": { ... } }

// Failure
{ "ResponseMetadata": { "Error": { "Code": "...", "Message": "..." } } }
```

### Error Handling

Whenever a `ve` command or extension helper fails, or a response contains `ResponseMetadata.Error`, read [references/common-errors.md](references/common-errors.md) completely before diagnosing the error or responding to the user. Partial searches, matched lines, or excerpts do not satisfy this requirement.

First classify the error as request-format, missing dependency, account state, service activation, real-name verification, purchase qualification, or permission related. For product-specific errors, also read the matching service note below. For permission errors (`AccessDenied`, `NoPermission`, `RoleNotExist`, `Forbidden`, or STS-related failures), activate the `volcengine-troubleshooting` skill and use its account-permission diagnosis capability to locate the root cause and guide the user through remediation.

### Async Resource Creation Requires Polling

Some resources (VKE clusters, RDS instances, ECS instances, etc.) take several minutes to create. After creation, poll the Describe endpoint until the resource reaches the desired status before proceeding.

> Creating sub-resources (e.g., security groups) immediately after VPC creation may fail with `InvalidVpc.InvalidStatus`. Create sub-resources sequentially (subnet first, then security group), or wait a few seconds and retry.

```text
# General polling pattern: check every 30 s, give up after a deadline, stop on API failure
max_attempts=40   # 40 x 30 s = 20 min; size it to the resource type
for attempt in $(seq 1 "$max_attempts"); do
  if ! cur_status=$(ve <svc> Describe<Resource> --<IdParam> "xxx" --query 'Result.<Path>.Status' --output text 2>&1); then
    echo "describe failed: $cur_status"; break        # classify with common-errors.md, do not keep looping
  fi
  echo "$(date +%H:%M:%S) $cur_status"
  case "$cur_status" in
    Running) break ;;
    Error|Failed|Deleted) echo "resource entered $cur_status"; break ;;
  esac
  [ "$attempt" -eq "$max_attempts" ] && echo "timed out waiting for Running"
  sleep 30
done
```

`Result.<Path>` and the terminal status names differ per product — take them from `--help --detail` and the service note, do not assume `Running`.

---

## 5. End-to-End Execution Flow (Summary)

```text
1. Initialize: verify credentials -> GetCallerIdentity -> confirm region
2. Understand the task: is the user querying or making changes?
3. Locate the API: ve --help first -> find_api.py as fallback -> --force if the metadata lacks it
4. Retrieve parameters: --help, then --help --detail for write/destructive actions
5. Query dependent resources: use Describe*/List* (with --query to pick IDs) to obtain required IDs
6. Read operation -> execute directly and display results (--output table for lists)
   Write operation -> show command -> DryRun (if supported) -> user confirmation -> execute
7. Parse the response and report results to the user
```

---

## 6. Service-Specific Notes

Consult or update the corresponding notes file when encountering service-specific issues:

- Common errors: [references/common-errors.md](references/common-errors.md)
- Console Login procedure (`ve_login_remote.sh`, exit codes, rules): [references/console-login.md](references/console-login.md)
- Cloud Control API (cloudcontrol): [references/cloudcontrol.md](references/cloudcontrol.md)
- ECS: [references/ecs.md](references/ecs.md)
- VPC: [references/vpc.md](references/vpc.md)
- CR: [references/cr.md](references/cr.md)
- ALB: [references/alb.md](references/alb.md)
- CLB: [references/clb.md](references/clb.md)
- VKE: [references/vke.md](references/vke.md)
- veFaaS: [references/vefaas.md](references/vefaas.md)
- RDS: [references/rds.md](references/rds.md)
- Message Queue: [references/mq.md](references/mq.md)
- Storage: [references/storage.md](references/storage.md)
- Observability: [references/observability.md](references/observability.md)
- DNS/Edge: [references/dns-edge.md](references/dns-edge.md)
- IAM: [references/iam.md](references/iam.md)
- KMS: [references/kms.md](references/kms.md)
- Redis: [references/redis.md](references/redis.md)
- NAT Gateway: [references/natgateway.md](references/natgateway.md)
- EBS: [references/ebs.md](references/ebs.md)
- Extension APIs (`--force` recipes + query/body helper): [references/extend-apis.md](references/extend-apis.md)
