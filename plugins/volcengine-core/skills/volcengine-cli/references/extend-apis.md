# Extended APIs

Use this reference when a Volcengine API is missing from the normal `ve` command surface but can still be called as a Volcengine OpenAPI extension.

The helper script is:

```bash
python3 scripts/call_extend_api.py
```

It embeds the extension API registry and the request-signing code needed by these APIs. It does not import external repositories.

## Credentials

The script resolves credentials in this order:

1. Environment variables.
2. Existing Volcengine CLI profile credentials from `VOLCENGINE_CLI_CONFIG_FILE`, or the default `~/.volcengine/config.json`.

If `VOLCENGINE_ACCESS_KEY` or `VOLCENGINE_SECRET_KEY` is not detected, the helper prints a notice and then tries the default `ve` CLI profile resolution. It reads local credentials directly.

`VOLCENGINE_CLI_CONFIG_FILE` expects a full config file path such as `/path/to/config.json`, not a config directory. When it is unset, the helper uses `~/.volcengine/config.json`.

For any profile mode, if the selected profile already contains `access-key` and `secret-key`, the helper uses them with optional `session-token`. For `console-login`, it can also read an unexpired local `ve login` cache. The helper does not refresh SSO, assume RAM roles, exchange OIDC tokens, or fetch ECS metadata; if the selected profile has no usable AK/SK/cache, ask the user to run the matching `ve` login/configure command or set environment credentials.

Profile selection must follow the conversation-scoped rule in the main `SKILL.md`:

- Do not pass `--profile` unless the user explicitly selected a profile for this conversation.
- If the user did select a profile, keep using the same `--profile <profile-name>` for subsequent extension helper calls.
- Do not inspect profile names, regions, list order, or config contents to decide a profile yourself.

Environment variables:

```bash
export VOLCENGINE_ACCESS_KEY="AK..."
export VOLCENGINE_SECRET_KEY="SK..."
export VOLCENGINE_REGION="cn-beijing"
# Optional:
export VOLCENGINE_SESSION_TOKEN="..."
export VOLCENGINE_CLI_CONFIG_FILE="/path/to/config.json"
```

CLI profile fallback when the user explicitly selected a profile:

```bash
python3 scripts/call_extend_api.py \
  --profile <user-selected-profile> \
  --api QueryMetrics \
  --params '{"workspace":"vmp-workspace-id","query":"up"}'
```

Default fallback when the user did not select a profile:

```bash
python3 scripts/call_extend_api.py \
  --api QueryMetrics \
  --params '{"workspace":"vmp-workspace-id","query":"up"}'
```

Do not print or echo secrets in the conversation. If both environment credentials and CLI profile resolution fail, ask the user to run `ve login`, configure a `ve` profile, or set `VOLCENGINE_ACCESS_KEY` and `VOLCENGINE_SECRET_KEY` in their shell.

## Discover Supported APIs

List the registry:

```bash
python3 scripts/call_extend_api.py --list
```

Describe one API:

```bash
python3 scripts/call_extend_api.py --describe QueryMetrics
```

Include test-only entries:

```bash
python3 scripts/call_extend_api.py --list --include-test
```

## Call An API

Basic form:

```bash
python3 scripts/call_extend_api.py \
  --api QueryMetrics \
  --params '{"workspace":"vmp-workspace-id","query":"up"}'
```

Pass params from a file:

```bash
python3 scripts/call_extend_api.py \
  --api ListPipelineRunStagesInner \
  --params @request.json
```

Assert the expected method:

```bash
python3 scripts/call_extend_api.py \
  --api ListAccelerateAreas \
  --method GET \
  --params '{}'
```

Override endpoint host only when the registry has a product endpoint or the user provides one:

```bash
python3 scripts/call_extend_api.py \
  --api QueryMetrics \
  --host open.volcengineapi.com \
  --params '{"workspace":"vmp-workspace-id","query":"up"}'
```

The script resolves `service`, `version`, `method`, default endpoint, scheme, and default `content_type` from the registry. If `--method` disagrees with the registry, it fails before making a request.
For APIs marked with query parameters in the registry, include those keys in `--params`; the helper signs them as URL query parameters and sends the remaining keys as the body.

## Account Verification

Use `GetVerifyInfo` to check real-name verification status:

```bash
python3 scripts/call_extend_api.py --api GetVerifyInfo
```

