# DNS and Edge Service Notes

## CDN Can Be Disabled at Account Level

`ve cdn ListCdnDomains` can fail even though the CLI command exists:

```text
OperationDenied.ServiceStopped: 服务处于停用状态，不支持该操作。
```

Treat this as account service state, not as a request-format bug. CDN domain validation requires the service to be enabled first.

## DNS, PrivateZone, and WAF Need Real Inputs

`ve dns ListZones`, `ve privatezone ListPrivateZones`, and `ve waf ListDomain` returned successfully in `cn-beijing`.

Do not use DNS/PrivateZone/WAF creation as a generic smoke test:

- public DNS zones need a real domain ownership/context;
- PrivateZone record tests need an intended VPC binding;
- WAF domain creation needs a real domain/backend/load-balancer context.
