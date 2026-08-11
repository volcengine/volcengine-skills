# VKE Service Notes

## Cluster APIs Use JSON Body Mode

`CreateCluster` and `DeleteCluster` use `--body` JSON mode.

```bash
ve vke CreateCluster --body '{
  "Name": "<cluster-name>",
  "ClusterConfig": {"SubnetIds": ["<subnet-id>"]},
  "PodsConfig": {
    "PodNetworkMode": "Flannel",
    "FlannelConfig": {"PodCidrs": ["172.16.0.0/16"]}
  },
  "ServicesConfig": {"ServiceCidrsv4": ["172.20.0.0/16"]},
  "Tags": [{"Key": "publish-by", "Value": "deploy-skill"}]
}'
ve vke DeleteCluster --body '{"Id":"<cluster-id>","Force":true}'
```

## Lifecycle Risk

Cluster creation is high-cost and long-running, and can create dependent ECS, network, log, and addon resources. Do not run it as a casual smoke test.

If explicitly approved, record every returned resource ID, use `DeleteCluster` with an explicit retention/deletion policy, and verify `ListClusters` no longer returns the test cluster. A newly created cluster can reject deletion while its status is `Creating` or addon sync is still `Progressing`; poll `ListClusters` until the cluster reaches `Running`/`Ok`, then delete.

Observed in `cn-beijing`: clusters, node pools, kubeconfigs, and addons all returned empty lists; supported addon/resource-type discovery worked.

Validation note: a no-node Flannel cluster with `Tags: [{"Key":"publish-by","Value":"deploy-skill"}]` was created in `cn-beijing`, the tag appeared in `ListClusters`, then `DeleteCluster` removed it after the cluster reached `Running`/`Ok`.

## Addons That Affect Basic Deployments

`ListSupportedAddons` returned both `core-dns` and `cr-credential-controller` as `Unmanaged` addons.

- `core-dns` is the cluster DNS/service-discovery foundation. If workloads cannot resolve Kubernetes service names, check `ListAddons`/cluster addon state before debugging application DNS.
- `cr-credential-controller` supports passwordless pulls from Volcengine CR. Without it, private CR images may require explicit image pull credentials, and Pods can fail with image pull authentication errors.