The default pretty output includes a derived summary:

- `verification.is_verified`: `IsVerified=true`.
- `verification.identity_type`: raw `IdentityType`, such as `individual` or `enterprise`.
- `verification.individual_verified`: `IsVerified=true` and `IdentityType="individual"`.
- `verification.enterprise_verified`: `IsVerified=true` and `IdentityType="enterprise"`.

## VMP Metric API Notes

The VMP extension APIs mirror Prometheus query APIs but are signed through Volcengine OpenAPI:

- `QueryMetrics`, `QueryMetricsRange`, `GetLabels`, and `GetSeries` put `workspace` in the URL query.
- `GetLabelValues` puts both `workspace` and `label` in the URL query.
- Remaining parameters are sent in an `application/x-www-form-urlencoded` body.
- Series selector parameters must use the Prometheus HTTP API name `match[]`. Do not pass `match` or `matches` for `GetSeries`, `GetLabels`, or `GetLabelValues`.

Example:

```bash
python3 scripts/call_extend_api.py \
  --api GetSeries \
  --params '{"workspace":"vmp-workspace-id","match[]":["up{job=\"node\"}"]}'
```

To validate VMP APIs with real data, create a temporary VMP workspace, enable public access, and configure authentication before writing samples:

```bash
ve vmp CreateWorkspace --body '{
  "Name":"codex-vmp-api-verify",
  "InstanceTypeId":"vmp.standard.15d",
  "Tags":[{"Key":"publish-by","Value":"deploy-skill"}],
  "DeleteProtectionEnabled":false,
  "PublicAccessEnabled":true,
  "PublicWriteBandwidth":1,
  "PublicQueryBandwidth":1
}'
```

Set BasicAuth with `Username` and a base64-encoded `Password`. Do not set `AuthType` to `Basic`; the service reports `InvalidParameter.AuthType`. Confirm with `GetWorkspaceAuthInfo`, which should return `AuthType: BasicAuth`.

```bash
ve vmp UpdateWorkspace --body '{
  "Id":"vmp-workspace-id",
  "Username":"user-name",
  "Password":"base64-encoded-password"
}'
```

Use `GetWorkspace` to obtain `PrometheusWriteEndpoint`; append `/api/v1/write` for Prometheus remote write. A successful remote-write request returns HTTP `204`. The path `/api/v1/push` was not accepted for this workspace during validation.

After writing a sample such as `codex_vmp_verify_value{run_id="..."} 42`, verify all five extension APIs:

```bash
python3 scripts/call_extend_api.py \
  --api QueryMetrics \
  --params '{"workspace":"vmp-workspace-id","query":"codex_vmp_verify_value{run_id=\"run-id\"}","time":"sample-or-later-unix-second"}'

python3 scripts/call_extend_api.py \
  --api QueryMetricsRange \
  --params '{"workspace":"vmp-workspace-id","query":"codex_vmp_verify_value{run_id=\"run-id\"}","start":"sample-start","end":"sample-end","step":"10s"}'

python3 scripts/call_extend_api.py \
  --api GetLabels \
  --params '{"workspace":"vmp-workspace-id","match[]":["codex_vmp_verify_value{run_id=\"run-id\"}"]}'

python3 scripts/call_extend_api.py \
  --api GetLabelValues \
  --params '{"workspace":"vmp-workspace-id","label":"run_id","match[]":["codex_vmp_verify_value{run_id=\"run-id\"}"]}'

python3 scripts/call_extend_api.py \
  --api GetSeries \
  --params '{"workspace":"vmp-workspace-id","match[]":["codex_vmp_verify_value{run_id=\"run-id\"}"]}'
```

For instant queries against freshly written remote-write data, query at or after the stored sample timestamp. A query before the sample timestamp can correctly return an empty vector even though range queries already show the sample.

## Safety

Apply the same safety rules as normal `ve` calls:

- Read-only actions such as `Describe*`, `List*`, `Get*`, `Query*`, `Check*`, and `Search*` can be run directly when the user asks for them.
- Write actions such as `Create*`, `Run*`, `Update*`, `Set*`, `Start*`, `Register*`, and `Import*` require confirmation.
- Destructive actions such as `Delete*`, `Stop*`, and `Cancel*` require explicit confirmation and an impact summary.

Parameter names and semantics are captured below so this file remains self-contained. Keep params explicit and prefer small read-only calls first.

