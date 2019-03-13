from aws_outage.outage import AWSOutage


class RDSOutage(AWSOutage):

    def __init__(self, region, az, duration, instance):
        super().__init__(region, az, duration)
        self.rds_client = self.session.client('rds')
        self.duration = duration
        self.instance = instance

    def __enter__(self):
        return self

    def __exit__(self):
        return self.restore()

    def outage(self):
        # This needs to be a multiAZ deployment else it won't work!
        self.rds_client.reboot_db_instance(
            DBInstanceIdentifier=self.instance,
            ForceFailover=True
        )

    def restore(self, waiter_config=None):
        # this is just waiting for the instance to reboot so the context
        # manager is not async
        waiter = self.rds_client.get_waiter('db_instance_available')
        if waiter_config is None:
            waiter.wait(
                DBInstanceIdentifier=self.instance,
                WaiterConfig={
                    'Delay': 30,
                    'MaxAttempts': 60
                }
            )
        # overwrite the waiter config for bigger instances
        else:
            waiter.wait(
                DBInstanceIdentifier=self.instance,
                WaiterConfig=waiter_config
            )
