# RDS Service Notes

## Explorer Helper Gap

`scripts/fetch_swagger.py --service rdsmysql --list`, `rdspostgresql`, and `rdsmssql` returned HTTP 404 from the Explorer versions endpoint. Use `ve <service> <Action> --help` for these service schemas.

Verified CLI service names in the current `ve` build:

| Engine | CLI service |
|---|---|
| MySQL | `rdsmysql` (`rds_mysql` alias also exists) |
| PostgreSQL | `rdspostgresql` |
| SQL Server | `rdsmssql` |

Do not use `ve rds_postgresql` or `ve rds_mssql`; they return `unknown command`.

## PostgreSQL CLI Pitfalls

`CreateDBInstance` uses `--body` JSON. For HA PostgreSQL, include both a `Primary` and a `Secondary` item in `NodeInfo`; a single primary node fails with `Secondary Node Number is not equal to 1`.

`CreateDBAccount` accepts `AccountPrivileges = "Inherit,Login"` for application login accounts. Do not use MySQL/Redis-style `ReadWrite` for PostgreSQL accounts.

Create the database with `Owner` set to the app account when possible. If migrations still fail on the default `public` schema, call `ModifySchemaOwner` for `SchemaName = "public"` and the application database/account before running migrations.

For `CreateDatabase`, omit `CharacterSetName` unless the accepted enum has been verified for that API call. A real CLI deployment rejected uppercase `UTF8`; the Terraform provider example uses lowercase `utf8`.

PostgreSQL instance creation takes several minutes. Even after the instance reports `Running`, account/database/schema/endpoint operations can briefly fail because the instance is in exclusive status. Retry those follow-up operations with short sleeps instead of recreating the instance.

## Lifecycle and Cleanup Risk

RDS instance creation is long-running and billable. Lifecycle tests should create the smallest postpaid instance, wait until the engine-specific status is available, delete it immediately, and verify the engine-specific list/detail API no longer returns it.

Observed in `cn-beijing`:

- MySQL, PostgreSQL, and SQL Server instance lists returned `0`.
- MySQL, PostgreSQL, and SQL Server allow-list read APIs returned successfully.

Existing allow lists are account resources and must not be deleted unless created by the current test run.