## API Index

Use this index for quick lookup by service or API name.

| Service | APIs |
| --- | --- |
| `account_verify` | `GetVerifyInfo` |
| `CDN` | `DescribeOriginTopStatisticalData` |
| `cp` | `ListPipelineRunStagesInner` |
| `dcdn` | `DescribeOriginRealtimeData`, `DescribeRealtimeData`, `DescribeTopIPs`, `DescribeTopReferers`, `DescribeTopUrls` |
| `domain_openapi` | `CheckFee`, `GetAsyncTask`, `GetDomain`, `GetTemplate`, `ListDomains`, `ListTemplates`, `RegisterDomain` |
| `flink` | `CancelGWSApplication`, `CreateGWSApplicationDraft`, `DeleteGWSApplication`, `DeployGWSApplicationDraft`, `GWSGetEventList`, `GetGMSProjectDetail`, `GetGRSAppById`, `GetGWSApplication`, `GetGWSApplicationDraft`, `ListGASLogs`, `ListGMCSResourcePool`, `ListGMSProject`, `ListGWSApplication`, `ListGWSDirectory`, `RestartGWSApplication`, `StartGWSApplication`, `UpdateGWSApplicationDraft` |
| `ga` | `DescribeListenerLogs`, `GetAcceleratorDimension`, `GetBandwidthPackage`, `GetBasicEndpointRelatedAccInstanceInfos`, `GetEndpointRelatedAccInstanceInfos`, `ListAccelerateAreas`, `ListBandwidthPackages` |
| `iot` | `CallService`, `GetAllLastDevicePropertyValue`, `GetCustomTopicList`, `GetDeviceDetail`, `GetDeviceEventRecordList`, `GetDeviceList`, `GetDeviceOverview`, `GetDeviceServiceCallRecordList`, `GetDeviceStatus`, `GetInstanceDetail`, `GetInstanceEndpoints`, `GetInstanceList`, `GetLastDevicePropertyValue`, `GetProductDetail`, `GetProductList`, `GetPropertyValuesByTime`, `GetThingModel`, `SetProperty` |
| `live` | `DescribeLiveBatchStreamSessionData`, `DescribeLiveBatchStreamTranscodeData` |
| `mcdn` | `DescribeCdnDomainConfig` |
| `metrics` | `GetQueryCluster`, `GetWorkspaceInfo`, `InfluxQuery`, `ListPreagg`, `ListQueryClusters`, `ListWorkspace`, `MetricsQuery` |
| `sec_agent` | `RunAlertFormatter`, `RunAlertInvestigator`, `RunDlpScreenshotAnalyzer`, `RunPcapAnalyzer`, `RunSensitiveDataDetector`, `RunThreatIntelProducer`, `RunWebRiskAssessor` |
| `trademark` | `GetApplicant`, `GetRequirement`, `GetTrademark`, `ListApplicants`, `ListBarrierTrademarks`, `ListRequirements`, `ListTrademarks`, `SearchTrademark`, `SearchTrademarkInfo` |
| `veenedge` | `GetBandwidthUsage`, `GetBillingUsageDetail`, `GetVEENInstanceUsage`, `GetVEEWInstanceUsage`, `RebootCloudServer`, `StartCloudServer`, `StopCloudServer` |
| `vke` | `CreateVirtualNode`, `ListVirtualNodes` |
| `vmp` | `GetLabelValues`, `GetLabels`, `GetSeries`, `QueryMetrics`, `QueryMetricsRange` |

## Supported APIs

