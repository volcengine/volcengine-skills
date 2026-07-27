# Storage Service Notes

## TOS Is Not Available in This ve Build

The current `ve` command list does not include `tos`. Running `ve tos --help` returns `unknown command`.

Do not troubleshoot TOS bucket operations as CLI parameter mistakes in this environment; there is no matching `ve tos` command to validate.

Use `tosutil` for TOS bucket/object operations when it is installed. Verified local `tosutil v4.1.4` help exposes:

```bash
tosutil mb tos://bucket-name -acl=private -sc=STANDARD
tosutil cp ./dist/app.tar.gz tos://bucket-name/artifacts/app.tar.gz
tosutil presign tos://bucket-name/artifacts/app.tar.gz -vp=15min
tosutil stat tos://bucket-name/artifacts/app.tar.gz
```

If a deployment path cannot require `tosutil`, keep it optional and provide SSH/scp or user-provided artifact URL fallback.

## File-System Creation Is Billable

EFS, FileNAS, and vePFS read paths worked in `cn-beijing`; all returned empty filesystem lists.

Creation is billable and may require zone/product sale checks. FileNAS and vePFS zone APIs include sale/status details; inspect those before choosing a zone.
