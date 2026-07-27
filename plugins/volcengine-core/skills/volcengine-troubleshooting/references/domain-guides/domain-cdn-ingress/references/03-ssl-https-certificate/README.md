# SSL / HTTPS 证书

用于证书过期、证书链不完整、域名与证书不匹配、HTTPS 访问提示不安全、CDN/CLB/ALB 证书绑定异常。

## 前置输入

- 域名、证书 ID、CommonName/SAN、错误文本。
- CDN 域名、CLB/ALB Listener ID。
- 浏览器错误类型、发生时间。

## 命令包

### 1. 证书中心查询

```text
ve certificateservice CertificateGetInstanceList --body '{"PageNumber":1,"PageSize":10,"Domain":"<domain>"}'
ve certificateservice CertificateGetInstance --body '{"InstanceId":"<certificate-instance-id>"}'
```

关注字段：证书状态、过期时间、CommonName、SAN、是否吊销。

### 2. CDN 证书绑定

```text
ve cdn ListCdnCertInfo --body '{"PageNum":1,"PageSize":10}'
ve cdn DescribeCertConfig --body '{"Domain":"<cdn-domain>"}'
```

关注字段：证书 ID、域名匹配、HTTPS 配置、强制跳转和回源协议。

### 3. CLB / ALB 证书

```text
ve clb DescribeCertificates --PageNumber 1 --PageSize 10
ve clb DescribeListenerAttributes --ListenerId <listener-id>
ve alb DescribeCertificates --PageNumber 1 --PageSize 10
ve alb DescribeListenerAttributes --ListenerId <listener-id>
```

关注字段：监听协议、证书 ID、SNI/扩展证书、TLS 策略。

## 本地补证据

```text
ve certificateservice ListCertificates
ve cdn ListCdnDomains --body '{"PageNum":1,"PageSize":10}'
```

只摘录证书主题、颁发者、有效期、SAN 和 TLS 错误，不输出私钥。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 证书过期或吊销 | 证书生命周期问题 |
| SAN 不含访问域名 | 证书域名不匹配 |
| CDN 证书正确但源站证书错 | 回源 HTTPS 或源站直连问题 |
| CLB/ALB 监听器证书不一致 | 监听器或 SNI 配置问题 |

## 变更边界

上传、替换、绑定、部署、删除证书都必须确认；不要输出证书私钥。