| APIName | Service | Version | Method | Purpose |
| --- | --- | --- | --- | --- |
| `GetVerifyInfo` | `account_verify` | `2018-01-01` | POST | Account real-name verification status |
| `DescribeOriginTopStatisticalData` | `CDN` | `2021-03-01` | POST | CDN origin-side top statistical data |
| `ListPipelineRunStagesInner` | `cp` | `2023-05-01` | POST | CodePipeline stage/task list for a pipeline run |
| `DescribeRealtimeData` | `dcdn` | `2021-04-01` | POST | DCDN realtime edge data |
| `DescribeOriginRealtimeData` | `dcdn` | `2021-04-01` | POST | DCDN realtime origin data |
| `DescribeTopIPs` | `dcdn` | `2021-04-01` | POST | DCDN top client IP ranking |
| `DescribeTopReferers` | `dcdn` | `2021-04-01` | POST | DCDN top referer ranking |
| `DescribeTopUrls` | `dcdn` | `2021-04-01` | POST | DCDN top URL ranking |
| `CheckFee`, `GetDomain`, `GetAsyncTask`, `GetTemplate`, `ListDomains`, `ListTemplates` | `domain_openapi` | `2022-12-12` | GET | Domain price, domain, task, and template queries |
| `RegisterDomain` | `domain_openapi` | `2022-12-12` | POST | Register a domain; creates a billable async task |
| Flink GMS/GWS/GAS actions | `flink` | `2021-06-01`, `2022-06-01` | GET/POST | Flink project, resource-pool, draft, application, event, and log operations |
| GA actions | `ga` | `2022-03-01` | GET/POST | Global Accelerator area, bandwidth package, metric, listener, and endpoint queries |
| IoT actions | `iot` | `2021-12-14` | POST | IoT instance, product, device, thing-model, service-call, and property operations |
| `DescribeLiveBatchStreamTranscodeData`, `DescribeLiveBatchStreamSessionData` | `live` | `2023-01-01` | POST | Live stream transcode/session statistics |
| `DescribeCdnDomainConfig` | `mcdn` | `2022-03-01` | GET | Multi-cloud CDN domain configuration |
| Metrics actions | `metrics` | `2024-06-29` | POST | Metrics workspace, query-cluster, pre-aggregation, Influx, and metrics queries |
| Security workflow actions | `sec_agent` | `2025-01-01` | POST | Security workflow execution and result retrieval |
| Trademark actions | `trademark` | `2023-06-01` | GET/POST | Trademark applicant, requirement, trademark, barrier, and search queries |
| VEEN actions | `veenedge` | `2021-04-30` | GET/POST | VEEN instance usage queries and cloud-server start/stop/reboot operations |
| `CreateVirtualNode`, `ListVirtualNodes` | `vke` | `2022-05-12` | POST | VKE virtual node create/list |
| VMP metric actions | `vmp` | `2021-03-03` | POST | Signed Prometheus-compatible query APIs |

## Parameter Reference

Unless noted otherwise, pass all fields in `--params` as one JSON object. The helper resolves `Action`, `Version`, `Service`, `Method`, endpoint host, and content type from the registry.

### Account Verification

`GetVerifyInfo`:

- No request parameters are required.
- Personal real-name verification is `IsVerified=true` with `IdentityType="individual"`.
- Enterprise real-name verification is `IsVerified=true` with `IdentityType="enterprise"`.

### CDN

`DescribeOriginTopStatisticalData`:

- Required: `Domain`, `StartTime`, `EndTime`, `Item`, `Metric`.
- `StartTime` and `EndTime` are Unix timestamps in seconds.
- `Item` currently supports `url`.
- `Metric` supports `flux`, `pv`, `status_2xx`, `status_3xx`, `status_4xx`, `status_5xx`.

### CodePipeline

`ListPipelineRunStagesInner`:

- Required: `WorkspaceId`, `PipelineId`, `PipelineRunId`.
- Use it after listing workspaces, pipelines, and pipeline runs with normal `ve cp` APIs.

### DCDN

`DescribeRealtimeData` and `DescribeOriginRealtimeData`:

- Required: `StartTime`, `EndTime`, `Metrics`.
- `StartTime` and `EndTime` use `"YYYY-MM-DD HH:MM:SS"` and the range must be within 24 hours.
- `Metrics` is an array. Common values: `all`, `traffic`, `bandwidth`, `request`, `QPS`, `2xx`, `3xx`, `4xx`, `5xx`; edge realtime also supports `RequestHitRate` and `TrafficHitRate`.
- Optional filters include `Domains`, `ProjectName`, `IspNameEn`, `RegionNameEn`, `Protocol`, `Type`, `IPVersion`.

`DescribeTopIPs`, `DescribeTopReferers`, and `DescribeTopUrls`:

- Required: `StartTime`, `EndTime`, `Sort`.
- `Sort` supports `traffic`, `bandwidth`, `request`, `QPS`.
- Optional: `Limit` (1-100), `ProjectName`, `Domain`, `StatusCode`.

### Domain

`CheckFee`:

- Required query field: `domain`.

`GetDomain`:

