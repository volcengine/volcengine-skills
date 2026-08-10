# Observability Service Notes

## TLS Is Not Available in This ve Build

The current `ve` command list does not include `tls`. Running `ve tls --help` returns `unknown command`.

Do not troubleshoot TLS resource operations as CLI parameter mistakes in this environment; there is no matching `ve tls` command to validate.

## CloudMonitor Read Path Works

`ve cloudmonitor ListRules` returned an empty `Data` array in `cn-beijing`. No CloudMonitor rule lifecycle test was run.
