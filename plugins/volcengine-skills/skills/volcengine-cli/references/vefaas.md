# veFaaS Service Notes

## Dependent APIs Require FunctionId

`ListSandboxes` requires `FunctionId`; a dummy ID reaches the service and returns `ResourceNotFound`.

`CreateTimer`, `CreateKafkaTrigger`, and `CreateSandbox` all depend on an existing function ID. Validate function creation before testing dependent resources.

Delete order for disposable tests:

```text
DeleteKafkaTrigger / DeleteTimer -> KillSandbox if needed -> DeleteFunction
```

Keep `EnableVpc`, TOS mount, NAS mount, and TLS log delivery disabled unless those integrations are specifically under test.

Observed in `cn-beijing`: `ListFunctions` returned `Total: 0`, and availability zones were `cn-beijing-a` through `cn-beijing-d`.
