# CR Service Notes

## Namespace and Repository Calls Need a Registry

`ListNamespaces` without `Registry` fails with:

```text
MissingParameter.Registry: The required parameter Registry is missing.
```

Passing a non-existent registry reaches the service and fails with:

```text
NotFound.Registry: The specified resource dummy not found.
```

Use these errors to distinguish JSON/CLI formatting mistakes from a legitimately missing registry.

## Write APIs Use JSON Body Mode

CR create APIs use `--body` JSON mode. Do not create namespaces or repositories until the registry ID/name is known from `ListRegistries` or `CreateRegistry` output.

Observed in `cn-beijing`: `ListRegistries` returned `TotalCount: 0`; no CR lifecycle test was run.

## Docker Authentication

For push/pull outside the VKE `cr-credential-controller` passwordless path, authenticate Docker with a short-lived CR authorization token:

```bash
token_json=$(ve cr GetAuthorizationToken --Registry "$registry_name")
cr_username=$(printf '%s' "$token_json" | jq -r '.Result.Username // empty')
cr_password=$(printf '%s' "$token_json" | jq -r '.Result.AuthorizationToken')
[ -n "$cr_username" ] || { echo "CR token response missing Result.Username" >&2; exit 1; }
[ -n "$cr_password" ] || { echo "CR token response missing Result.AuthorizationToken" >&2; exit 1; }
printf '%s' "$cr_password" | docker login "$registry_endpoint" \
  --username "$cr_username" \
  --password-stdin
```

Rules:

- Do not print or write `AuthorizationToken` to logs.
- Re-run `GetAuthorizationToken` when Docker push/pull starts failing after a long session; the token is temporary.
- If `Username` is missing from the response, stop and inspect the CR API response; do not invent a fallback username.
- For VKE private CR pulls, prefer the `cr-credential-controller` addon when available; otherwise use an explicit Kubernetes `imagePullSecret`.