- Optional query fields: `domain`, `instance_no`. Provide at least one useful identifier.

`GetAsyncTask`:

- Required query field: `task_no`.

`GetTemplate`:

- Required query field: `tag`.

`ListDomains`:

- Optional query fields: `domain`, `status`, `verify_status`, `expired_after`, `is_auto_renew`, `domain_name_audit_status`, `order_by`, `asc_or_desc`, `page_number`, `page_size`.

`ListTemplates`:

- Optional query fields: `registrant_zh`, `registration_type`, `tag`, `status`, `page_number`, `page_size`.

`RegisterDomain`:

- Required body fields: `domain`, `template_tag`.
- Optional: `period`, `ns_list`, `is_auto_renew`, `package_id`.
- This is billable and creates an async task. Confirm with the user before calling.

### Flink

GET actions:

- `ListGMSProject`: optional `SearchKey`, `PageSize`, `PageNum`.
- `GetGMSProjectDetail`: required `ProjectName`.
- `ListGMCSResourcePool`: `ProjectId`, optional `Name`, `NameKey`, `PageSize`, `PageNum`; use version `2022-06-01`.
- `GetGRSAppById`: required `AppIdKey`.

GWS/GAS POST actions:

- `ListGWSDirectory`: query-style fields `ProjectId`, `Type` (`JOB` or `QUERY`).
- `GetGWSApplicationDraft`: `ProjectId`, `Id`.
- `CreateGWSApplicationDraft`: `ProjectId`, `JobName`, `DirectoryId`, optional `JobType`, `EngineVersion`.
- `UpdateGWSApplicationDraft`: `Id`, `ProjectId`, `AccountId`, `UserId`, `JobName`, `JobId`, `DirectoryId`, `DirectoryName`, `SqlText`, optional `DynamicOptions`, `JobType`, `EngineVersion`.
- `DeployGWSApplicationDraft`: `ProjectId`, `Id`, `ResourcePool`, `Queue`, optional `Priority`, `SchedulePolicy`, `ScheduleTimeout`.
- `DeleteGWSApplication`, `StartGWSApplication`, `CancelGWSApplication`, `RestartGWSApplication`: `ProjectId`, `Id`; start/restart also support `Type` such as `FROM_NEW` or `FROM_LATEST`.
- `ListGWSApplication`: optional `ProjectId`, `JobName`, `ResourcePool`, `JobType`, `State`, `PageSize`, `PageNum`, `SortField`, `SortOrder`.
- `GetGWSApplication`: required `Id`, optional `AccountId`.
- `GWSGetEventList`: `ProjectId`, optional `Id`, `Limit`.
- `ListGASLogs`: `Application`, `Project`, `StartTime`, `EndTime`; optional `Level`, `Properties.component`, `Properties.podName`, `Cursor`, `PageSize`.

### Global Accelerator

`ListAccelerateAreas`:

- No required parameters.

`ListBandwidthPackages`:

- Required in observed request shape: `BandwidthType`, `PageNumber`, `PageSize`.
- Optional: `AcceleratorId`, `AccountId`, `BandwidthPackageId`, `Domain`, `Isp`, `OrderType`, `State`, `States`, `ProjectName`, `ResourceTagFilter`.

`GetBandwidthPackage`:

- Required: `BandwidthPackageId`.

`GetAcceleratorDimension`:

- Required: `AcceleratorType`, `TargetName`, `Filters`.
- `Filters` is an array of `{ "Name": "...", "Values": ["..."] }`.

`DescribeListenerLogs`:

- Required: `InputIdType`, `InputId`, `StartTime`, `EndTime`, `Interval`.
- Optional: `Metrics`, `RegionType`, `Region`, grouping fields.

`GetBasicEndpointRelatedAccInstanceInfos` and `GetEndpointRelatedAccInstanceInfos`:

- Require the endpoint identifier used by the corresponding GA endpoint type. Include pagination fields such as `PageNum`/`PageSize` when listing related instances.

### IoT

The IoT extension APIs use product-specific identifiers. Common fields are:

- Instance: `InstanceId`.
- Product: `ProductKey` or `ProductID`.
- Device: `DeviceName`, `DeviceID`, `DeviceSecret`, depending on the API.
- Thing model: `ModuleKey`, `Identifier`, `PropertyIdentifier`, `EventIdentifier`, `ServiceIdentifier`.
- Pagination and time range: `PageNumber`, `PageSize`, `StartTime`, `EndTime`.
- `CallService` needs target device identifiers plus service identifier and input params.
- `SetProperty` needs target device identifiers plus property values.

