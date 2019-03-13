# oh-my-aws-outage
Simple wrapper around the AWS API to create an outage for a few services.

# Usage

```python
from aws_outage.network_outage import NetworkOutage

# Network outage of one AZ for one or more vpcs
print('[~] Taking service down...')
outage_duration = 30
vpc = 'some-vpc-name'
with NetworkOutage('eu-central-1', 'eu-central-1a', outage_duration, vpc) as o:
    print(f'[+] Service is now down for {outage_duration} seconds!')
    o.outage(duration=outage_duration)
print('[+] Service restored!')
```
