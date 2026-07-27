# EBS Service Notes

## Existing Volumes Are Often ECS System Disks

`ve storageebs DescribeVolumes` returned an existing system volume attached to an ECS instance. Treat every existing volume as a user resource; never detach or delete it during smoke tests.

## Explorer Helper Gap

`scripts/fetch_swagger.py --service storageebs --list` returned HTTP 404 from the Explorer versions endpoint. Use `ve storageebs <Action> --help` for parameter discovery.

## Lifecycle Risk

`CreateVolume` is billable. If lifecycle testing is approved, use a small postpaid data disk, never attach it to a non-test instance, delete it immediately, and verify the test volume disappears from `DescribeVolumes`.