IoT was not business-tested in this account because the service could not be opened.

### Live

`DescribeLiveBatchStreamTranscodeData`:

- Required: `StartTime`, `EndTime`.
- Optional: `DomainList`, `PageNum`, `PageSize`.
- Times are RFC3339 strings, for example `2022-11-10T00:00:00+08:00`.

`DescribeLiveBatchStreamSessionData`:

- Required: `StartTime`, `EndTime`.
- Optional: `DomainList`, `PageNum`, `PageSize`, `OnlineUserType`, plus stream/session dimensions when available.
- Times are RFC3339 strings.

### MCDN

`DescribeCdnDomainConfig`:

- Optional identifiers: `DomainId`, `DomainName`, `Vendor`, `DomainVersion`, `NormalizeOptions`.
- Prefer `DomainId` when known.

### Metrics

`ListWorkspace`:

- Recommended: `PageNumber`, `PageSize`, `ListGlobal`.
- Optional: `Filters`, `ProjectName`.

`GetWorkspaceInfo`:

- Required: `WorkspaceId`.

`ListQueryClusters`:

- Recommended: `Page` object with `PageNumber` and `PageSize`.
- Optional: `Name`, `ProjectName`.

`GetQueryCluster`:

- Required: `Id`.

`ListPreagg`:

- Recommended: `PageNumber`, `PageSize`, `onlyShowMine`.
- Optional: `Filters`, such as `{"WorkspaceName":"..."}`.

`InfluxQuery` and `MetricsQuery`:

- Require a real workspace/query context and query payload. Include workspace identifier, query expression(s), and time range fields according to the query type.

### Security Workflows

`RunAlertInvestigator`, `RunPcapAnalyzer`, `RunAlertFormatter`, `RunThreatIntelProducer`, `RunWebRiskAssessor`, `RunDlpScreenshotAnalyzer`, `RunSensitiveDataDetector`:

- Require real workflow input such as alert details, PCAP content/reference, URL, screenshot/image data, or text to inspect.
- Do not treat an empty workflow request as validation.

### Trademark

GET actions:

- `GetApplicant`: required `ApplicantID`.
- `GetTrademark`: required `TrademarkID`.
- `GetRequirement`: required `RequirementID`.
- `ListApplicants`: optional `ApplicantType`, `ApplicantName`, `Status`, `Country`, `PageNumber`, `PageSize`, `OrderBy`.
- `ListRequirements`: optional status/type filters plus `PageNumber`, `PageSize`.
- `ListTrademarks`: optional trademark/applicant/status filters plus `PageNumber`, `PageSize`.
- `ListBarrierTrademarks`: optional requirement/trademark identifiers and pagination fields.

POST actions:

- `SearchTrademarkInfo`: required `ClassID` and `RegistrationNumber`.
- `SearchTrademark`: provide at least one useful search condition such as `TrademarkName`, `ApplicantName`, or `RegistrationNumber`; optional `PageNumber`, `PageSize`, class/status filters.

### VEEN

`StartCloudServer`, `StopCloudServer`, `RebootCloudServer`:

- Require the target cloud-server identifier. Confirm before start/stop/reboot.

`GetVEENInstanceUsage`, `GetVEEWInstanceUsage`, `GetBandwidthUsage`, `GetBillingUsageDetail`:

- Usage queries require a billing or resource time range and resource filters. During validation, these GET actions reached `veenedge.volcengineapi.com` but returned `Method Not Allowed`.

### VKE

`ListVirtualNodes`:

- Optional pagination and filters such as `PageNumber`, `PageSize`, cluster or virtual-node identifiers.

`CreateVirtualNode`:

- Required: `Kubeconfig`, `VirtualNodeConfig`.
- This creates infrastructure and needs a cleanup plan before execution.

### VMP

The VMP action-specific parameter details are in "VMP Metric API Notes" above. The short form:

- `QueryMetrics`: URL query key `workspace`; body fields include `query`, optional `time`.
- `QueryMetricsRange`: URL query key `workspace`; body fields include `query`, `start`, `end`, `step`.
- `GetLabelValues`: URL query keys `workspace`, `label`; body supports `match[]`, `start`, `end`.
- `GetLabels`: URL query key `workspace`; body supports `match[]`, `start`, `end`.
- `GetSeries`: URL query key `workspace`; body supports `match[]`, `start`, `end`.

