from aws_outage.outage import AWSOutage
from time import sleep


class NetworkOutage(AWSOutage):

    def __init__(self, region, az, duration, vpc_name):
        super().__init__(region, az, duration)
        self.ec2_client = self.session.client('ec2')
        self.vpc_name = vpc_name
        self.vpc_id = self._vpc_name_to_id(self.vpc_name)
        original_acls = self.ec2_client.describe_network_acls(
            NetworkAclIds=[],
            Filters=[{'Name': 'association.subnet-id', 'Values': self.subnets}]
        )['NetworkAcls']
        self.original_acls = original_acls
        #self.outage_acl = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.restore()

    @property
    def subnets(self):
        subnets_raw = self.ec2_client.describe_subnets(
                Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [self.vpc_id]
                    },
                    {
                        'Name': 'availabilityZone',
                        'Values': [self.az]
                    }
                ]
        )
        subnet_ids = [subnet['SubnetId'] for subnet in subnets_raw['Subnets']]
        return subnet_ids

    @property
    def acl_associations(self):
        acls = self.ec2_client.describe_network_acls(
            NetworkAclIds=[],
            Filters=[{'Name': 'association.subnet-id', 'Values': self.subnets}]
        )
        return [acl['Associations'] for acl in acls['NetworkAcls']]

    def _vpc_name_to_id(self, vpc_name):
        vpc_id = self.ec2_client.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [vpc_name]
                }
            ]
        )['Vpcs'][0]['VpcId']
        return vpc_id

    def outage(self, duration=0):
        vpc = self.session.resource('ec2').Vpc(self.vpc_id)
        nacl = vpc.create_network_acl()
        self.outage_acl = nacl
        for acl_associations in self.acl_associations:
            for acl_association in acl_associations:
                if acl_association['SubnetId'] in self.subnets:
                    # fuck you linter - this is 80 chars long and I will leave
                    # it!
                    nacl.replace_association(
                        AssociationId=acl_association['NetworkAclAssociationId']
                    )
        sleep(duration)

    def restore(self):
        ec2 = self.session.resource('ec2')
        for acl in self.original_acls:
            t_acl = ec2.NetworkAcl(acl['NetworkAclId'])
            for acl in self.acl_associations:
                for acl_association in acl:
                    # fuck you linter - this is 80 chars long and I will leave
                    # it!
                    t_acl.replace_association(
                        AssociationId=acl_association['NetworkAclAssociationId']
                    )
        self.outage_acl.delete()