## Notes For Agents

- Prefer normal `ve` commands when available. Use this helper only when `ve` does not expose the needed API.
- The registry is exact-match by `APIName`. If duplicate names appear, pass `--service`.
- Do not invent params. Use the parameter reference in this file; if a required business ID is missing, ask the user for it or locate it with a read-only list/get command.
- Some registry entries have product-specific default hosts such as `cdn.volcengineapi.com`, `live.volcengineapi.com`, `iot.cn-shanghai.volcengineapi.com`, or `veenedge.volcengineapi.com`.

## Verification Notes

- `ListPipelineRunStagesInner` was tested with an existing CP workspace, pipeline, and pipeline run and returned HTTP 200 with stage/task data.
- `ListVirtualNodes` returned HTTP 200 with an empty list.
- `ListPreagg` returned HTTP 200 with an empty response.
- VMP metric APIs (`QueryMetrics`, `QueryMetricsRange`, `GetLabelValues`, `GetLabels`, `GetSeries`) were validated against a temporary `vmp.standard.15d` workspace with a real remote-write sample `codex_vmp_verify_value{run_id="run_20260602_1916",source="codex"} 42`. `QueryMetrics` and `QueryMetricsRange` returned value `42`; `GetLabels` returned `__name__`, `run_id`, and `source`; `GetLabelValues` returned the test `run_id`; `GetSeries` returned the complete series. The temporary workspace was deleted afterwards and `GetWorkspace` returned `ResourceNotExist`.
- Live batch stream APIs returned permission errors after valid `StartTime`/`EndTime` parameters were supplied, confirming the earlier `InvalidParam` was only parameter-shape related.
- `CreateVirtualNode` reached VKE and requires `Kubeconfig` plus `VirtualNodeConfig`. It was not executed because it needs an external Kubernetes kubeconfig and the registry does not include a matching virtual-node delete API for cleanup.
- Most domain, IoT, trademark, metrics, sec_agent, VEEN, and Flink APIs returned `AccessDenied` for the tested account. Creating dependent resources cannot bypass IAM denial; use an account with the relevant service permissions for full business-flow testing.

Implementation notes:

| Implementation style | Services observed | Validation note |
| --- | --- | --- |
| Signed Action/Version root path for former universal entries | `cp`, `vke` | Uses `/?Action=...&Version=...` with the registry's service, version, method, and content type. |
| Signed Action/Version root path | `CDN`, `dcdn`, `domain_openapi`, `ga`, `live`, `mcdn`, `metrics`, `sec_agent`, `trademark`, `veenedge` | Uses `/?Action=...&Version=...` with service-specific signing region, endpoint, scheme, and method from the registry. |
| Signed Prometheus-compatible Action/Version path | `vmp` | Uses the VMP regional endpoint, URL query keys for `workspace`/`label`, and form-encoded body parameters. |
| Signed Flink compatibility request | `flink` | Keeps the Flink registry style for parameter routing, then sends the wire request through `/?Action=...&Version=...` like the SDK interceptor. |

Current business validation status:

| Service | APIs | Result |
| --- | --- | --- |
| `vmp` | `QueryMetrics`, `QueryMetricsRange`, `GetLabels`, `GetLabelValues`, `GetSeries` | Fully validated with a temporary VMP workspace and real remote-write sample value `42`. The valid write endpoint was `PrometheusWriteEndpoint + /api/v1/write`; `/api/v1/push` was not accepted. Workspace was deleted and deletion was confirmed. |
| `cp` | `ListPipelineRunStagesInner` | Fully validated with an existing workspace, pipeline, and pipeline run. Response returned real stage/task/step data matching public `ve cp ListPipelineRuns` context. |
| `dcdn` | `DescribeRealtimeData`, `DescribeOriginRealtimeData`, `DescribeTopIPs`, `DescribeTopReferers`, `DescribeTopUrls` | Validated through signed Action/Version calls. `StartTime`/`EndTime` must be `"YYYY-MM-DD HH:MM:SS"` strings. Realtime APIs use `Metrics` array; top APIs use `Sort`. Current account has no DCDN domains (`ve dcdn ListDomainConfig` returned total `0`), so statistical responses correctly returned empty result structures. |
| `domain_openapi` | `ListDomains`, `ListTemplates`, `CheckFee` | Validated through signed Action/Version calls. Lists returned empty account resources. `CheckFee` returned real pricing fields for a sample `.com` domain, proving business lookup works without creating a domain. Detail/task/register APIs require existing domain/template/task IDs or would register a billable domain. |
| `trademark` | list APIs, `SearchTrademark`, `SearchTrademarkInfo` | List APIs returned empty account resources. Search/detail APIs reached business logic: bad/missing params returned field-specific errors; sample public names/registration numbers returned no-match/not-exists business errors. Positive validation needs a known registration number plus class ID accepted by this service. |
| `metrics` | `ListWorkspace`, `ListQueryClusters`, `ListPreagg` | Validated with required fields such as `ListGlobal`, pagination, and `onlyShowMine`. Current account has no Metrics workspaces/query clusters/pre-aggregation rules, so responses were HTTP 200 with empty/null business payloads. `Get*`/query APIs need real workspace or cluster IDs. |
| `ga` | `ListAccelerateAreas`, `ListBandwidthPackages`, `GetAcceleratorDimension`, related endpoint info APIs | `ListAccelerateAreas` returned real area metadata. Bandwidth/accelerator/dimension/endpoint-related APIs returned empty results, consistent with `ve ga ListAccelerators` and `ve ga ListPublicBandwidthPackages` showing zero resources. Resource-detail APIs need GA accelerator, bandwidth package, listener, or endpoint IDs. |
| `live` | `DescribeLiveBatchStreamTranscodeData`, `DescribeLiveBatchStreamSessionData` | Validated through signed Action/Version calls and RFC3339 time strings. `ListDomainDetail` returned no live domains; both private stats APIs returned zero totals and empty stream lists, matching current resource state. |
| `flink` | `ListGMSProject`, `ListGMCSResourcePool` | Validated with the Flink compatibility request. `ListGMCSResourcePool` returned a valid empty list; `ListGMSProject` reached Flink business logic and reported the current account is not initialized. Other GWS/GAS APIs require Flink project/resource pool/application/draft IDs and should not be called without creating those resources. |
| `vke` | `ListVirtualNodes`, `CreateVirtualNode` | `ListVirtualNodes` returned an empty list, consistent with no VKE clusters. `CreateVirtualNode` reached VKE and returned missing `VirtualNodeConfig`; real validation requires an existing Kubernetes cluster/kubeconfig and cleanup plan. |
| `CDN` | `DescribeOriginTopStatisticalData` | Request reached the service, but CDN is stopped/not opened for the account (`OperationDenied.ServiceStopped` / `NotFound.Service`). Positive validation requires CDN service activation and a CDN domain with origin traffic. |
| `mcdn` | `DescribeCdnDomainConfig` | Service is unsubscribed (`mcdn.UnsupportedOperation.ServiceUnsubscribed`). Positive validation requires MCDN activation and a CDN domain. |
| `veenedge` | `GetVEENInstanceUsage`, `GetVEEWInstanceUsage`, `GetBandwidthUsage`, `GetBillingUsageDetail` | GET requests against `veenedge.volcengineapi.com` returned `Method Not Allowed`. Positive validation requires service-side confirmation of the accepted method. |
| `sec_agent` | `Run*` workflow APIs | These are workflow/task APIs and need real alert, PCAP, URL, screenshot, or sensitive-text samples to validate meaningful business output. Do not run empty workflow calls as a success criterion. |
| `iot` | all IoT entries | Not tested by user instruction because the service cannot be opened in this account. |

Resource creation gaps for full positive validation:

- Flink: create a temporary Flink project/resource pool/application only after confirming cost/specs, then validate GWS/GAS APIs and delete resources.
- DCDN/CDN/MCDN/Live: require real domains and, for CDN/DCDN stats, actual traffic. Domain ownership, ICP/filing, origin, and certificate setup may be required.
- GA: create accelerator/bandwidth/listener/endpoint resources only after confirming cost and cleanup commands.
- VKE virtual node: requires an existing VKE cluster and kubeconfig; the helper registry does not include a matching virtual-node delete API, so cleanup must be planned through public VKE APIs.
- SecAgent: requires real security workflow input samples and expected-output criteria.
